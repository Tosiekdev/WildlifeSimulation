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

    def add_sound(self, x: int, y: int):
        if not self.model.grid.out_of_bounds((x, y)):
            self.edge = False
            new_sound = Sound(self.model, self.r, self.direction, True)
            self.model.scheduler.add(new_sound)
            self.model.grid.place_agent(new_sound, (x, y))

    def step(self) -> None:
        self.r += 1
        self.force = Sound.FORCE / self.r ** 2
        if self.r > 5:
            self.model.grid.remove_agent(self)
            self.model.scheduler.remove(self)
            return

        x, y = self.pos
        match self.direction:
            case Direction.TOP:
                y += 1
                if self.edge:
                    self.add_sound(x - 1, y)
            case Direction.RIGHT:
                x += 1
                if self.edge:
                    self.add_sound(x, y + 1)
            case Direction.DOWN:
                y -= 1
                if self.edge:
                    self.add_sound(x + 1, y)
                pass
            case Direction.LEFT:
                x -= 1
                if self.edge:
                    self.add_sound(x, y - 1)
                pass
            case Direction.TOP_LEFT:
                x -= 1
                if self.edge:
                    self.add_sound(x, y + 1)
                pass
            case Direction.TOP_RIGHT:
                y += 1
                if self.edge:
                    self.add_sound(x + 1, y)
                pass
            case Direction.DOWN_RIGHT:
                x += 1
                if self.edge:
                    self.add_sound(x, y - 1)
                pass
            case Direction.DOWN_LEFT:
                y -= 1
                if self.edge:
                    self.add_sound(x - 1, y)
                pass

        self.edge = False
        if not self.model.grid.out_of_bounds((x, y)):
            self.model.grid.move_agent(self, (x, y))
        else:
            self.model.grid.remove_agent(self)
            self.model.scheduler.remove(self)
