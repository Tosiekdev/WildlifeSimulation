import mesa


class Animal(mesa.Agent):
    """Animal interface"""

    def __init__(self, unique_id, model, lifetime, consumption, speed, trace, view_range):
        super().__init__(unique_id, model)
        self.lifetime = lifetime
        self.consumption = consumption
        self.speed = speed
        self.trace = trace
        self.view_range = view_range


    def step(self) -> None:
        pass
