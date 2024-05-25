import pymunk
import random
from classes import Robot, Wall, Constants, Food, Enemy

class Simulation():
    # class to create the simulation environment
    def __init__(self):
        self.points = 0
        self.timer = 0
        self.enemies = []


    def run(self):
        # function to run the simulation
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)
        self.space.iterations = 30

        self.robot = Robot("robot", self.space, (Constants.WIDTH // 2, Constants.HEIGHT // 2))

        for cords in Constants.WALLS:
            wall = Wall(self.space, *cords)

        # spawn  random walls, initial food, and enemy 
        self.spawn_random_walls()
        self.spawn_food(10)
        self.spawn_enemy(10)

        # collision handlers
        # robot-food
        food_handler = self.space.add_collision_handler(Constants.ROBOT, Constants.FOOD)
        food_handler.begin = self.robot_eat_food

        # robot-enemy
        enemy_handler = self.space.add_collision_handler(Constants.ROBOT, Constants.ENEMY)
        enemy_handler.begin = self.robot_hit_enemy

        return self.space, self.robot

    def spawn_random_walls(self, n=5):
        # function to add random walls
        for _ in range(n):
            start_x = random.randint(Constants.WALLS_DISTANCE, Constants.WIDTH - Constants.WALLS_DISTANCE)
            start_y = random.randint(Constants.WALLS_DISTANCE, Constants.HEIGHT - Constants.WALLS_DISTANCE)
            end_x = random.randint(start_x - 50, start_x + 50)
            end_y = random.randint(start_y - 50, start_y + 50)
            Wall(self.space, start_x, start_y, end_x, end_y, thickness = 8)

    def spawn_food(self, shift):
        # function to add random food
        while True:
            # generate random position in between walls
            x = random.randint(Constants.WALLS_DISTANCE + shift, Constants.WIDTH - Constants.WALLS_DISTANCE - shift)
            y = random.randint(Constants.WALLS_DISTANCE + shift, Constants.HEIGHT - Constants.WALLS_DISTANCE - shift)

            # create a temp body to check for overlap
            temp_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            temp_body.position = (x, y)
            temp_shape = pymunk.Circle(temp_body, Constants.FOOD_SIZE)

            # check for overlap
            overlap = self.space.shape_query(temp_shape)

            # if no overlap, add the food
            if not overlap:
                Food(self.space, (x, y))
                break

    def spawn_enemy(self, shift):
        # function to add random enemy
        while True:
            # generate random position in between walls
            x = random.randint(Constants.WALLS_DISTANCE + shift, Constants.WIDTH - Constants.WALLS_DISTANCE - shift)
            y = random.randint(Constants.WALLS_DISTANCE + shift, Constants.HEIGHT - Constants.WALLS_DISTANCE - shift)

            if (abs(x - self.robot.body.position.x) > 100) or (abs(y - self.robot.body.position.y) > 100):
                # create a temp body to check for overlap
                temp_body = pymunk.Body(body_type=pymunk.Body.STATIC)
                temp_body.position = (x, y)
                temp_shape = pymunk.Circle(temp_body, Constants.ENEMY_SIZE)
            else:
                continue

            # check for overlap
            overlap = self.space.shape_query(temp_shape)

            # if no overlap, add the enemy
            if not overlap:
                enemy = Enemy(self.space, (x, y))
                self.enemies.append(enemy)
                break

    def robot_eat_food(self, arbiter, space, data):
        # remove the food from the space
        food_shape = arbiter.shapes[1]
        space.remove(food_shape, food_shape.body)

        # add a new food in a random position
        self.spawn_food(10)

        # increase the points
        self.points += Constants.POINTS_GAINED_PER_FOOD

        return False

    def robot_hit_enemy(self, arbiter, space, data):
        # Decrease points by 50
        if self.points - 50 >= 0:
            self.points -= 50
        else:
            self.points = 0

        # Bounce the robot and enemy off each other
        robot_body = arbiter.shapes[0].body
        enemy_body = arbiter.shapes[1].body

        # Calculate the bounce direction and apply impulse
        direction = robot_body.position - enemy_body.position
        direction = direction.normalized() * 20

        robot_body.apply_impulse_at_local_point(direction)
        enemy_body.apply_impulse_at_local_point(-direction)

        return True

    def move_enemies(self):
        for enemy in self.enemies:
            direction = self.robot.body.position - enemy.body.position
            if direction.length > 0:
                direction = direction.normalized() * Constants.ENEMY_SPEED
                enemy.body.velocity = direction


    def update_points(self, dt):
        # decrease a point every X seconds
        self.timer += dt
        if self.timer >= Constants.PER_WHAT_TIME_POINTS_ARE_LOST:
            if self.points - Constants.POINTS_LOST_PER_TIME >= 0:
                self.points -= Constants.POINTS_LOST_PER_TIME
            else:
                self.points = 0
            self.timer = 0