from typing import Any

import mesa

from .Wolf import Wolf


class SimulationModel(mesa.Model):
    """Application base model"""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.width = 282
        self.height = 282

        self.grid = mesa.space.MultiGrid(self.width, self.height, False)

        self.iterations = 10

        self.num_of_hares = 0
        self.num_of_wolves = 5

        self.scheduler = mesa.time.BaseScheduler(self)

        # for i in range(self.num_of_hares):
        #     hare = Hare()
        #     self.scheduler.add(hare)

        for i in range(self.num_of_wolves):
            wolf = Wolf(self.num_of_hares+i, self)
            self.scheduler.add(wolf)

            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(wolf, (x, y))

        self.step()

    def step(self):
        self.scheduler.step()

    def run(self):
        for i in range(self.iterations):
            self.step()
