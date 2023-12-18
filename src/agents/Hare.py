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
        neighbors = self.model.grid.get_neighbors(self.pos, False, True, 0)
        neighbors = [neighbor for neighbor in neighbors if type(neighbor) is Pheromone]

        if len(neighbors) == 0:
            Pheromone.create(self.model, self.pos, self.trace)
        else:
            pheromone = neighbors[0]
            pheromone.value = self.trace

    def step(self) -> None:
        self.random_move()
        self.leave_trace()
        print(self)
