import random
import sys
from typing import Tuple

import pygame

from MultiAgentAlg.AntColonyOptimization.graph import Graph


class Ant:
    """
    Ant class that moves through the graph to retrieve food to the colony
    """

    def __init__(self, position: int) -> None:
        """
        Ant to traverse the graph

        Arguments:
            position [int]:     Initial position of the ant
        """

        self.position = position
        # Position to display midway (only visual help)
        self.prev_position = position
        self.path = []
        # If the is carrying food at the moment
        self.found_food = False
        # Time the ant has to wait to decide next move
        # as right now is travelling a path
        self.waiting = 0
        # For displaying movement between vertex (only visual help)
        self.total_cost_path = 0

    def move(self, position: int, cost: int) -> None:
        """
        The ant moves to a new position, registering the last
        position in its path, to backtrack later

        Arguments:
            position [int]: New position of the ant
            cost[int]:      Cost of the movement
        """
        self.waiting = cost
        self.total_cost_path = cost

        self.path.append(self.position)
        self.prev_position = self.position
        self.position = position

    def select_path(self, G: Graph, exploring_prob: float = 0.1) -> None:
        """
        Select a path from it's current position to move to
        going to the path with highest pheromone trace, but 
        exploring with a pobability

        Arguments:
            G [Graph]:              Graph where to check the movements
            exploring_prob [float]: Exploration probability, defaults to .1
                                    
        """
        # vertices, costs and pheromones trailexploring_prob
        v, c, p = G.get_neighbor(self.position)

        if random.random() >= exploring_prob:
        # If there are multiple max pheromones traces, select randomly
            possible_paths_index = [i for i, x in enumerate(p) if x == max(p)]
        else:
            # If exploring, move randomly
            possible_paths_index = [i for i, x in enumerate(p)]
            
        selected_path_index = random.choice(possible_paths_index)

        new_position = v[selected_path_index]
        cost = c[selected_path_index]

        # Move to that position
        # This can lead to cicles, but that should not matter
        # as eventually will get to the best position
        self.move(new_position, cost)

    def fix_backtrack_path(self) -> None:
        """
        Checks if the backtrack has loops and fix them.
        The idea to solve loops is to remove them until there
        are no repeated values.
        """

        index_counter = 0
        # Until there are no repeated values
        while len(self.path) != len(list(set(self.path))):

            # To remove loops, we will delete everything that happened
            # before each index. The explanation is not very good, so
            # let's show an example.
            # Given a path with loops: A -> B -> C -> A -> B -> C -> B-> D
            # The fixed path should be: A -> B -> D
            # Starting from the first, everything that happens between the
            # first and last time that 'A' (the first) appears.
            # Same with all the others second third ...
            # Until there are no repeated

            element_at_index = self.path[index_counter]

            index_where_appear = [
                i for i, x in enumerate(self.path) if x == element_at_index
            ]

            first = index_counter
            last = index_where_appear[-1]

            self.path = self.path[:first] + self.path[last:]

            index_counter += 1

    def backtrack(self, G: Graph) -> None:
        """
        Using the path it has, it traverses back to get to the colony,
        leaving a pheromone trail

        Arguments:
            G [Graph]:  Graph to obtain the edge information
        """

        move_to = self.path.pop()

        v, c, _ = G.get_neighbor(self.position)

        index_of_cost = v.index(move_to)

        self.waiting = c[index_of_cost]
        G.add_pheromone(self.position, move_to)

        self.prev_position = self.position
        self.position = move_to

    def travel(self, G: Graph) -> int:
        """
        Function to do the behaviour of an ant in one tick of time

        Arguments:
            G [Graph]:  Graph where the ant is working

        Returns:
            food [int]: Amount of food found and bringed to the colony
        """

        food = 0

        # If the ant is travelling a path, it has to keep travelling it,
        # cannot do anything else
        # It acn only move if it's in a path intersection
        if self.waiting == 0:

            # Check if is at the colony and has food
            # to deposit it
            if self.found_food:
                if G.is_home(self.position):
                    food += 1
                    self.found_food = False

            # Check if it has found food
            if not self.found_food:
                self.found_food = G.is_food(self.position)

            # If is in a intersection and does not have food, has to keep
            # looking
            if not self.found_food:
                self.select_path(G)
            else:
                # If it has found food, it has to return through the path
                # it has done, but it has to remove the loops first
                self.fix_backtrack_path()
                self.backtrack(G)

        else:
            print(type(self.waiting))
            self.waiting -= 1

        return food


