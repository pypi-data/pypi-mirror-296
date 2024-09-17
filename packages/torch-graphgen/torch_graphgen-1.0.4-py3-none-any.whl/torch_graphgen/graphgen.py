import os
from typing import List, Union

import torch
from torch.fx.immutable_collections import immutable_list, immutable_dict
import torch.nn as nn
import transformers
from transformers.utils import fx as transfx

from .utils.graph import LayerNode, recording_hook
from .utils.inclusion import is_included, search_for_next_included_layer
from .utils.stats import get_n_components


class LayerGraph:
    def __init__(self, model: nn.Module):
        self.model: nn.Module = model
        self.graph: dict = {}
        self.idx_graph: dict = {}
        self.initial_nodes: List[LayerNode] = []
        # self.adj_list = []
        # self.edge_list = []

        self.model.eval()

        self.gen_layer_graph()
        self.find_initial_nodes()
        self.gen_idx_graph()

    def find_initial_nodes(self):
        self.initial_nodes = [
            node for node in self.graph.values() if len(node.parents) == 0
        ]

    def gen_idx_graph(self):
        if self.idx_graph:
            print(
                "Graph was already generated previously. Call reset() to reset object and regenerate the graph."
            )
            return
        for node in self.graph.values():
            self.idx_graph[node.idx] = node

    def get_node(self, node_identifier: Union[int, str]) -> LayerNode:
        if isinstance(node_identifier, str):
            node = self.graph[node_identifier]
        else:
            node = self.idx_graph[node_identifier]
        return node

    def get_node_module(
        self, node_identifier: Union[int, str]
    ) -> Union[nn.Module, None]:
        node = self.get_node(node_identifier)
        return node.get_module(self.model)

    def reset(self):
        self.__init__(self.model)

    def gen_layer_graph(self):
        if self.graph:
            print(self.graph)
            print(
                "Graph was already generated previously. Call reset() to reset object and regenerate the graph."
            )
            return
        if issubclass(type(self.model), transformers.PreTrainedModel):
            computational_graph = transfx.symbolic_trace(self.model)
        else:
            computational_graph = torch.fx.symbolic_trace(self.model)

        layer_graph = {}

        # Reminder: With regular networks (straight from torch), args[0] contains every parent layer

        # Create base nodes, no edges are created
        for idx, node in enumerate(computational_graph.graph.nodes):
            layer_graph[node.name] = LayerNode(node.name, node.target)

        # Create edges by iterating through the nodes
        for node in reversed(computational_graph.graph.nodes):
            cur_node = layer_graph[node.name]
            if len(node.args) == 0:
                continue
            elif type(node.args[0]) == immutable_list or type(node.args[0]) == tuple:
                for parent in node.args[0]:
                    parent_node = layer_graph[parent.name]
                    parent_node.children.append(cur_node)
                    cur_node.parents.append(parent_node)
            elif type(node.args[0]) == immutable_dict:
                for parent in node.args[0].values():
                    parent_node = layer_graph[parent.name]
                    parent_node.children.append(cur_node)
                    cur_node.parents.append(parent_node)
            else:
                for parent in node.args:
                    if type(parent) == torch.fx.node.Node:
                        parent_name = parent.name
                        parent_node = layer_graph[parent_name]
                        parent_node.children.append(cur_node)
                        cur_node.parents.append(parent_node)

        # Connect is_included layers together, clean up unimportant layers
        for node in reversed(computational_graph.graph.nodes):
            if node.op != "placeholder" and node.op != "output":
                cur_node = layer_graph[node.name]

                # Update parents to nearest included layer
                next_clean_nodes = []
                cur_node.parents = search_for_next_included_layer(
                    self.model, cur_node, "parents", layer_graph, next_clean_nodes
                )

                # Update children to nearest included layer
                next_clean_nodes = []
                cur_node.children = search_for_next_included_layer(
                    self.model, cur_node, "children", layer_graph, next_clean_nodes
                )
        # Clean up the graph by removing layers not in INCLUSION_LIST (which are not connected anymore)
        # Add some additional data like vertices boundaries and layer index
        idx = 0
        cur_lb = 0
        cur_ub = 0
        n_components = 0
        total_n_components = 0
        for name in list(layer_graph.keys()):
            node = layer_graph[name]
            if not is_included(node.get_module(self.model)):
                del layer_graph[name]
            else:
                cur_lb += n_components
                node.idx = idx
                module = node.get_module(self.model)
                n_components = get_n_components(module)
                total_n_components += n_components
                cur_ub += n_components
                node.boundaries = [cur_lb, cur_ub]
                idx += 1

        # self.n_components = total_n_components
        self.graph = layer_graph
        # return total_n_components

    def get_n_components(self):
        total_n_components = 0
        for name in list(self.graph.keys()):
            node = self.graph[name]
            # if not is_included(node.get_module(self.model)):
            #     del self.graph[name]
            # else:
            module = node.get_module(self.model)
            n_components = get_n_components(module)
            total_n_components += n_components
        return total_n_components

    def to_component_edge_list(
        self, output: str, parents=True, children=True, overwrite=False
    ):
        assert parents or children
        # assert not os.path.isfile(output)
        if os.path.isfile(output):
            if overwrite == False:
                print(
                    "Output file already exists, skipping writing edge list because overwrite = False"
                )
                return
            else:
                print(f"Deleted file {output}. Will proceed with overwrite.")
                os.remove(output)
        edge_list = []

        for cur_node in self.graph.values():
            for cur_vertex in range(*cur_node.boundaries):
                next_nodes = []
                if parents:
                    next_nodes.extend(cur_node.parents)
                if children:
                    # If we have parent nodes whose ONLY connections are deleted children (in the exclusion list), then the extend here does nothing and these nodes
                    # do not appear in the edgelists
                    next_nodes.extend(cur_node.children)
                for next_node in next_nodes:
                    edges = map(lambda x: [cur_vertex, x], range(*next_node.boundaries))
                    edge_list.extend(edges)

            # Dump current edge_list
            if len(edge_list) > 100_000:
                with open(output, "a") as f:
                    for edge in edge_list:
                        string = " ".join(map(str, edge))
                        f.write(string + "\n")

                edge_list = []
        # Final write
        with open(output, "a") as f:
            for edge in edge_list:
                string = " ".join(map(str, edge))
                f.write(string + "\n")

    def to_component_adj_list(self, output: str, parents=True, children=True):
        assert parents or children
        assert not os.path.isfile(output)

        adj_list = []
        for cur_node in self.graph.values():
            for _ in range(*cur_node.boundaries):
                vertex_adj_list = []
                next_nodes = []
                if parents:
                    next_nodes.extend(cur_node.parents)
                if children:
                    next_nodes.extend(cur_node.children)
                for next_node in next_nodes:
                    vertex_adj_list.extend(list(range(*next_node.boundaries)))
                adj_list.append(vertex_adj_list)

            # Dump current adj_list
            if len(adj_list) > 10_000:
                with open(output, "a") as f:
                    for edge in adj_list:
                        string = " ".join(map(str, edge))
                        f.write(string + "\n")

                adj_list = []
        # Final write
        with open(output, "a") as f:
            for edge in adj_list:
                string = " ".join(map(str, edge))
                f.write(string + "\n")

    def __len__(self) -> int:
        return len(self.graph)
