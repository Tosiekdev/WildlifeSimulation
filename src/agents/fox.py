import mesa

from .animal import Animal
from .sound import Sound, Direction


class Fox(Animal):

    def __init__(self,
                 model,
                 lifetime=4,
                 consumption=5,
                 speed=6,
                 trace=10,
                 view_range=135
                 ):
        super().__init__(model, lifetime, consumption, speed, trace, view_range)

    def step(self) -> None:
        for ngh in self.model.grid.get_neighborhood(self.pos, moore=True):
            sound = None
            if ngh[0] < self.pos[0] and ngh[1] == self.pos[1]:
                sound = Sound(self.model, 1, Direction.LEFT, True)
            elif ngh[0] > self.pos[0] and ngh[1] == self.pos[1]:
                sound = Sound(self.model, 1, Direction.RIGHT, True)
            elif ngh[1] < self.pos[1] and ngh[0] == self.pos[0]:
                sound = Sound(self.model, 1, Direction.DOWN, True)
            elif ngh[1] > self.pos[1] and ngh[0] == self.pos[0]:
                sound = Sound(self.model, 1, Direction.TOP, True)
            elif ngh[1] > self.pos[1] and ngh[0] < self.pos[0]:
                sound = Sound(self.model, 1, Direction.TOP_LEFT, True)
            elif ngh[1] > self.pos[1] and ngh[0] > self.pos[0]:
                sound = Sound(self.model, 1, Direction.TOP_RIGHT, True)
            elif ngh[1] < self.pos[1] and ngh[0] > self.pos[0]:
                sound = Sound(self.model, 1, Direction.DOWN_RIGHT, True)
            elif ngh[1] < self.pos[1] and ngh[0] < self.pos[0]:
                sound = Sound(self.model, 1, Direction.DOWN_LEFT, True)

            self.model.grid.place_agent(sound, ngh)
            self.model.scheduler.add(sound)
        self.random_move()
        print(self)
