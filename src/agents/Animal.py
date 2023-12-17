from abc import ABC, abstractmethod 
import mesa


class Animal(mesa.Agent, ABC):
    """Animal interface"""

    def __init__(
        self,
        unique_id: int,
        model: mesa.Model,
        lifetime: int,
        consumption: int,
        speed: int,
        trace: int,
        view_range: int
    ):
        super().__init__(unique_id, model)
        self.lifetime = lifetime
        self.consumption = consumption
        self.speed = speed
        self.trace = trace
        self.view_range = view_range

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.pos}"

    @abstractmethod
    def step(self) -> None:
        """
        An Animal step. Move, eat, etc.
        """
        pass

    def random_move(self) -> None:
        """
        Step one cell in any allowable direction.
        """

        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, True)
        next_move = self.random.choice(next_moves)

        # Now move:
        self.model.grid.move_agent(self, next_move)
