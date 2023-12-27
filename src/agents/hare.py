from enum import Enum
from typing import Tuple, Union
import math
import mesa


from .fox import Fox
from .sound import Sound
from .hare_food import HareFood
from .pheromone import Pheromone
from .animal import Animal, ViewDirection

distance = lambda p1, p2: math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) 
def get_surrounding_points(position: Tuple[int, int], radius: int = 1):
    x, y = position
    surroundings = []

    # Define offsets for surrounding points within the given radius
    offsets = [(i, j) for i in range(-radius, radius+1) for j in range(-radius, radius+1)]

    for offset in offsets:
        new_x = x + offset[0]
        new_y = y + offset[1]
        surroundings.append((new_x, new_y))

    return surroundings

class HareStatus(Enum):
    NORMAL = 0
    SPRINTING = 1
    NO_MOVEMENT = 2

class Hare(Animal):
    def __init__(self,
        model,
        lifetime=200,
        consumption=5,
        speed=2,
        trace=1,
        view_range=5,
        view_angle=350,
        hearing_range=20,
        sprint_speed=4,
        sprint_duration=10,
        sprint_cool_down=10,
        sprint_distance=4,
        no_movement_distance=8,
        no_movement_duration=10
    ):
        super().__init__(model, lifetime, consumption, speed, trace, view_range, view_angle)
        self.hearing_range = hearing_range
        self.sprint_speed = sprint_speed
        self.sprint_duration = sprint_duration
        self.sprint_cool_down = sprint_cool_down
        self.sprint_distance = sprint_distance
        self.no_movement_distance = no_movement_distance
        self.no_movement_duration = no_movement_duration
        self.status = HareStatus.NORMAL
        self.iteration = 0
        self.cool_down_iteration = 0

    @staticmethod
    def create(model: mesa.Model, pos: Tuple[int, int]) -> None:
        hare = Hare(model, **model.hare_params)
        model.grid.place_agent(hare, pos)
        model.scheduler.add(hare)

    def leave_trace(self) -> None:
        """
        Leave a trace of pheromone.
        """
        neighbors = self.model.grid[self.pos]
        neighbors = [neighbor for neighbor in neighbors if type(neighbor) is Pheromone]

        if len(neighbors) == 0:
            Pheromone.create(self.model, self.pos, self.trace)
        else:
            pheromone = neighbors[0]
            pheromone.value = self.trace

    def listen(self) -> dict:
        """
        Listen to the sound in the hearing range.
        """
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.hearing_range
        )
        sound = {neighbor.pos: neighbor.force for neighbor in neighbors if type(neighbor) is Sound}

        return sound

    def find_food(self) -> Union[Tuple[int, int], None]:
        """
        Find food in the view range.
        """
        neighbors = self.get_neighbors_within_angle()
        sound = self.listen()
        food = [neighbor.pos for neighbor in neighbors if type(neighbor) is HareFood and not neighbor.eaten]

        if not food:
            return None
        r = self.random_movement()
        food.append(r)

        min_distance = float('inf')
        closest_food_pos = None

        for f in food:
            dist = distance(f, self.pos) + sum([sound.get(pos, 0) for pos in get_surrounding_points(f)]) * Sound.FORCE
            if r == f:
                dist += self.speed * math.sqrt(2)
            if dist < min_distance:
                min_distance = dist
                closest_food_pos = f
        return closest_food_pos

    def move(self, destination: Tuple[int, int]) -> None:
        """
        Move to the destination.
        """

        x, y = tuple(x-y for x, y in zip(destination, self.pos))
        if abs(x) > self.speed or abs(y) > self.speed:
            x = min(self.speed, x) if x > 0 else max(-1 * self.speed, x)
            y = min(self.speed, y) if y > 0 else max(-1 * self.speed, y)
        next_move = (self.pos[0] + x, self.pos[1] + y)

        # Change view direction
        if next_move[0] > self.pos[0]:
            if next_move[1] > self.pos[1]:
                self.view_direction = ViewDirection.BOTTOM_RIGHT
            elif next_move[1] < self.pos[1]:
                self.view_direction = ViewDirection.TOP_RIGHT
            else:
                self.view_direction = ViewDirection.RIGHT
        elif next_move[0] < self.pos[0]:
            if next_move[1] > self.pos[1]:
                self.view_direction = ViewDirection.BOTTOM_LEFT
            elif next_move[1] < self.pos[1]:
                self.view_direction = ViewDirection.TOP_LEFT
            else:
                self.view_direction = ViewDirection.LEFT
        else:
            if next_move[1] > self.pos[1]:
                self.view_direction = ViewDirection.BOTTOM
            elif next_move[1] < self.pos[1]:
                self.view_direction = ViewDirection.TOP

        self.model.grid.move_agent(self, next_move)

    def eat_food(self) -> None:
        """
        Eat food.
        """
        neighbors = self.model.grid[self.pos]
        neighbors = [neighbor for neighbor in neighbors if type(neighbor) is HareFood and not neighbor.eaten]

        if len(neighbors) > 0:
            food = neighbors[0]
            food.eat_food()
            self.eaten += 1
        else:
            print('no food')

    def check_consumption(self) -> None:
        """
        Check if the hare has enough energy to survive.
        """
        if self.model.scheduler.steps > 0 and self.model.scheduler.steps % self.model.one_week == 0:
            check = self.consumption <= self.eaten
            self.eaten = 0
            return check
        else:
            return True

    def check_threats(self) -> float:
        """
        Check if there are any threats in the view range.
        """
        neighbors = self.get_neighbors_within_angle()
        threats = [distance(neighbor.pos, self.pos) for neighbor in neighbors if type(neighbor) is Fox]

        return 0 if len(threats) < 1 else min(threats)

    def random_movement(self) -> None:
        """
        Step one cell in any allowable direction.
        """
        current_speed = self.sprint_speed if self.status == HareStatus.SPRINTING else self.speed
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            radius=current_speed
        )

        # Find the next move with the least sound.
        sound = self.listen()
        sound_values = map(lambda x: sound.get(x, 0), next_moves)
        min_value = min(sound_values)
        next_moves = [move for move in next_moves if sound.get(move, 0) == min_value]
        next_move = self.random.choice(next_moves)

        return next_move

    def step(self) -> None:
        if self.lifetime <= 0 or not self.check_consumption():
            self.remove()
        else:
            self.lifetime -= 1
            threats = self.check_threats()
            match self.status:
                case HareStatus.NORMAL if threats > self.sprint_distance:
                    self.iteration = 1
                    self.status = HareStatus.NO_MOVEMENT
                case HareStatus.NORMAL if self.cool_down_iteration == 0 and threats < self.sprint_distance:
                    self.iteration = 1
                    self.status = HareStatus.SPRINTING
                    self.move(self.random_movement())
                case HareStatus.NORMAL:
                    self.eat_food()
                    food_pos = self.find_food()
                    if food_pos:
                        self.move(food_pos)
                    else:
                        self.move(self.random_movement())
                case HareStatus.SPRINTING if self.iteration < self.sprint_duration:
                    self.iteration += 1
                    self.move(self.random_movement())
                case HareStatus.SPRINTING:
                    self.status = HareStatus.NORMAL
                    self.cool_down_iteration = self.sprint_cool_down
                    self.move(self.random_movement())
                case HareStatus.NO_MOVEMENT if self.cool_down_iteration == 0 and threats < self.sprint_distance:
                    self.iteration = 1
                    self.status = HareStatus.SPRINTING
                    self.move(self.random_movement())
                case HareStatus.NO_MOVEMENT if self.iteration < self.no_movement_duration:
                    self.iteration += 1
                case HareStatus.NO_MOVEMENT:
                    self.status = HareStatus.NORMAL
                    self.move(self.random_movement())

            self.leave_trace()
            print(self)
