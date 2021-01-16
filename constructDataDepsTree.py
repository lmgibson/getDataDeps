import json
import pydot
import pprint

with open('./dataDeps.json') as json_file:
    data = json.load(json_file)

# data = {'A': {'To': ['B', 'C'], 'From': None},
#         'B': {'To': None, 'From': 'A'},
#         'C': {'To': None, 'From': 'A'}}


def createDepGraph(data):
    dot_graph = pydot.Dot(graph_type='digraph')

    for i, val in enumerate(data):
        # Add node for the dataset
        node = pydot.Node(val)
        node.set_shape('box2d')
        dot_graph.add_node(node)

        # Add nodes above the dataset for the file(s) that create it
        # Add an edge from the file to the dataset
        for j in data[val]['save']:
            node = pydot.Node(j)
            node.set_shape('box2d')
            dot_graph.add_node(node)

            edge = pydot.Edge(j, val)
            dot_graph.add_edge(edge)

        # Add edges from the dataset to the files it is read by
        if data[val]['read']:
            for j in data[val]['read']:
                edge = pydot.Edge(val, j)
                dot_graph.add_edge(edge)

    return dot_graph


graph = createDepGraph(data)
graph.write_svg('test.svg')

# dot_graph = pydot.Dot(graph_type='digraph')

# sd_node = pydot.Node('A')
# sd_node.set_shape('box3d')
# dot_graph.add_node(sd_node)

# qsd_node = pydot.Node('B')
# qsd_node.set_shape('box3d')
# dot_graph.add_node(qsd_node)

# iedge = pydot.Edge(sd_node, qsd_node)
# iedge.set_label('Tables')
# dot_graph.add_edge(iedge)
