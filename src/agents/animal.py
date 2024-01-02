from abc import ABC, abstractmethod
from numpy import arctan2, degrees
from random import choice
from enum import IntEnum
from typing import Tuple
import mesa

class ViewDirection(IntEnum):
    TOP = 90
    RIGHT = 0
    BOTTOM = -90
    LEFT = 180
    TOP_RIGHT = 45
    BOTTOM_RIGHT = -45
    BOTTOM_LEFT = -135
    TOP_LEFT = 135

    def get(move: Tuple[int, int]) -> 'ViewDirection':
        directions = {
            (1, 1): ViewDirection.BOTTOM_RIGHT,
            (1, -1): ViewDirection.TOP_RIGHT,
            (1, 0): ViewDirection.RIGHT,
            (-1, 1): ViewDirection.BOTTOM_LEFT,
            (-1, -1): ViewDirection.TOP_LEFT,
            (-1, 0): ViewDirection.LEFT,
            (0, 1): ViewDirection.BOTTOM,
            (0, -1): ViewDirection.TOP
        }

        return directions.get(move)

class Animal(mesa.Agent, ABC):
    """Animal interface"""

    def __init__(
        self,
        model: mesa.Model,
        lifetime: int,
        consumption: int,
        speed: int,
        trace: int,
        view_range: int,
        view_angle: int = 360
    ):
        super().__init__(model.next_id(), model)
        self.lifetime = lifetime
        self.consumption = consumption
        self.speed = speed
        self.trace = trace
        self.view_range = view_range
        self.view_angle = view_angle
        self.view_direction = choice(list(ViewDirection))
        self.eaten = 0

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.pos}"

    @abstractmethod
    def step(self) -> None:
        """
        An Animal step. Move, eat, etc.
        """
        pass

    def remove(self) -> None:
        """
        Remove the animal from the grid and the scheduler.
        """
        self.model.grid.remove_agent(self)
        self.model.scheduler.remove(self)

    def get_neighbors_within_angle(self):
        neighbors = []
        possible_neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.view_range
        )
        for agent in possible_neighbors:
            if agent.unique_id != self.unique_id:
                dx = agent.pos[0] - self.pos[0]
                dy = agent.pos[1] - self.pos[1]

                # Calculate angle between current agent and the potential neighbor

                angle_to_agent = arctan2(dy, dx)
                angle_to_agent = degrees(angle_to_agent) % 360

                # Calculate the angle difference (absolute value)
                angle_diff = abs((angle_to_agent - int(self.view_direction) + 180) % 360 - 180)

                # If the angle difference is within the desired view angle, consider it a neighbor
                if angle_diff <= self.view_angle // 2:
                    neighbors.append(agent)

        return neighbors

    def sees(self, agent: 'Animal') -> bool:
        return agent in self.get_neighbors_within_angle()

    def random_move(self, distance: int = 1) -> None:
        """
        Step one cell in any allowable direction.
        """

        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            radius=distance
        )
        next_move = self.random.choice(next_moves)

        # Change view direction
        dx = (next_move[0] > self.pos[0]) - (next_move[0] < self.pos[0])
        dy = (next_move[1] < self.pos[1]) - (next_move[1] > self.pos[1])

        self.view_direction = ViewDirection.get((dx, dy))

        # Now move.
        self.model.grid.move_agent(self, next_move)
