"""
Utils file to the Ant Colony Optimization Algorithm
"""
from typing import Tuple

from MultiAgentAlg.AntColonyOptimization.ant import Colony
from MultiAgentAlg.AntColonyOptimization.graph import Edge, Graph


def instance_reader(filename: str) -> Tuple[Colony, Graph]:
    """
    Function to transform from a file to a problem instance

    Arguments:
        filename [str]: File from where to read the instance

    Returns:
        c [Colony]      Colony with the appropriate parameters
        g [Graph]       Graph with the appropriate parameters
    """

    with open(filename, "r") as f:

        lines = f.readlines()

        c_pos = int(lines[0])
        num_ants = int(lines[1])

        food_pos = int(lines[2])

        num_vertex = int(lines[3])

        edge_list = []

        for i in range(num_vertex):
            for j, dist in enumerate(lines[4 + i].split(" ")):
                dist = int(dist)
                if dist != -1:
                    edge = Edge(i, j, dist)
                    edge_list.append(edge)

        vertex_pos_list = []
        for i in range(num_vertex):
            x, y = lines[4 + num_vertex + i].split(" ")
            x = int(x)
            y = int(y)
            vertex_pos_list.append((x, y))

        c = Colony(num_ants, c_pos)
        g = Graph(num_vertex, edge_list, c_pos, food_pos, vertex_pos_list)

    return c, g
