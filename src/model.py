from typing import Any, Tuple
import mesa
import numpy as np
from .agents import *
from .environment.map import create_map, add_food_to_map
from .environment.map import create_map, add_food_to_map
from .agents.fox_habitat import FoxHabitat
from .agents.hare_habitat import HareHabitat
from .agents.hare_food import HareFood

from .agents.hare_food_factory import HareFoodFactory


class SimulationModel(mesa.Model):
    "A model for simulating Fox and Hare (predator-prey) ecosystem modelling."

    def __init__(
        self,
        one_week: int,
        initial_plant: int,
        initial_fox: int,
        initial_hare: int,
        initial_number_of_hares_habitats: int,
        initial_number_of_foxes_habitats: int,
        initial_food_amount: int,
        initial_food_frequency: int,
        initlal_fox_mating_season: int,
        initial_fox_min_mating_range: int,
        initial_fox_max_mating_range: int,
        initial_hare_mating_season: int,
        initial_hare_min_mating_range: int,
        initial_hare_max_mating_range: int,
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
        fox_lifetime: int,
        fox_consumption: int,
        fox_speed: int,
        fox_trace: float,
        fox_view_range: int,
        fox_view_angle: int,
        fox_smelling_range: int,
        fox_attack_range: int,
        *args: Any,
        **kwargs: Any
    ):
        super().__init__(*args, **kwargs)

        self.width = 40
        self.height = 40

        self.grid = mesa.space.MultiGrid(self.width, self.height, False)

        self.iterations = 100
        self.one_week = one_week

        self.num_of_hares = initial_hare
        self.num_of_foxes = initial_fox
        self.number_of_plant = initial_plant
        self.number_of_hares_habitats = initial_number_of_hares_habitats
        self.number_of_foxes_habitats = initial_number_of_foxes_habitats
        self.food_amount = initial_food_amount
        self.food_frequency = initial_food_frequency
        self.fox_mating_season = initlal_fox_mating_season
        self.fox_min_mating_range = initial_fox_min_mating_range
        self.fox_max_mating_range = initial_fox_max_mating_range
        self.hare_mating_season = initial_hare_mating_season
        self.hare_min_mating_range = initial_hare_min_mating_range
        self.hare_max_mating_range = initial_hare_max_mating_range
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
            "no_movement_duration": hare_no_movement_duration,
        }

        self.fox_params = {
            "lifetime": fox_lifetime,
            "consumption": fox_consumption,
            "speed": fox_speed,
            "trace": fox_trace,
            "view_range": fox_view_range,
            "view_angle": fox_view_angle,
            "smelling_range": fox_smelling_range,
            "attack_range": fox_attack_range,
        }

        self.fox_params = {
            "lifetime": fox_lifetime,
            "consumption": fox_consumption,
            "speed": fox_speed,
            "trace": fox_trace,
            "view_range": fox_view_range,
            "view_angle": fox_view_angle,
            "smelling_range": fox_smelling_range,
            "attack_range": fox_attack_range,
        }

        self.pheromone_params = {
            "evaporation_rate": pheromone_evaporation_rate,
            "diffusion_rate": pheromone_diffusion_rate,
        }

        self.scheduler = mesa.time.BaseScheduler(self)

        map = create_map(self.height, self.width)
        self.map = add_food_to_map(
            map, self.number_of_plant, self.number_of_foxes_habitats, self.number_of_hares_habitats
        )

        agent_mapping = {2: HareFood, 3: HareHabitat, 4: FoxHabitat}

        for (y, x), agent_type in np.ndenumerate(self.map):
            agent_class = agent_mapping.get(agent_type)
            if agent_class:
                if agent_class != HareFood:
                    (mating_season, mating_range) = (
                        self.fox_mating_season if agent_class == FoxHabitat else self.hare_mating_season,
                        (self.fox_min_mating_range, self.fox_max_mating_range)
                        if agent_class == FoxHabitat
                        else (self.hare_min_mating_range, self.hare_max_mating_range),
                    )
                    agent = agent_class(self, mating_season, mating_range)
                else:
                    agent = agent_class(self)
                self.scheduler.add(agent)
                self.grid.place_agent(agent, (x, self.height - 1 - y))
                if agent_class == HareHabitat or agent_class == FoxHabitat:
                    agent.init()

        HareFoodFactory(self, self.food_amount, self.food_frequency)
        self.running = True

    def step(self):
        self.scheduler.step()

    def run_model(self):
        for _ in range(self.iterations):
            self.step()
