from typing import Any
import mesa
from .agents import *
from.environment.map import create_map, add_food_to_map
from .agents.fox_habitat import FoxHabitat
from .agents.hare_habitat import HareHabitat
from .agents.hare_food import HareFood

class SimulationModel(mesa.Model):
    "A model for simulating Fox and Hare (predator-prey) ecosystem modelling."

    def __init__(self,
            one_week: int,
            initial_plant: int,
            initial_fox: int,
            initial_hare: int,
            hare_lifetime: int,
            hare_consumption: int,
            hare_speed: int,
            hare_trace: float,
            hare_view_range: int,
            hare_view_angle: int,
            hare_hearing_range: int,
            hare_sprint_speed: int,
            hare_sprint_duration: int,
            hare_sprint_cool_down: int,
            hare_sprint_distance: int,
            hare_no_movement_distance: int,
            hare_no_movement_duration: int,
            pheromone_evaporation_rate: float,
            pheromone_diffusion_rate: float,
            *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.width = 20
        self.height = 20

        self.grid = mesa.space.MultiGrid(self.width, self.height, False)

        self.iterations = 100
        self.one_week = one_week
        
        self.num_of_hares = initial_hare
        self.num_of_foxes = initial_fox
        self.number_of_plant = initial_plant

        self.hare_params = {
            "lifetime": hare_lifetime,
            "consumption": hare_consumption,
            "speed": hare_speed,
            "trace": hare_trace,
            "view_range": hare_view_range,
            "view_angle": hare_view_angle,
            "hearing_range": hare_hearing_range,
            "sprint_speed": hare_sprint_speed,
            "sprint_duration": hare_sprint_duration,
            "sprint_cool_down": hare_sprint_cool_down,
            "sprint_distance": hare_sprint_distance,
            "no_movement_distance": hare_no_movement_distance,
            "no_movement_duration": hare_no_movement_duration
        }

        self.pheromone_params = {
            "evaporation_rate": pheromone_evaporation_rate,
            "diffusion_rate": pheromone_diffusion_rate
        }

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
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            Fox.create(self, (x, y))

        for _ in range(self.num_of_hares):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            Hare.create(self, (x, y))

        self.running = True

    def step(self):
        self.scheduler.step()

    def run_model(self):
        for _ in range(self.iterations):
            self.step()
