from typing import Tuple

import mesa
import numpy as np

from .animal import Animal
from .sound import Sound, Direction
from .pheromone import Pheromone


class Fox(Animal):

    def __init__(self,
                 model,
                 lifetime=160,
                 consumption=5,
                 speed=6,
                 trace=5,
                 view_range=135,
                 smelling_range=10
                 ):
        super().__init__(model, lifetime, consumption, speed, trace, view_range)
        self.smelling_range = smelling_range

    @staticmethod
    def create(model: mesa.Model, pos: Tuple[int, int]):
        fox = Fox(model)
        model.grid.place_agent(fox, pos)
        model.scheduler.add(fox)

    def smell(self) -> dict:
        """
        Smell the pheromone in the smelling range.
        """
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.smelling_range
        )
        smell = {neighbor.pos: neighbor.value for neighbor in neighbors if type(neighbor) is Pheromone}

        return smell

    def hunt(self):
        smell = self.smell()
        if smell:
            heuristic = max(smell, key=smell.get)
            dx = heuristic[0] - self.pos[0]
            dy = heuristic[1] - self.pos[1]
            direction = np.array([dx, dy], dtype=float)
            direction /= np.linalg.norm(direction)
            if direction[1] > np.sin(22.5/180):
                dy = 1
            elif direction[1] < -np.sin(22.5 / 180):
                dy = -1
            else:
                dy = 0

            if direction[0] > np.cos(67.5/180):
                dx = 1
            elif direction[0] < -np.cos(67.5 / 180):
                dx = -1
            else:
                dx = 0

            print(dx, dy)

            self.model.grid.move_agent(self, (self.pos[0]+dx, self.pos[1]+dy))


        else:
            self.random_move()

    def step(self) -> None:
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.remove()
            return

        for ngh in self.model.grid.get_neighborhood(self.pos, moore=True):
            if ngh[0] < self.pos[0] and ngh[1] == self.pos[1]:
                Sound.create_sound(self.model, ngh, 1, Direction.LEFT, True)
            elif ngh[0] > self.pos[0] and ngh[1] == self.pos[1]:
                Sound.create_sound(self.model, ngh, 1, Direction.RIGHT, True)
            elif ngh[1] < self.pos[1] and ngh[0] == self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.BOTTOM, True)
            elif ngh[1] > self.pos[1] and ngh[0] == self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.TOP, True)
            elif ngh[1] > self.pos[1] and ngh[0] < self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.TOP_LEFT, True)
            elif ngh[1] > self.pos[1] and ngh[0] > self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.TOP_RIGHT, True)
            elif ngh[1] < self.pos[1] and ngh[0] > self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.BOTTOM_RIGHT, True)
            elif ngh[1] < self.pos[1] and ngh[0] < self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.BOTTOM_LEFT, True)

        self.hunt()

        print(self)
