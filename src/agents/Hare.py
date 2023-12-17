from .pheromone import Pheromone
from .animal import Animal

class Hare(Animal):
    def __init__(self,
        model,
        lifetime=4,
        consumption=5,
        speed=6,
        trace=1,
        view_range=350
    ):
        super().__init__(model, lifetime, consumption, speed, trace, view_range)

    def leave_trace(self) -> None:
        """
        Leave a trace of pheromone.
        """
        Pheromone.create(self.model, self.pos, self.trace)

    def step(self) -> None:
        self.random_move()
        self.leave_trace()
        print(self)
