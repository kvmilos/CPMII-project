import pymunk
import random
from classes import Robot, Wall, Constants, Food, Enemy
import neat

seed_value = 1

def generate_seeds(num_seeds=30):
    seeds = []
    for _ in range(num_seeds):
        seeds.append(random.randint(0, 1000))
    return seeds

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
        self.food = []
        self.food_number = []
        self.robots_previous_positions = []
        self.seed = generate_seeds()

    def run(self, seed_value, n_robots):
        # function to run the simulation
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)
        self.space.iterations = 30
        #self.seed = random.Random(seed_value)
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
        wall_handler = self.space.add_collision_handler(Constants.ROBOT, Constants.WALL)
        wall_handler.begin = self.robot_hit_wall
        
        #robot_rect = self.robot.get_rect(topleft = self.robot.body.position)

        return self.space

    def get_robots(self):
        return self.robots
    
    def spawn_robot(self, color):
        self.robots.append(Robot("robot", self.space, (Constants.WIDTH // 2, Constants.HEIGHT // 2), color=color))
        self.robots_previous_positions.append([(100, 100)])
        self.food.append([])
        self.food_number.append([1])

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
        for i, robot in enumerate(self.robots):
            if self.food[i] == []:
            # generate random position in between walls
                
                #print(self.seed[self.food_number[i][0]-1])
                seed_food = self.seed[self.food_number[i][0]-1]
                while True:
                    random.seed(seed_food)
                    seed_food += 1
                    x = random.randint(Constants.WALLS_DISTANCE + shift, Constants.WIDTH - Constants.WALLS_DISTANCE - shift)
                    y = random.randint(Constants.WALLS_DISTANCE + shift, Constants.HEIGHT - Constants.WALLS_DISTANCE - shift)
                    #print(x,y)
            # create a temp body to check for overlap
                    temp_body = pymunk.Body(body_type=pymunk.Body.STATIC)
                    temp_body.position = (x, y)
                    temp_shape = pymunk.Circle(temp_body, Constants.FOOD_SIZE)

            # check for overlap
                    overlap = self.space.shape_query(temp_shape)
                    if overlap != [] and overlap[0].shape.color != Constants.COLORS2[i] and overlap[0].shape.collision_type == Constants.FOOD:
                        overlap = False
            # if no overlap, add the food
                    if not overlap:
                #Food(self.space, (x, y))
            #for robot in self.robots:
              #  index = self.robots.index(robot)
              #  if self.food[index] == []:
                        self.food[i].append(Food(self.space, (x, y), Constants.COLORS2[i]))
            #print(self.food[0])
                        break
        #print(self.food_number)
    def get_space(self):
        return self.space
    
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
        for i, robot in enumerate(self.robots):
            if robot.shape == arbiter.shapes[0]:
                #print(self.food[index])
                if robot.shape.color == food_shape.color and food_shape.body.position == self.food[i][0].body.position:
                    del self.food[i][0]
                    space.remove(food_shape, food_shape.body)
                    self.points[i] += Constants.POINTS_GAINED_PER_FOOD
                    self.food_number[i][0] += 1
       # if len(self.food) > 0:
          #  tmp = []
        #    for food in self.food:
          #      tmp.append(food[0].body.position)
          #  if food_shape.body.position in tmp:
            #    del self.food[tmp.index(food_shape.body.position)]

        
        # add a new food in a random position
        self.spawn_food(10)
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
        robot_body = arbiter.shapes[0]
        for i, robot in enumerate(self.robots):
            if robot_body.color == robot.shape.color:
                self.points[i] -= Constants.POINTS_LOST_PER_WALL
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
            for i in range(0, len(self.robots)):
                self.points[i] -= Constants.POINTS_LOST_PER_TIME
                tmp = []
                for j, radar in enumerate(self.robots[i].radars):
                    tmp.append(radar[2])
                if set(tmp) == {2}:
                    self.points[i] -= 1
                elif 3 in set(tmp):
                    self.points[i] += 1
                self.timer = 0

    def update_position(self, dt):
        self.timer2 += dt
        if self.timer2 >= Constants.PER_WHAT_TIME_POINTS_ARE_LOST/2:
            for i in range(0, len(self.robots)):
                self.robots_previous_positions[i].append(self.robots[i].body.position)
                self.timer2 = 0
                self.check_if_stuck(i)
                if len(self.robots_previous_positions[i]) == 5:
                    del self.robots_previous_positions[i][0]

    def check_if_stuck(self, id):
        if(len(set(self.robots_previous_positions[id])) == 1):
            self.points[id] -= Constants.POINTS_LOST_PER_NOT_MOVING