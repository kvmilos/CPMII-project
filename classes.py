import pygame
import pymunk
import math
import random


def generate_colours(num_colors):
    colors = []
    for _ in range(num_colors):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        colors.append((r, g, b, 255))
    return colors

class Constants:
    # class to store constants
    # width and height of the window
    WIDTH, HEIGHT = 800, 800

    N_ROBOTS = 10

    # movement and rotation speed
    MOVEMENT_SPEED = 200
    ROTATION_SPEED = 2
    ENEMY_SPEED = 100

    # visual field
    VISION_FIELD_ANGLE = 60
    VISION_FIELD_RANGE = 500

    # points
    POINTS_GAINED_PER_FOOD = 200
    POINTS_LOST_PER_TIME = 1
    PER_WHAT_TIME_POINTS_ARE_LOST = 2
    POINTS_LOST_PER_ENEMY = 50
    POINTS_LOST_PER_WALL = 5
    POINTS_LOST_PER_NOT_MOVING = 20

    # distance from window edges to place the walls
    WALLS_DISTANCE = 20

    # sizes
    ROBOT_SIZE = 30
    FOOD_SIZE = 10
    ENEMY_SIZE = 20

    # collision types
    ROBOT = 1
    WALL = 2
    FOOD = 3
    ENEMY = 4

    # masks
    ROBOT_MASK = 0b0001 
    WALL_MASK = 0b0010
    FOOD_MASK = 0b0100
    ENEMY_MASK = 0b1000
    
    # mapping of 'what' -> colours
    COLOURS = {
        2: (0, 0, 255, 255),
        3: (0, 255, 0, 255),
        4: (255, 0, 0, 255),
        0: (100, 100, 100, 255)
    }

    # walls around the window
    WALLS = [
        (WALLS_DISTANCE, WALLS_DISTANCE, WIDTH - WALLS_DISTANCE, WALLS_DISTANCE),
        (WALLS_DISTANCE, WALLS_DISTANCE, WALLS_DISTANCE, HEIGHT - WALLS_DISTANCE),
        (WALLS_DISTANCE, HEIGHT - WALLS_DISTANCE, WIDTH - WALLS_DISTANCE, HEIGHT - WALLS_DISTANCE),
        (WIDTH - WALLS_DISTANCE, WALLS_DISTANCE, WIDTH - WALLS_DISTANCE, HEIGHT - WALLS_DISTANCE)
    ]

    COLORS2 = generate_colours(N_ROBOTS).copy()

class Robot():
    # robot is a circle with a vision field, the main object in the simulation
    def __init__(self, name, space, position = (100, 100), size = Constants.ROBOT_SIZE, angle = 0, color = (50, 50, 200, 100), vision_field_angle = Constants.VISION_FIELD_ANGLE, vision_field_range = Constants.VISION_FIELD_RANGE):
        self.name = name
        # body is what is used to apply forces
        self.body = pymunk.Body(1, 1)
        self.body.position = position
        self.body.angle = math.radians(angle)
        self.space = space
        self.vision_angle = vision_field_angle
        self.vision_range = vision_field_range
        self.radius = size
        # shape is what is used to draw the robot
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.color = color
        self.body.mass = 1
        self.shape.collision_type = 1
        self.shape.filter = pymunk.ShapeFilter(categories=Constants.ROBOT_MASK, mask=Constants.WALL_MASK | Constants.FOOD_MASK | Constants.ENEMY_MASK)
        self.radars = []
        space.add(self.body, self.shape)

    def draw(self, window = None):
        # # function to draw both the robot, and its vision field
        self.window = window

        self.radars.clear()
        for i in range(int(self.body.angle - (self.vision_angle/2)), int(self.body.angle + (self.vision_angle/2)), 12):
            self.sense(i, self.space)
            
        for radar in self.radars:
            pos = radar[0]
            dist = radar[1]
            colour = Constants.COLOURS[radar[2]]
            radar.append(pos - self.body.position)
            #pygame.draw.line(window, colour, (self.body.position.x, self.body.position.y), (pos[0], pos[1]), 1)
            #pygame.draw.circle(window, colour, (int(pos[0]), int(pos[1])), 5)
        
        # draw space onto window
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(window))
        
        #return [(pos.x, pos.y, dist, what) for _, dist, what, pos in self.radars]

    def rotate(self, angle) -> None:
        # rotate the robot by angle
        self.body.angle = self.body.angle + math.radians(angle) * Constants.ROTATION_SPEED

    def move(self, dist) -> None:
        # apply force to the robot to move it
        force = dist * Constants.MOVEMENT_SPEED
        direction = pymunk.Vec2d(math.cos(self.body.angle), math.sin(self.body.angle))
        self.body.apply_force_at_world_point(direction * force, self.body.position)

    def sense(self, degree, space):
        # Detect objects within the robot's vision field
        length = 0
        detected = False

        end_x = int(self.body.position.x + math.cos(self.body.angle - math.radians(degree)) * self.vision_range)
        end_y = int(self.body.position.y + math.sin(self.body.angle - math.radians(degree)) * self.vision_range)

        query_info = space.segment_query_first(self.body.position, (end_x, end_y), 1, pymunk.ShapeFilter(mask=Constants.WALL_MASK | Constants.FOOD_MASK | Constants.ENEMY_MASK))
        if query_info:
            detected = True
            shape = query_info.shape
            x, y = query_info.point
            shape = query_info.shape
            what = shape.collision_type
            if what == 3 and shape.color != self.shape.color:
                what = 0
        else:
            what = 0
            x, y = end_x, end_y
            
        dist = int(math.sqrt((x - self.body.position.x) ** 2 + (y - self.body.position.y) ** 2))
        self.radars.append([(x, y), dist, what])
    
    def get_data(self):
        if self.radars == []:
            for i in range(int(self.body.angle - (self.vision_angle/2)), int(self.body.angle + (self.vision_angle/2)), 12):
                self.sense(i, self.space)
        distances = [None] * len(self.radars)
        objects = [None] * len(self.radars)
        #print("SELFRADARS:", len(self.radars))
        for i, radar in enumerate(self.radars):
            distances[i] = int(radar[1])
            objects[i] = int(radar[2])
        return objects


class Wall():
    # wall is a static segment
    def __init__(self, space, start_x, start_y, end_x, end_y, thickness=10):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (start_x, start_y), (end_x, end_y), thickness)
        self.shape.color = (0, 0, 255, 255)
        self.shape.elasticity = 0.00
        self.shape.collision_type = Constants.WALL
        self.shape.friction = 1.0
        space.add(self.body, self.shape)
        

class Food():
    def __init__(self, space, position, color, size = Constants.FOOD_SIZE):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position   
        self.shape = pymunk.Circle(self.body, size)
        self.shape.color = color
        self.shape.collision_type = Constants.FOOD
        # self.shape.filter = pymunk.ShapeFilter(mask=Constants.FOOD_MASK)
        space.add(self.body, self.shape)


class Enemy():
    def __init__(self, space, position, size = Constants.ENEMY_SIZE):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, size)
        self.shape.color = (255, 0, 0, 255)
        self.shape.collision_type = Constants.ENEMY
        # self.shape.filter = pymunk.ShapeFilter(mask=Constants.ENEMY_MASK)
        space.add(self.body, self.shape)