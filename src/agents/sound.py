from typing import Tuple

import mesa
from enum import Enum


class Direction(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
    TOP_LEFT = 5
    TOP_RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM_RIGHT = 8

    @staticmethod
    def get(move: Tuple[int, int]) -> 'Direction':
        direction = {
            (-1, 0): Direction.LEFT,
            (-1, 1): Direction.TOP_LEFT,
            (0, 1): Direction.TOP,
            (1, 1): Direction.TOP_RIGHT,
            (1, 0): Direction.RIGHT,
            (1, -1): Direction.BOTTOM_RIGHT,
            (0, -1): Direction.BOTTOM,
            (-1, -1): Direction.BOTTOM_LEFT
        }

        return direction.get(move)


class Sound(mesa.Agent):
    FORCE = 10.0
    MIN_FORCE = 0.1

    def __init__(self, model: mesa.Model, r: int, direction: Direction, edge: bool = False, force: float = None):
        super().__init__(model.next_id(), model)
        self.force = force if force else Sound.FORCE / r ** 2
        self.r = r
        self.edge = edge
        self.direction = direction

    @staticmethod
    def create_sound(model: mesa.Model,
                     pos: Tuple[int, int],
                     radius: int,
                     direction: Direction,
                     edge: bool = True,
                     force: float = None):
        if not model.grid.out_of_bounds(pos):
            new_sound = Sound(model, radius, direction, edge, force)
            model.scheduler.add(new_sound)
            model.grid.place_agent(new_sound, pos)

    def update_vale(self) -> None:
        """
        Updates the radius and current force of the sound.
        """
        self.r += 1
        self.force = Sound.FORCE / self.r ** 2

    def step(self) -> None:
        """
        Propagates the sound.
        """
        self.update_vale()
        if self.force < 0.1:
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
            case Direction.BOTTOM:
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
            case Direction.BOTTOM_RIGHT:
                x += 1
                if self.edge:
                    Sound.create_sound(self.model, (x, y - 1), self.r, self.direction)
            case Direction.BOTTOM_LEFT:
                y -= 1
                if self.edge:
                    Sound.create_sound(self.model, (x - 1, y), self.r, self.direction)

        self.edge = False
        if not self.model.grid.out_of_bounds((x, y)):
            self.model.grid.move_agent(self, (x, y))
        else:
            self.model.grid.remove_agent(self)
            self.model.scheduler.remove(self)
