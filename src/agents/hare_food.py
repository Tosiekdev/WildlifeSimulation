import mesa


class HareFood(mesa.Agent):
    def __init__(self, model: mesa.Model) -> None:
        """
        Class responsible for feeding Hares.

        @param: mmodel - Mesa model .
        """
        super().__init__(model.next_id(), model)
        self.lifetime: int = 200
        self.eaten: bool = False

    def step(self) -> None:
        """
        Performs a single of agent.

        """
        pass

    def eat_food(self) -> None:
        """
        Changes the parameter eaten to True.

        """
        self.eaten = True