class Colony:
    """
    Class for the ant colony to work as a group
    """

    def __init__(self, num_ants: int, position: int) -> None:
        """
        Ant colony with given size and position

        Arguments:
            num_ants [int]: Number of travelling ants in the colony
            position [int]: Position of the ant colony
        """
        self.position = position

        self.ants = []

        for i in range(num_ants):
            self.ants.append(Ant(self.position))

        self.food = 0

        # PyGame stuff
        pygame.init()

        self.screen = pygame.display.set_mode((750, 750))
        self.clock = pygame.time.Clock()
        self.font_size = 25
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), self.font_size)

    def collect_food(self, time_limit: int, G: Graph, plot_speed: int = 1) -> None:
        """
        Function for the main loop of the algorithm, for every ant
        to look for food and bring back to the colony

        Arguments:
            time_limit [int]:   Maximun iterations of the algorithm
            G [Graph]:          Graph where the ants will move
            plot_speed [int]:   Speed of the plotting, defaults to 1
                                frame per second
        """
        self.print_problem_situation(G, 0)
        time_counter = 1
        for _ in range(time_limit):

            for ant in self.ants:
                self.food += ant.travel(G)

                self.print_problem_situation(G, time_counter)

            

            self.screen.fill((0, 0, 0))

            for edge in G.E:
                origin = G.V_position[edge.o]
                dest = G.V_position[edge.d]

                self.draw_connection(origin, dest, edge.p)

            for i, a in enumerate(G.V_position):
                if G.food == i:
                    self.draw_vertex(a, i, (0, 255, 0))
                elif G.colony == i:
                    self.draw_vertex(a, i, (0, 0, 255))
                else:
                    self.draw_vertex(a, i)

            for ant in self.ants:

                if ant.waiting == 0:
                    position = G.V_position[ant.position]
                    self.draw_ant(position)

                else:
                    direction = G.V_position[ant.position]
                    previous_point = G.V_position[ant.prev_position]
                    path_percentage = (
                        ant.total_cost_path - ant.waiting
                    ) / ant.total_cost_path

                    dist_x = direction[0] - previous_point[0]
                    dist_y = direction[1] - previous_point[1]

                    x = previous_point[0] + path_percentage * dist_x
                    y = previous_point[1] + path_percentage * dist_y

                    position = (x, y)
                    self.draw_ant(position)
            
            # Pheromones are gradually dissapearing
            # For this problem, one will dissapear every 
            # 100 loops from each edge.
            # It cannot be lower than 0
            if time_counter % 100 == 0:
                for edge in G.E:
                    edge.p = max(edge.p-1, 0)

            time_counter += 1

            # EVENTS
            for event in pygame.event.get():

                # Close game
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.flip()

            self.clock.tick(plot_speed)

    def print_problem_situation(self, G: Graph, time_stamp: int) -> None:
        """
        Informative function to display the state of the graph
        and the colony.

        Arguments:
            G [Graph]:          Graph to print the state of
            time_stamp [int]:   Moment of the printing
        """

        print("----------------------------------")
        print(f"Time stamp:\t\t{time_stamp}")
        print(f"Position of the colony:\t{G.colony}")
        print(f"Position of the food:\t{G.food}")
        print(f"Food found:\t\t{self.food}")
        print("----------------------------------")
        for i, ant in enumerate(self.ants):

            food = "-"

            if ant.found_food:
                food = "*"

            print(f"Ant {i+1}:")
            print(f"\tPosition:\t{ant.position}")
            print(f"\tFood:\t\t{food}")
            print(f"\tWaiting:\t{ant.waiting}")

    def draw_connection(self, origin: Tuple[int, int], dest: Tuple[int, int], pheromones: int) -> None:
        """
        Draw the connection from one point to the other to connect vertex

        Arguments:
            origin [Tuple[int, int]]:   Origin point
            dest [Tuple[int, int]]:     Destination point
        """
        pygame.draw.line(self.screen, (255, 255, 255), origin, dest)

        text_pos = ((origin[0] + dest[0]) / 2 + 10, (origin[1] + dest[1]) / 2 + 10)


        text = self.font.render(str(pheromones), True, (255, 255, 255))
        text_rect = text.get_rect(center=text_pos)

        self.screen.blit(text, text_rect)

    def draw_vertex(
        self,
        position: Tuple[int, int],
        text: int,
        color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        """
        Draw the vertexs

        Arguments:
            position [Tuple[int, int]]:     Where to draw the vertex
            text [int]:                     Vertex index
            color [Tuple[int, int, int]]:   Color to draw the vertex.
                                            Defaults to white
        """
        pygame.draw.circle(self.screen, color, position, 25)

        text = self.font.render(str(text), True, (0, 0, 0))
        text_rect = text.get_rect(center=position)

        self.screen.blit(text, text_rect)

    def draw_ant(self, position: Tuple[int, int]) -> None:
        """
        Draws the ant, with some random displacement

        Arguments:
            position [Tuple[int, int]]: Position where to draw the ant
        """
        position = (
            position[0] + random.randint(1, 10),
            position[1] + random.randint(1, 10),
        )
        pygame.draw.circle(self.screen, (0, 255, 255), position, 7)
