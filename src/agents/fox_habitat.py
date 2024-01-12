from typing import Tuple
import mesa
import numpy as np
from importlib import import_module

class FoxHabitat(mesa.Agent):
    """
    Class representing fox habitat area.
        
    """
    def __init__(self, model: mesa.Model, mating_season:int = 365, mating_range: Tuple[int, int] = (1,11)) -> None:
        super().__init__(model.next_id(), model)
        self.mating_season = mating_season
        self.model = model
        self.mating_range = mating_range
        self.initial_mating_season = mating_season

    def init(self) -> None:
        """
        Function called manually after the agent is created.
        """
        fox = import_module("src.agents.fox")
        for _ in range(self.model.num_of_foxes):
            fox.Fox.create(self.model, self, True)
            
    def step(self) -> None:
        """
        Method called in every step of the simulation.
        It creates few foxes in the habitat every mating season.
        """
        fox = import_module("src.agents.fox")
        if self.mating_season == 0:
            self.mating_season = self.initial_mating_season
            self.model.num_of_foxes += 1
            number_of_foxes_to_create = np.random.randint(self.mating_range[0], self.mating_range[1])
            for _ in range(number_of_foxes_to_create):
                fox.Fox.create(self.model, self, False)
        else:
            self.mating_season -= 1

