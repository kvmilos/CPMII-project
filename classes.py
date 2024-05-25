import pygame
import pymunk
import math


class Constants:
    # class to store constants
    # width and height of the window
    WIDTH, HEIGHT = 800, 800

    # walls around the window
    WALLS = [
        (20, 20, WIDTH - 20, 20),
        (20, 20, 20, HEIGHT - 20),
        (20, HEIGHT - 20, WIDTH - 20, HEIGHT - 20),
        (WIDTH - 20, 20, WIDTH - 20, HEIGHT - 20)
    ]

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
        "wall": (0, 0, 255, 255),
        "food": (0, 255, 0, 255),
        "enemy": (255, 0, 0, 255),
        "nothing": (100, 100, 100, 255)
    }


class Robot():
    # robot is a circle with a vision field, the main object in the simulation
    def __init__(self, name, space, position = (100, 100), size = 30, angle = 0, color = (50, 50, 200, 100), vision_field_angle = 90, vision_field_range = 400):
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
        self.shape.filter = pymunk.ShapeFilter(categories=Constants.ROBOT_MASK)
        self.radars = []
        space.add(self.body, self.shape)

    def draw(self, window = None):
        # # function to draw both the robot, and its vision field
        self.window = window

        self.radars.clear()
        for i in range(int(self.body.angle - (self.vision_angle//2)), int(self.body.angle + (self.vision_angle//2)), 5):
            self.sense(i, self.space)

        for radar in self.radars:
            pos = radar[0]
            dist = radar[1]
            colour = Constants.COLOURS[radar[2]]
            pygame.draw.line(window, colour, (self.body.position.x, self.body.position.y), (pos[0], pos[1]), 1)
            pygame.draw.circle(window, colour, (int(pos[0]), int(pos[1])), 5)
        
        # draw space onto window
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(window))
        return self.window

    def rotate(self, angle) -> None:
        # rotate the robot by angle
        self.body.angle = self.body.angle + math.radians(angle)

    def move(self, dist) -> None:
        # apply force to the robot to move it
        force = dist * 100
        direction = pymunk.Vec2d(math.cos(self.body.angle), math.sin(self.body.angle))
        self.body.apply_force_at_world_point(direction * force, self.body.position)

    def sense(self, degree, space):
        # Detect objects within the robot's vision field
        length = 0
        detected = False
        x = int(self.body.position.x)
        y = int(self.body.position.y)

        end_x = int(self.body.position.x + math.cos(self.body.angle - math.radians(degree)) * self.vision_range)
        end_y = int(self.body.position.y + math.sin(self.body.angle - math.radians(degree)) * self.vision_range)

        # # Keep sensing as long as the length is less than vision range and the coordinates are within screen bounds
        # while (0 <= x < Constants.WIDTH) and (0 <= y < Constants.HEIGHT) and not detected and length < self.vision_range:
        #     length += 1
        #     x = int(self.body.position.x + math.cos(self.body.angle - math.radians(degree)) * length)
        #     y = int(self.body.position.y + math.sin(self.body.angle - math.radians(degree)) * length)

        query_info = space.segment_query_first(self.body.position, (end_x, end_y), 1, pymunk.ShapeFilter(mask=Constants.WALL_MASK | Constants.FOOD_MASK | Constants.ENEMY_MASK))
        if query_info:
            detected = True
            shape = query_info.shape
            x, y = query_info.point
            shape = query_info.shape
            if shape.collision_type == Constants.WALL:
                what = "wall"
            elif shape.collision_type == Constants.FOOD:
                what = "food"
            elif shape.collision_type == Constants.ENEMY:
                what = "enemy"
            else:
                what = "nothing"
        else:
            what = "nothing"
            x, y = end_x, end_y

        dist = int(math.sqrt((x - self.body.position.x) ** 2 + (y - self.body.position.y) ** 2))
        self.radars.append([(x, y), dist, what])


class Wall():
    # wall is a static segment
    def __init__(self, space, start_x, start_y, end_x, end_y, thickness=10):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (start_x, start_y), (end_x, end_y), thickness)
        self.shape.color = (0, 0, 255, 255)
        self.shape.elasticity = 0.00
        self.shape.collision_type = 2
        self.shape.friction = 1.0
        space.add(self.body, self.shape)
        

class Food():
    def __init__(self, space, position, size=10):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, size)
        self.shape.color = (0, 255, 0, 255)
        self.shape.collision_type = 3
        space.add(self.body, self.shape)


class Enemy():
    def __init__(self, space, position, size=10):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, size)
        self.shape.color = (255, 0, 0, 255)
        self.shape.collision_type = 4
        space.add(self.body, self.shape)