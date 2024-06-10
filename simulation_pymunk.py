import pymunk
import random
from classes import Robot, Wall, Constants, Food, Enemy
import neat

seed_value = 1

class Simulation():
    # class to create the simulation environment
    def __init__(self):
        self.points = []
        self.timer = 0
        self.timer2 = 0
        self.enemies = []
        #self.robot = Robot
        self.robots = []
        self.walls = []
        self.food_count = 0
        self.food = []
        self.robots_previous_positions = []

    def run(self, seed_value, n_robots):
        # function to run the simulation
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)
        self.space.iterations = 30
        self.seed = random.Random(seed_value)
        self.walls = self.spawn_random_walls()

        for cords in Constants.WALLS:
            wall = Wall(self.space, *cords)

        for i in range(0, n_robots):
            #color = Constants.COLORS2[i]
            self.points.append(0)
            self.spawn_robot(Constants.COLORS2[i])
        # spawn  random walls, initial food, and enemy 
        
        self.spawn_food(10)
        #self.spawn_enemy(10)

        # collision handlers
        # robot-food
        food_handler = self.space.add_collision_handler(Constants.ROBOT, Constants.FOOD)
        food_handler.begin = self.robot_eat_food

        # robot-enemy
        enemy_handler = self.space.add_collision_handler(Constants.ROBOT, Constants.ENEMY)
        enemy_handler.begin = self.robot_hit_enemy

        #robot-obstacles
        #wall_handler = self.space.add_collision_handler(Constants.ROBOT, Constants.WALL)
        #wall_handler.begin = self.robot_hit_wall
        
        #robot_rect = self.robot.get_rect(topleft = self.robot.body.position)

        return self.space

    def get_robots(self):
        return self.robots
    
    def spawn_robot(self, color):
        self.robots.append(Robot("robot", self.space, (Constants.WIDTH // 2, Constants.HEIGHT // 2), color=color))
        self.robots_previous_positions.append([(100, 100)])
        self.food.append([])

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
        #if len(self.food) == 0:
        #while True:
            for robot in self.robots:
                index = self.robots.index(robot)
                if self.food[index] == []:
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
                #Food(self.space, (x, y))
            #for robot in self.robots:
              #  index = self.robots.index(robot)
              #  if self.food[index] == []:
                        self.food[index].append(Food(self.space, (x, y), Constants.COLORS2[index]))
            #print(self.food[0])
                    

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
        index = 0
        food_shape = arbiter.shapes[1]
        for robot in self.robots:
            if robot.shape == arbiter.shapes[0]:
                index = self.robots.index(robot)
                #print(self.food[index])
                if robot.shape.color == food_shape.color and food_shape.body.position == self.food[index][0].body.position:
                    del self.food[index][0]
                    space.remove(food_shape, food_shape.body)
                    self.points[index] += Constants.POINTS_GAINED_PER_FOOD
       # if len(self.food) > 0:
          #  tmp = []
        #    for food in self.food:
          #      tmp.append(food[0].body.position)
          #  if food_shape.body.position in tmp:
            #    del self.food[tmp.index(food_shape.body.position)]

        
        # add a new food in a random position
        self.spawn_food(10)

        # increase the points
        self.points[index] += Constants.POINTS_GAINED_PER_FOOD
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

    def robot_hit_wall(self, arbiter, space, data):
         # Decrease points by 5
        #if self.points - 5 >= 0:
        self.points[self.robots.index[arbiter[0]]] -= 100
        #else:
         #   self.points = 0
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
            #if self.points - Constants.POINTS_LOST_PER_TIME >= 0:
            for robot in self.robots:
                index = self.robots.index(robot)
                #print(self.points[index])
                self.points[index] -= Constants.POINTS_LOST_PER_TIME
            #else:
                #self.points = 0
                tmp = []
                for j, radar in enumerate(self.robots[index].radars):
                    tmp.append(radar[2])
                if set(tmp) == {2}:
                    self.points[index] -= 1
                elif 3 in set(tmp):
                    self.points[index] += 1
                self.timer = 0

    def update_position(self, dt):
        self.timer2 += dt
        if self.timer2 >= Constants.PER_WHAT_TIME_POINTS_ARE_LOST/2:
            for robot in self.robots:
                index = self.robots.index(robot)
                self.robots_previous_positions[index].append(self.robots[index].body.position)
                self.timer2 = 0
                self.check_if_stuck(index)
                if len(self.robots_previous_positions[index]) == 5:
                    del self.robots_previous_positions[index][0]
            #print(self.robots_previous_positions)
            

    def check_if_stuck(self, id):
        if(len(set(self.robots_previous_positions[id])) == 1):
            self.points[id] -= Constants.POINTS_LOST_PER_NOT_MOVING