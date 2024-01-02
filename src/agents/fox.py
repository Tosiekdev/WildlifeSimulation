import importlib
from enum import Enum
from typing import Tuple, List
from random import choice

import mesa
import numpy as np

from .animal import Animal, ViewDirection
from .sound import Sound, Direction
from .pheromone import Pheromone


class State(Enum):
    SNEAKING = 1
    WALKING = 2
    SPRINTING = 3


class Fox(Animal):

    def __init__(self,
                 model,
                 home: Tuple,
                 lifetime=160,
                 consumption=5,
                 speed=6,
                 trace=5,
                 view_range=6,
                 view_angle=135,
                 smelling_range=10,
                 attack_range=3,
                 ):
        super().__init__(model, lifetime, consumption, speed, trace, view_range, view_angle)
        self.smelling_range = smelling_range
        self.home = home
        self.hunting = True
        self.state = State.WALKING
        self.attack_range = attack_range
        self.focused_hare = None

    @staticmethod
    def create(model: mesa.Model, pos: Tuple[int, int]):
        fox = Fox(model, pos)
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

    def kill(self):
        if self.focused_hare and self.focused_hare.pos == self.pos:
            self.focused_hare.remove()
            self.hunting = False
            self.focused_hare = None

    def go_in_direction(self, direction):
        dx = direction[0] - self.pos[0]
        dy = direction[1] - self.pos[1]
        direction = np.array([dx, dy], dtype=float)
        direction /= np.linalg.norm(direction)
        if direction[1] > np.sin(22.5 / 180):
            dy = 1
        elif direction[1] < -np.sin(22.5 / 180):
            dy = -1
        else:
            dy = 0

        if direction[0] > np.cos(67.5 / 180):
            dx = 1
        elif direction[0] < -np.cos(67.5 / 180):
            dx = -1
        else:
            dx = 0

        self.model.grid.move_agent(self, (self.pos[0] + dx, self.pos[1] + dy))
        self.view_direction = ViewDirection.get((dx, dy))
        self.kill()

    def return_to_home(self):
        self.go_in_direction(self.home)
        if self.pos == self.home:
            self.hunting = True

    def get_hares_in_attack_range(self) -> List[Animal]:
        hare = importlib.import_module("src.agents.hare")
        view_range = self.view_range
        self.view_range = self.attack_range
        neighbors = self.get_neighbors_within_angle()
        self.view_range = view_range
        hares = [neighbor for neighbor in neighbors if type(neighbor) is hare.Hare]

        return hares

    def get_hares_in_sneaking_range(self) -> List[Animal]:
        hare = importlib.import_module("src.agents.hare")
        hares_in_attack_range = self.get_hares_in_attack_range()
        neighbors = self.get_neighbors_within_angle()
        hares = [neighbor for neighbor in neighbors if type(neighbor) is hare.Hare and neighbor not in hares_in_attack_range]

        return hares

    def hunt(self):
        """
        Moves fox according to his surroundings.
        """

        if self.focused_hare:
            dist = max(abs(self.pos[0]-self.focused_hare.pos[0]), abs(self.pos[1]-self.focused_hare.pos[1]))
            if dist <= self.view_range:
                if dist <= self.attack_range:
                    self.state = State.SPRINTING
                if self.state == State.SPRINTING:
                    self.go_in_direction(self.focused_hare.pos)
                return

            self.focused_hare = None
        else:
            hares_to_attack = self.get_hares_in_attack_range()
            hares_to_sneak = self.get_hares_in_sneaking_range()
            if hares_to_attack:
                self.state = State.SPRINTING
                self.focused_hare = choice(hares_to_attack)
                self.go_in_direction(self.focused_hare.pos)
                return

            if hares_to_sneak:
                self.focused_hare = choice(hares_to_sneak)
                self.state = State.SNEAKING
                if self.focused_hare.sees(self):
                    return
                else:
                    self.go_in_direction(self.focused_hare.pos)

        smell = self.smell()
        if smell:
            heuristic = max(smell, key=smell.get)
            self.go_in_direction(heuristic)

        else:
            self.random_move()

    def make_noise(self):
        force = 10
        match self.state:
            case State.SNEAKING:
                force = 1
            case State.SPRINTING:
                force = 20
            case _:
                pass

        for ngh in self.model.grid.get_neighborhood(self.pos, moore=True):
            if ngh[0] < self.pos[0] and ngh[1] == self.pos[1]:
                Sound.create_sound(self.model, ngh, 1, Direction.LEFT, True, force)
            elif ngh[0] > self.pos[0] and ngh[1] == self.pos[1]:
                Sound.create_sound(self.model, ngh, 1, Direction.RIGHT, True, force)
            elif ngh[1] < self.pos[1] and ngh[0] == self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.BOTTOM, True, force)
            elif ngh[1] > self.pos[1] and ngh[0] == self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.TOP, True, force)
            elif ngh[1] > self.pos[1] and ngh[0] < self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.TOP_LEFT, True, force)
            elif ngh[1] > self.pos[1] and ngh[0] > self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.TOP_RIGHT, True, force)
            elif ngh[1] < self.pos[1] and ngh[0] > self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.BOTTOM_RIGHT, True, force)
            elif ngh[1] < self.pos[1] and ngh[0] < self.pos[0]:
                Sound.create_sound(self.model, ngh, 1, Direction.BOTTOM_LEFT, True, force)

    def step(self) -> None:
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.remove()
            return

        if self.hunting:
            self.hunt()
        else:
            self.return_to_home()

        self.make_noise()

        print(self)
