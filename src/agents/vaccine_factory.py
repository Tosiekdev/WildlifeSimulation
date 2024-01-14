from typing import Tuple
import mesa
import numpy as np

class VaccineFactory(mesa.Agent):
    def __init__(self, model: mesa.Model, vaccine_amount: int = 25, vaccine_frequency: int = 10, vaccine_effectiveness: int = 20, vaccine_lifetime: int = 50):
        """
        Class responsible for creating vaccine for Hares.

        @param: model - Mesa model.
        @param: vaccine_amount - amount of vaccine created.
        @param: vaccine_frequency - vaccine_frequency of vaccine creation.
        """
        super().__init__(model.next_id(), model)
        self.vaccine_amount= vaccine_amount
        self.iteration = 0
        self.frquency = vaccine_frequency
        self.model.scheduler.add(self)
        self.vaccine_efeectivness = vaccine_effectiveness
        self.vaccine_lifetime = vaccine_lifetime

    def step(self) -> None:
        """
        Performs a single of agent.
        Create number of vaccine in given vaccine_frequency

        """
        self.iteration += 1
        if self.iteration == self.frquency:
            self.iteration = 0
            for _ in range(self.vaccine_amount):
                height, width = self.model.map.shape
                x = np.random.randint(0, width)
                y = np.random.randint(0, height)
                Vaccine.create(self.model, (y, self.model.height - 1 - x), self.vaccine_lifetime, self.vaccine_efeectivness)
                
class Vaccine(mesa.Agent):
    def __init__(self, model: mesa.Model, lifetime:int = 50, effectivness:int = 20):
        """
        Class representing vaccine.

        @param: model - Mesa model.
        """
        super().__init__(model.next_id(), model)
        self.lifetime: int = lifetime
        self.effectivness: int = effectivness
        
    def remove(self) -> None:
        """
        Removes vaccine.

        """
        self.model.grid.remove_agent(self)
        self.model.scheduler.remove(self)
        
    def step(self) -> None:
        """
        Performs a single of agent.

        """
        if self.lifetime <= 0:
            self.remove()
        else:
            self.lifetime -= 1
    
    @staticmethod
    def create(model: mesa.Model, pos: Tuple[int, int], lifetime, effectivness) -> None:
        """
        Creates vaccine.

        @param: model - Mesa model.
        @param: pos - position of vaccine.

        """
        vaccine = Vaccine(model, lifetime, effectivness)
        model.grid.place_agent(vaccine, pos)
        model.scheduler.add(vaccine)
    
    

