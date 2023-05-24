import random
import numpy as np

import math
from scipy.spatial.distance import cityblock

from agent import Agent

N_ACTIONS = 4
DOWN, UP, RIGHT, LEFT = range(N_ACTIONS)

class RandomAgent(Agent):

    def __init__(self):
        super(RandomAgent, self).__init__("Random Agent")
        self.n_actions = 4

    def action(self) -> int:
        return np.random.choice(np.arange(self.n_actions))
        

class FullyGreedyAgent(Agent):

    def __init__(self, agent_id, debug):
        super(FullyGreedyAgent, self).__init__(f"Greedy Agent")
        self.agent_id = agent_id
        self.n_agents = 2
        self.n_actions = 4
        self.debug = debug

    def action(self) -> int:
        agents_positions = self.observation[0][0]
        agent_pos = agents_positions[self.agent_id-1]
        food_pos = self.observation[0][1][self.agent_id-1]
        if self.debug:
            print("Agent", self.agent_id, ": ", agent_pos[0])
            print("Food", self.agent_id,": ", food_pos)
        return self.direction_to_go(agent_pos[0], food_pos)


    # ################# #
    # Auxiliary Methods #
    # ################# #

    def direction_to_go(self, agent_position, food_position):
        """
        Given the position of the agent and the position of a food,
        returns the action to take in order to close the distance
        """
        distances = np.array(food_position) - np.array(agent_position)
        roll = random.uniform(0, 1)
        return self._close_horizontally(distances) if roll > 0.5 else self._close_vertically(distances)

    # ############### #
    # Private Methods #
    # ############### #

    def _close_horizontally(self, distances):

        if distances[0] == 0:
            return self._close_vertically(distances)

        elif distances[0] > 0:
            if self.debug:
                print("Direction: Right")
            return RIGHT
        elif distances[0] < 0:
            if self.debug:
                print("Direction: Left")
            return LEFT

    def _close_vertically(self, distances):

        if distances[1] == 0:
            return self._close_horizontally(distances)

        elif distances[1] > 0:
            if self.debug:
                print("Direction: UP")
            return UP
        elif distances[1] < 0:
            if self.debug:
                print("Direction: Down")
            return DOWN


class PartiallyGreedyAgent(Agent):

    def __init__(self, agent_id, debug):
        super(PartiallyGreedyAgent, self).__init__(f"Greedy Agent")
        self.agent_id = agent_id
        self.n_agents = 2
        self.n_actions = 4
        self.debug = debug

    def action(self) -> int:
        agents_positions = self.observation[0][0]
        agent_pos = agents_positions[self.agent_id-1]
        food_pos = self.observation[0][1][self.agent_id-1]
        if self.debug:
            print("Agent", self.agent_id, ": ", agent_pos[0])
            print("Food", self.agent_id,": ", food_pos)
        return self.direction_to_go(agent_pos[0], food_pos)


    # ################# #
    # Auxiliary Methods #
    # ################# #

    def direction_to_go(self, agent_position, food_position):
        """
        Given the position of the agent and the position of a food,
        returns the action to take in order to close the distance
        """
        distances = np.array(food_position) - np.array(agent_position)

        
        if (self._snake_adj_horizontally()):
            return self._close_vertically(distances, False)
        if (self._snake_adj_vertically()):
            return self._close_horizontally(distances, False)

        roll = random.uniform(0, 1)
        return self._close_horizontally(distances, False) if roll > 0.5 else self._close_vertically(distances, False)

    # ############### #
    # Private Methods #
    # ############### #

    def _snake_adj_horizontally(self):
        agent_pos = self.observation[0][0][self.agent_id-1]
        agent_head = agent_pos[0]
        other_snake_pos = self.observation[0][0][self.agent_id%2]
        for block in other_snake_pos:
            if (block == [agent_head[0]+10, agent_head[1]] or block == [agent_head[0]-10, agent_head[1]]):
                return True

        return False

    def _snake_adj_vertically(self):
        agent_pos = self.observation[0][0][self.agent_id-1]
        agent_head = agent_pos[0]
        other_snake_pos = self.observation[0][0][self.agent_id%2]
        for block in other_snake_pos:
            if (block == [agent_head[0], agent_head[1]+10] or block == [agent_head[0], agent_head[1]-10]):
                return True

        return False

    def _close_horizontally(self, distances, forced):
        agent_pos = self.observation[0][0][self.agent_id-1]
        agent_head = agent_pos[0]
        agent_neck = agent_pos[1]

        #If fruit is on same x
        if distances[0] == 0 and not forced:
            return self._close_vertically(distances, False)

        #Avoid self-collision
        elif agent_head[0] == agent_neck[0]+10:
            #Avoid some wall situations
            if agent_head[0] == 290 and not self._snake_adj_vertically():
                return self._close_vertically(distances, True)
            if self.debug:
                print("Direction: Right")
            return RIGHT
        elif agent_head[0] == agent_neck[0]-10:
            #Avoid some wall situations
            if agent_head[0] == 10 and not self._snake_adj_vertically():
                return self._close_vertically(distances, True)
            if self.debug:
                print("Direction: Left")
            return LEFT

        #Go in the fruit's direction
        elif distances[0] > 0:
            if self.debug:
                print("Direction: Right")
            return RIGHT
        elif distances[0] < 0:
            if self.debug:
                print("Direction: Left")
            return LEFT

        #If forced and in same x, randomize movement
        roll = random.uniform(0, 1)
        return LEFT if roll > 0.5 else RIGHT

    def _close_vertically(self, distances, forced):
        agent_pos = self.observation[0][0][self.agent_id-1]
        agent_head = agent_pos[0]
        agent_neck = agent_pos[1]

        if distances[1] == 0 and not forced:
            return self._close_horizontally(distances, False)

        #Avoid self-collision
        if agent_head[1] == agent_neck[1]+10:
            #Avoid some wall collisions
            if agent_head[1] == 290 and not self._snake_adj_horizontally():
                return self._close_horizontally(distances, True)
            if self.debug:
                print("Direction: UP")
            return UP
        elif agent_head[1] == agent_neck[1]-10:
            if agent_head[1] == 10 and not self._snake_adj_horizontally():
                return self._close_horizontally(distances, True)
            if self.debug:
                print("Direction: Down")
            return DOWN

        #Go in the fruit's direction
        elif distances[1] > 0:
            if self.debug:
                print("Direction: UP")
            return UP
        elif distances[1] < 0:
            if self.debug:
                print("Direction: Down")
            return DOWN
        
        #If forced and in same y, randomize movement
        roll = random.uniform(0, 1)
        return UP if roll > 0.5 else DOWN
