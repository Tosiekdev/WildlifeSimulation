from typing import Any, Tuple
import mesa
import numpy as np

from .agents.vaccine_factory import VaccineFactory
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
        food_amount: int,
        food_frequency: int,
        food_lifetime: int,
        fox_mating_season: int,
        fox_min_mating_range: int,
        fox_max_mating_range: int,
        hare_mating_season: int,
        hare_min_mating_range: int,
        hare_max_mating_range: int,
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
        fox_sprint_speed: int,
        fox_sneak_speed: int,
        vaccine_amount: int,
        vaccine_frequency: int,
        vaccine_lifetime: int,
        vaccine_effectiveness: int,
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
            "sprint_speed": fox_sprint_speed,
            "sneak_speed": fox_sneak_speed,
        }

        self.pheromone_params = {
            "evaporation_rate": pheromone_evaporation_rate,
            "diffusion_rate": pheromone_diffusion_rate,
        }
        self.fox_habitat_params = {
            "mating_season": fox_mating_season,
            "mating_range": (fox_min_mating_range, fox_max_mating_range),
        }
        self.hare_habitar_params = {
            "mating_season": hare_mating_season,
            "mating_range": (hare_min_mating_range, hare_max_mating_range),
        }
        self.hare_food_factory_params = {
            "food_amount": food_amount,
            "frequency": food_frequency,
            "food_lifetime": food_lifetime,
        }
        self.vaccine_factory_params = {
            "vaccine_amount": vaccine_amount,
            "vaccine_frequency": vaccine_frequency,
            "vaccine_effectiveness": vaccine_effectiveness,
            "vaccine_lifetime": vaccine_lifetime,
        }

    
        self.scheduler = mesa.time.BaseScheduler(self)
        self.datacollector = mesa.datacollection.DataCollector(
            model_reporters={
                "agent_count": lambda m: m.scheduler.get_agent_count(),
                "Hare": lambda m: len(list(filter(lambda a: type(a) is Hare, m.scheduler.agents))),
                "Fox": lambda m: len(list(filter(lambda a: type(a) is Fox, m.scheduler.agents))),
            }
        )

        map = create_map(self.height, self.width)
        self.map = add_food_to_map(
            map, self.number_of_plant, self.number_of_foxes_habitats, self.number_of_hares_habitats
        )

        agent_mapping = {2: HareFood, 3: HareHabitat, 4: FoxHabitat}

        for (y, x), agent_type in np.ndenumerate(self.map):
            agent_class = agent_mapping.get(agent_type)
            if agent_class:
                if agent_class != HareFood:
                    params = self.fox_habitat_params if agent_class == FoxHabitat else self.hare_habitar_params
                    agent = agent_class(self,**params)
                else:
                    agent = agent_class(self)
                self.scheduler.add(agent)
                self.grid.place_agent(agent, (x, self.height - 1 - y))
                if agent_class == HareHabitat or agent_class == FoxHabitat:
                    agent.create_animals()

        HareFoodFactory(self,**self.hare_food_factory_params)
        VaccineFactory(self, **self.vaccine_factory_params)
        self.running = True

    def step(self):
        self.datacollector.collect(self)
        self.datacollector.get_model_vars_dataframe().to_csv("data.csv")
        self.scheduler.step()

    def run_model(self):
        for _ in range(self.iterations):
            self.step()
