import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    def child(self):
        if self.left is None and self.right is not None:
            return self.right
        elif self.right is None and self.left is not None:
            return self.left
        else:
            raise ValueError("Both children are defined so child() has an ambiguous return value")

def draw_tree(root, filename = None):
    graph = nx.DiGraph()
    add_node(graph, root)
    
    # Use the dot layout engine from graphviz for a tree structure
    pos = graphviz_layout(graph, prog="dot")

    labels = {n: graph.nodes[n]['label'] for n in graph.nodes}
    nx.draw(graph, pos, labels=labels, with_labels=True, node_size=1500, arrows=False)
    
    # Draw edge labels to show left and right children.
    edge_labels = {(u, v): 'L' if graph.nodes[v]['label'] != 'ε' else 'R' for u, v in graph.edges}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, label_pos=0.3)
    
    if filename is None:
        plt.savefig("./output.png")
    else:
        plt.savefig(filename)


def add_node(graph, node):
    if node:
        graph.add_node(id(node), label=str(node.value))
        if node.left:
            graph.add_edge(id(node), id(node.left))
            add_node(graph, node.left)
        if node.right:
            graph.add_edge(id(node), id(node.right))
            add_node(graph, node.right)

def parse_regex(regex):
    index = 0
    root, index = parse_union(regex, index)
    if index < len(regex):
        raise ValueError("Unexpected characters in the regular expression")
    return root

# Lowest Precedence is union, so it must check for concatenation before doing any processing
def parse_union(regex, index):
    left, index = parse_concatenation(regex, index)
    if index < len(regex) and (regex[index] == '|' or regex[index] == '+'): # Checking for concatenation operator
        index += 1  # Skip '|'/'+
        right, index = parse_union(regex, index) # recursively passing expression on the left of union operator
        left = Node('|', left, right) # combine union into one node
    return left, index

# Third highest precedence is concatenation, so it must call the processing of * to be processed right after it
def parse_concatenation(regex, index):
    left, index = parse_kleene_closure(regex, index)
    if index < len(regex) and regex[index] not in ('|', ')', '+'): # If it finds no special symbol, it must be a terminal which is implicitly concatenated to whatever follows
        right, index = parse_concatenation(regex, index) # recursively parse right side
        if right is not None:
            left = Node('.', left, right) # combine concatenation into one node
    return left, index

# Second highest precedence is *, so it must call the processing of () to be processed right after them
def parse_kleene_closure(regex, index):
    node, index = parse_parentheses(regex, index)
    while index < len(regex) and regex[index] == '*': # Star is unary, must return it as a node without further processing
        node = Node('*', node) # return node with only one child
        index += 1
    return node, index

# Highest Precedence is (), so it must be the lowest in the call stack to get processed first
def parse_parentheses(regex, index):
    if index < len(regex) and regex[index] == '(':
        index += 1  # Skip '('
        node, index = parse_union(regex, index) # if a parenthesis has been spotted, we must recursively build a call stack on the inner expression
        if index >= len(regex) or regex[index] != ')':
            raise ValueError("Missing closing parenthesis")
        index += 1  # Skip ')'
    elif index < len(regex) and (regex[index].isalpha() or regex[index].isnumeric()): # bottommost case, just a terminal and no parenthesis
        node = Node(regex[index])
        index += 1
    else:
        raise ValueError(f"Unexpected symbol {regex[index]} at index {index}")
    return node, index

if __name__ == "__main__":
    regex = "((1|01)10(0)*)*1"
    tree = parse_regex(regex)
    print("Parse tree for the regular expression '{}':".format(regex))
    draw_tree(tree)
