import mesa
import numpy as np
from .hare_food import HareFood

class HareFoodFactory(mesa.Agent):
    
    def __init__(self, model: mesa.Model, food_amount: int = 25, frequency: int = 10):
        """
        Class responsible for creating food for Hares.

        @param: model - Mesa model.
        @param: food_amount - amount of food created.
        @param: frequency - frequency of food creation.
        """
        super().__init__(model.next_id(), model)
        self.food_amount: int = food_amount
        self.iteration = 0
        self.frquency = frequency
        self.model.scheduler.add(self)
        
    def step(self) -> None:
        """
        Performs a single of agent.
        Create number of food in given frequency

        """
        self.iteration += 1
        if self.iteration == self.frquency:
            self.iteration = 0
            for _ in range(self.food_amount):
                possible_positions = np.where((self.model.map == 0) | (self.model.map == 2))
                random_index = np.random.choice(len(possible_positions[0]), 1, replace=False)
                x = int(possible_positions[0][random_index])
                y = int(possible_positions[1][random_index])
                HareFood.create(self.model, (y, self.model.height - 1 - x))
    
    