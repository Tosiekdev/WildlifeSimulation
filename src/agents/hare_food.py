from typing import Tuple
import mesa


class HareFood(mesa.Agent):
    def __init__(self, model: mesa.Model, lifetime:int = 350) -> None:
        """
        Class responsible for feeding Hares.

        @param: mmodel - Mesa model .
        """
        super().__init__(model.next_id(), model)
        self.lifetime: int = lifetime
        self.eaten: bool = False

    def step(self) -> None:
        """
        Performs a single of agent.

        """
        if self.lifetime <= 0:
            self.model.grid.remove_agent(self)
            self.model.scheduler.remove(self)
        else:
            self.lifetime -= 1

    def eat_food(self) -> None:
        """
        Changes the parameter eaten to True.

        """
        self.eaten = True

    @staticmethod
    def create(model: mesa.Model, pos: Tuple[int, int], food_lifetime: int) -> None:
        """
        Creates hare food.

        @param: model - Mesa model.
        @param: pos - position of hare food.

        """
        hare_food = HareFood(model, food_lifetime)
        model.grid.place_agent(hare_food, pos)
        model.scheduler.add(hare_food)
