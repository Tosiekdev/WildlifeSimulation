from .Animal import Animal


class Fox(Animal):

    def __init__(self,
        model,
        lifetime=4,
        consumption=5,
        speed=6,
        trace=10,
        view_range=135
    ):
        super().__init__(model.next_id(), model, lifetime, consumption, speed, trace, view_range)

    def step(self) -> None:
        self.random_move()
        print(self)
