from typing import List, Tuple


class Edge:
    """
    Class for the edges of the graph
    """

    def __init__(self, o: int, d: int, c: float, p: int = 0) -> None:
        """
        Each edge in the graph has origin, destiny, cost and
        pheromone trail

        Arguments:
            o [int]:    Origin of the edge
            d [int]:    Destination of the edge
            c [float]:  Cost of travelling the edge
            p [int]:    Pheromone trail in the edge, defaults to 0
        """

        self.o = o
        self.d = d
        self.c = c
        self.p = p

    def connected(self, vertex: int) -> int:
        """
        Returns the vertex the input is connected to. If there is none,
        returns -1

        Arguments:
            vertex [int]:       Vertex to check if is connected to it

        Return:
            connected [int]:    The vertex it is connected to. -1
        """

        connected = -1

        if vertex == self.o:
            connected = self.d
        elif vertex == self.d:
            connected = self.o

        return connected


class Graph:
    """
    Class for defining the graph where the ant colony will do search
    """

    def __init__(
        self,
        V: int,
        E: List[Edge],
        colony: int,
        food: int,
        V_position: List[Tuple[int, int]],
    ) -> None:
        """
        Graph for path solving

        Arguments:
            V [int]:                            Number of vertex in the graph
            E [List[Edge]]:                     List of edges of the graph,
                                                with distances and weights
            food [int]:                         Vertex where the colony is
            food [int]:                         Vertex where the food is
            V_position [List[Tuple[int, int]]]: Position of each vertex in
                                                the graph
        """

        self.V = list(range(V))
        self.E = E
        self.colony = colony
        self.food = food
        self.V_position = V_position

    def get_neighbor(self, position: int) -> Tuple[List[int], List[float], List[int]]:
        """
        Returns all the vertices connected to the position, with the
        cost and the pheromone

        Arguments:
            position [int]:         Vertex to check the neighbors from

        Returns:
            vertices [List[int]]:   Vertices which is connected to
            costs [List[float]]:    Cost to get toeach vertice
            pheromones [List[int]]: Pheromone value of the edge to
                                    get to each vertex
        """

        vertices = []
        costs = []
        pheromones = []

        for edge in self.E:

            connected = edge.connected(position)

            if connected != -1:
                vertices.append(connected)
                costs.append(edge.c)
                pheromones.append(edge.p)

        return vertices, costs, pheromones

    def is_food(self, position: int) -> bool:
        """
        Return if the position is food or not

        Arguments:
            position [int]: Position where to check

        Returns:
            is_foof [bool]: If the position is food or not
        """

        is_food = position == self.food

        return is_food

    def is_home(self, position: int) -> bool:
        """
        Return if the position is at the colony or not

        Arguments:
            position [int]: Position where to check

        Returns:
            is_gome [bool]: If the position is at the colony or not
        """

        is_home = position == self.colony

        return is_home

    def add_pheromone(self, origin: int, dest: int) -> None:
        """
        Add pheromone trail to a given position

        Arguments:
            origin [int]:   One conexion of the edge
            dest [int]:     Other conexion of the edge
        """

        for e in self.E:
            if (e.o == origin or e.d == origin) and (e.o == dest or e.d == dest):
                e.p += 1
