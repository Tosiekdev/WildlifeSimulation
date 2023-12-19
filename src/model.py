from typing import Any
import mesa
from .agents import *

class SimulationModel(mesa.Model):
    """Application base model"""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.width = 20
        self.height = 20

        self.grid = mesa.space.MultiGrid(self.width, self.height, False)

        self.iterations = 10

        self.num_of_hares = 10
        self.num_of_foxes = 1

        self.scheduler = mesa.time.BaseScheduler(self)

        for _ in range(self.num_of_foxes):
            fox = Fox(self)
            self.scheduler.add(fox)

            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(fox, (x, y))

        for _ in range(self.num_of_hares):
            hare = Hare(self)
            self.scheduler.add(hare)

            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(hare, (x, y))

        self.running = True

    def step(self):
        self.scheduler.step()

    def run_model(self):
        for _ in range(self.iterations):
            self.step()
