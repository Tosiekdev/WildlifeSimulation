from typing import Tuple
import mesa

class Pheromone(mesa.Agent):
    def __init__(
        self,
        model: mesa.Model,
        value: int = 1,
        evaporation_rate: float = 0.4,
        diffusion_rate: float = 0.1
    ):
        super().__init__(model.next_id(), model)
        self.value = value
        self.evaporation_rate = evaporation_rate
        self.diffusion_rate = diffusion_rate

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.pos} {self.value}"

    @staticmethod
    def create(model: mesa.Model, pos: Tuple[int, int], value = 1) -> None:
        pheromone = Pheromone(model, value, **model.pheromone_params)
        model.grid.place_agent(pheromone, pos)
        model.scheduler.add(pheromone)

    @property
    def avg_value(self) -> float:
        neighbors = self.model.grid.get_neighbors(self.pos, True)
        
        if len(neighbors) == 0:
            return 0

        total_value = sum([neighbor.value for neighbor in neighbors if type(neighbor) is Pheromone])
        
        return total_value / len(neighbors)

    def update_value(self) -> None:
        self.value = (1 - self.evaporation_rate) * self.value \
            + self.diffusion_rate * (self.avg_value - self.value)
        
    def step(self) -> None:
        self.update_value()
        # print(self)

        if self.value < 0.1:
            self.model.grid.remove_agent(self)
            self.model.scheduler.remove(self)
            return

        for pos in self.model.grid.iter_neighborhood(self.pos, True):
            if self.model.grid.is_cell_empty(pos):
                Pheromone.create(self.model,pos, self.value)
