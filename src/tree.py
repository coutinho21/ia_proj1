class Tree:
    def __init__(self, nodes):
        self.nodes = nodes

class Node:
    def __init__(self, value, data, children, type):
        self.value = value
        self.data = data
        self.children = children
        self.type = type
