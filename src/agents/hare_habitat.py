from typing import Tuple
import mesa
import numpy as np

from .hare import Hare


class HareHabitat(mesa.Agent):
    """
    Class representing hare habitat area.
    
    """
    
    def __init__(self, model: mesa.Model,mating_season: int = 100, mating_range: Tuple[int,int]=(3, 5)) -> None:
        super().__init__(model.next_id(), model)
        self.mating_season = mating_season
        self.model = model
        self.mating_range = mating_range
    
    def init(self) -> None:
        """
        Function called manually after the agent is created.
        
        """
        for _ in range(self.model.num_of_hares):
            Hare.create(self.model, self.pos)
    
    def step(self) -> None:
        """
        
        Method called in every step of the simulation.
        It creates few hares in the habitat every mating season.
        
        """
        if self.mating_season == 0:
            self.mating_season = 100
            self.model.num_of_hares += 1
            number_of_hares_to_create = np.random.randint(self.mating_range[0], self.mating_range[1])
            for _ in range(number_of_hares_to_create):
                Hare.create(self.model, self.pos)
        else:
            self.mating_season -= 1
    
