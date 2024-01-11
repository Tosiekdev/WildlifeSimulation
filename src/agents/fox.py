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
                 home: Tuple[int, int],
                 lifetime=160,
                 consumption=5,
                 speed=2,
                 trace=5,
                 view_range=6,
                 view_angle=135,
                 smelling_range=10,
                 attack_range=3,
                 sprint_speed=3,
                 sneak_speed=1
                 ):
        super().__init__(model, lifetime, consumption, speed, trace, view_range, view_angle)
        self.smelling_range = smelling_range
        self.home = home
        self.hunting = True
        self.state = State.WALKING
        self.attack_range = attack_range
        self.focused_hare = None
        self.eaten = 0
        self.sprint_speed = sprint_speed
        self.sneak_speed = sneak_speed

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

    def kill(self) -> None:
        """
        Kills focused hare.
        """

        if self.focused_hare and self.focused_hare.pos == self.pos:
            self.focused_hare.remove()
            self.hunting = False
            self.focused_hare.is_alive = False
            self.focused_hare = None
        self.eaten += 4

    def go_in_direction(self, direction: Tuple[int, int]) -> None:
        """
        Moves fox in specified direction.
        """
        speed = self.speed
        match self.state:
            case State.SPRINTING:
                speed = self.sprint_speed
            case State.SNEAKING:
                speed = self.sneak_speed
            case _:
                speed = self.speed

        dx = direction[0] - self.pos[0]
        dy = direction[1] - self.pos[1]
        direction = np.array([dx, dy], dtype=float)
        direction /= np.linalg.norm(direction)
        dir_x = 0
        dir_y = 0
        if direction[1] > np.sin(22.5 / 180):
            dy = min(dy, speed)
            dir_y = -1
        elif direction[1] < -np.sin(22.5 / 180):
            dy = max(dy, -speed)
            dir_y = 1
        else:
            dy = 0

        if direction[0] > np.cos(67.5 / 180):
            dx = min(dx, speed)
            dir_x = 1
        elif direction[0] < -np.cos(67.5 / 180):
            dx = max(dx, -speed)
            dir_x = -1
        else:
            dx = 0

        self.model.grid.move_agent(self, (self.pos[0] + dx, self.pos[1] + dy))
        self.view_direction = ViewDirection.get((dir_x, dir_y))
        self.kill()

    def return_to_home(self):
        """
        Fox moves in destination of his home and does not hunt.
        """
        self.go_in_direction(self.home)
        if self.pos == self.home:
            self.hunting = True

    def get_hares_in_attack_range(self) -> List[Animal]:
        """
        Returns hares that are seen in the fox attack range.
        """
        hare = importlib.import_module("src.agents.hare")
        view_range = self.view_range
        self.view_range = self.attack_range
        neighbors = self.get_neighbors_within_angle()
        self.view_range = view_range
        hares = [neighbor for neighbor in neighbors if type(neighbor) is hare.Hare]

        return hares

    def get_hares_in_sneaking_range(self) -> List[Animal]:
        """
        Returns hares that are seen in the fox view range.
        """
        hare = importlib.import_module("src.agents.hare")
        hares_in_attack_range = self.get_hares_in_attack_range()
        neighbors = self.get_neighbors_within_angle()
        hares = [neighbor for neighbor in neighbors if type(neighbor) is hare.Hare and neighbor not in hares_in_attack_range]

        return hares

    def attack(self) -> None:
        """
        Set's state to sprinting and goes into hare's direction
        """
        self.state = State.SPRINTING
        self.go_in_direction(self.focused_hare.pos)

    def sneak(self) -> None:
        """
        Set's state to sneaking and implements sneaking logic.
        """
        self.state = State.SNEAKING
        if self.focused_hare.sees(self):
            return
        else:
            self.go_in_direction(self.focused_hare.pos)

    def hunt(self) -> None:
        """
        Moves fox according to his surroundings.
        """
        if self.focused_hare and self.focused_hare.is_alive:
            dist = max(abs(self.pos[0]-self.focused_hare.pos[0]), abs(self.pos[1]-self.focused_hare.pos[1]))

            if dist <= self.view_range:
                if dist <= self.attack_range:
                    self.attack()
                    return

                self.sneak()
                return

            self.focused_hare = None
        else:
            hares_to_attack = self.get_hares_in_attack_range()
            hares_to_sneak = self.get_hares_in_sneaking_range()
            if hares_to_attack:
                self.focused_hare = choice(hares_to_attack)
                self.attack()
                return

            if hares_to_sneak:
                self.focused_hare = choice(hares_to_sneak)
                self.sneak()
                return

        smell = self.smell()
        if smell:
            heuristic = max(smell, key=smell.get)
            self.go_in_direction(heuristic)

        else:
            self.random_move()

    def make_noise(self) -> None:
        """
        Creates noise around last postition.
        """
        force = 10
        match self.state:
            case State.SNEAKING:
                force = 1
            case State.SPRINTING:
                force = 20
            case _:
                pass

        for ngh in self.model.grid.get_neighborhood(self.pos, moore=True):
            dx = (ngh[0] > self.pos[0]) - (ngh[0] < self.pos[0])
            dy = (ngh[1] < self.pos[1]) - (ngh[1] > self.pos[1])
            Sound.create_sound(self.model, ngh, 1, Direction.get((dx, dy)), True, force)

    def hungry(self) -> bool:
        """
        Checks if fox has eaten enough in passing week.
        """
        if self.model.scheduler.steps > 0 and self.model.scheduler.steps % self.model.one_week == 0:
            self.eaten = 0
            if self.eaten < self.consumption:
                return True
        return False

    def step(self) -> None:
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.remove()
            return

        if self.hungry():
            self.remove()
            return

        if self.hunting:
            self.hunt()
        else:
            self.return_to_home()

        self.make_noise()

        print(self)
