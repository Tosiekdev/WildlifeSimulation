from typing import Tuple

import mesa
from enum import Enum


class Direction(Enum):
    TOP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    TOP_LEFT = 5
    TOP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8


class Sound(mesa.Agent):
    FORCE = 10.0
    MIN_FORCE = 0.1

    def __init__(self, model: mesa.Model, r: int, direction: Direction, edge: bool = False):
        super().__init__(model.next_id(), model)
        self.force = Sound.FORCE / r ** 2
        self.r = r
        self.edge = edge
        self.direction = direction

    @staticmethod
    def create_sound(model: mesa.Model, pos: Tuple[int, int], radius: int, direction: Direction, edge=True):
        if not model.grid.out_of_bounds(pos):
            new_sound = Sound(model, radius, direction, edge)
            model.scheduler.add(new_sound)
            model.grid.place_agent(new_sound, pos)

    def update_vale(self):
        self.r += 1
        self.force = Sound.FORCE / self.r ** 2

    def step(self) -> None:
        self.update_vale()
        if self.r > 5:
            self.model.grid.remove_agent(self)
            self.model.scheduler.remove(self)
            return

        x, y = self.pos
        match self.direction:
            case Direction.TOP:
                y += 1
                if self.edge:
                    Sound.create_sound(self.model, (x - 1, y), self.r, self.direction)
            case Direction.RIGHT:
                x += 1
                if self.edge:
                    Sound.create_sound(self.model, (x, y + 1), self.r, self.direction)
                pass
            case Direction.DOWN:
                y -= 1
                if self.edge:
                    Sound.create_sound(self.model, (x + 1, y), self.r, self.direction)
            case Direction.LEFT:
                x -= 1
                if self.edge:
                    Sound.create_sound(self.model, (x, y - 1), self.r, self.direction)
            case Direction.TOP_LEFT:
                x -= 1
                if self.edge:
                    Sound.create_sound(self.model, (x, y + 1), self.r, self.direction)
            case Direction.TOP_RIGHT:
                y += 1
                if self.edge:
                    Sound.create_sound(self.model, (x + 1, y), self.r, self.direction)
            case Direction.DOWN_RIGHT:
                x += 1
                if self.edge:
                    Sound.create_sound(self.model, (x, y - 1), self.r, self.direction)
            case Direction.DOWN_LEFT:
                y -= 1
                if self.edge:
                    Sound.create_sound(self.model, (x - 1, y), self.r, self.direction)

        self.edge = False
        if not self.model.grid.out_of_bounds((x, y)):
            self.model.grid.move_agent(self, (x, y))
        else:
            self.model.grid.remove_agent(self)
            self.model.scheduler.remove(self)
