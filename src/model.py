from typing import Any
import mesa
from .agents import *
from.environment.map import create_map, add_food_to_map
from .agents.fox_habitat import FoxHabitat
from .agents.hare_habitat import HareHabitat
from .agents.hare_food import HareFood

class SimulationModel(mesa.Model):
    """Application base model"""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.width = 20
        self.height = 20
        self.number_of_plant = 60

        self.grid = mesa.space.MultiGrid(self.width, self.height, False)

        self.iterations = 10

        self.num_of_hares = 10
        self.num_of_foxes = 10

        self.scheduler = mesa.time.BaseScheduler(self)

        pre_map = create_map()
        map = add_food_to_map(pre_map, self.number_of_plant, 3, 3)
        for y in reversed(range(self.height)):
            for x in range(self.width):
                if map[y][x] == 2:
                    food = HareFood(self)
                    self.scheduler.add(food)
                    self.grid.place_agent(food, (x, self.height - 1 - y))
                elif map[y][x] == 3:
                    hare_habitat = HareHabitat(self)
                    self.scheduler.add(hare_habitat)
                    self.grid.place_agent(hare_habitat, (x, self.height - 1 - y))
                elif map[y][x] == 4:
                    fox_habitat = FoxHabitat(self)
                    self.scheduler.add(fox_habitat)
                    self.grid.place_agent(fox_habitat, (x, self.height - 1 - y))

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
