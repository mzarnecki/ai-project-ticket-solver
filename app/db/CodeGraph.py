import pickle

import networkx as nx

class CodeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as f:
            instance = pickle.load(f)
        return instance

    def add_file(self, metadata):
        self.graph.add_node(metadata['file_path'], **metadata)
        # Add edges for class inheritance
        if metadata.get('parent_class'):
            self.graph.add_edge(metadata['file_path'], metadata['parent_class'])
        # Add edges for dependencies
        for dep in metadata.get('dependencies', []):
            self.graph.add_edge(metadata['file_path'], dep)

    def get_relations(self, file_path):
        node = self.graph.nodes.get(file_path, {})
        all_related = list(nx.descendants(self.graph, file_path)) + list(node.get('methods', []))
        all_related.sort()
        return {
            'parent': node.get('parent_class'),
            'dependencies': node.get('dependencies', []),
            'methods': node.get('methods', []),
            'all_related': all_related
        }
