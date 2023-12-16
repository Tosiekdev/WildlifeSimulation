from .Animal import Animal


class Wolf(Animal):

    def __init__(self, unique_id, model, lifetime=4, consumption=5, speed=6, trace=10, view_range=135):
        super().__init__(unique_id, model, lifetime, consumption, speed, trace, view_range)

    def __str__(self):
        return f"{self.pos}"

    def step(self) -> None:
        print(self)
