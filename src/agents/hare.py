import math
from typing import List, Tuple
import mesa

from .hare_food import HareFood
from .pheromone import Pheromone
from .animal import Animal

class Hare(Animal):
    def __init__(self,
        model,
        lifetime=200,
        consumption=5,
        speed=6,
        trace=1,
        view_range=5,
        view_angle=350
    ):
        super().__init__(model, lifetime, consumption, speed, trace, view_range)
        self.view_angle = view_angle

    @staticmethod
    def create(model: mesa.Model, pos: Tuple[int, int]) -> None:
        hare = Hare(model)
        model.grid.place_agent(hare, pos)
        model.scheduler.add(hare)

    def leave_trace(self) -> None:
        """
        Leave a trace of pheromone.
        """
        neighbors = self.model.grid.get_neighbors(self.pos, False, True, 0)
        neighbors = [neighbor for neighbor in neighbors if type(neighbor) is Pheromone]

        if len(neighbors) == 0:
            Pheromone.create(self.model, self.pos, self.trace)
        else:
            pheromone = neighbors[0]
            pheromone.value = self.trace

    def find_food(self) -> List[HareFood]:
        """
        Find food in the view range.
        """
        neighbors = self.get_neighbors_within_angle(self.view_angle, self.view_range)
        neighbors = [neighbor for neighbor in neighbors if type(neighbor) is HareFood and not neighbor.eaten]

        if not neighbors:
            return None

        min_distance = float('inf')
        closest_neighbor = None

        for neighbor in neighbors:
            x, y = neighbor.pos
            distance = math.sqrt((x - self.pos[0])**2 + (y - self.pos[1])**2)
            if distance < min_distance:
                min_distance = distance
                closest_neighbor = neighbor

        return closest_neighbor

    def move(self, destination: Tuple[int, int]) -> None:
        """
        Move to the destination.
        """
        x, y = tuple(x-y for x, y in zip(destination, self.pos))
        if abs(x) > 1 or abs(y) > 1:
            x = min(1, x) if x > 0 else max(-1, x)
            y = min(1, y) if y > 0 else max(-1, y)
        next_move = (self.pos[0] + x, self.pos[1] + y)
        self.model.grid.move_agent(self, next_move)

    def eat_food(self) -> None:
        """
        Eat food.
        """
        neighbors = self.model.grid.get_neighbors(self.pos, False, True, 0)
        neighbors = [neighbor for neighbor in neighbors if type(neighbor) is HareFood and not neighbor.eaten]

        if len(neighbors) > 0:
            food = neighbors[0]
            print(food, food.eaten)
            food.eat_food()
            self.eaten += 1
        else:
            print('no food')

    def check_consumption(self) -> None:
        """
        Check if the hare has enough energy to survive.
        """
        if self.model.scheduler.steps > 0 and self.model.scheduler.steps % self.model.one_week == 0:
            check = self.consumption < self.eaten
            self.eaten = 0
            return check
        else:
            return True

    def step(self) -> None:
        if self.lifetime <= 0 or not self.check_consumption():
            self.remove()
        else:
            self.lifetime -= 1
            self.eat_food()
            food = self.find_food()
            if food:
                self.move(food.pos)
            else:
                self.random_move()
            self.leave_trace()
            print(self)
