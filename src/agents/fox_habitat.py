from typing import Tuple
import mesa
import numpy as np
from .fox import Fox

class FoxHabitat(mesa.Agent):
    """
    Class representing fox habitat area.
        
    """
    def __init__(self, model: mesa.Model, mating_season:int = 10, mating_range: Tuple[int, int] = (1,11)) -> None:
        super().__init__(model.next_id(), model)
        self.mating_season = mating_season
        self.model = model
        self.mating_range = mating_range

    def init(self) -> None:
        for _ in range(self.model.num_of_hares):
            Fox.create(self.model, self.pos)
            
    def step(self) -> None:
        """
        Method called in every step of the simulation.
        It creates few foxes in the habitat every mating season.
        """
        if self.mating_season == 0:
            self.mating_season = 365
            self.model.num_of_foxes += 1
            number_of_foxes_to_create = np.random.randint(self.mating_range[0], self.mating_range[1])
            for _ in range(number_of_foxes_to_create):
                Fox.create(self.model, self.pos)
        else:
            self.mating_season -= 1