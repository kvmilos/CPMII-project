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

    WALL = 2
    FOOD = 3
    ENEMY = 4


class Robot():
    # robot is a circle with a vision field, the main object in the simulation
    def __init__(self, name, space, position = (100, 100), size = 30, angle = 0, color = (50, 50, 200, 100), vision_field_angle = 90, vision_field_range = 500):
        self.name = name
        # body is what is used to apply forces
        self.body = pymunk.Body(1, 1)
        self.body.position = position
        self.body.angle = angle
        self.space = space
        self.vision_angle = vision_field_angle
        self.vision_range = vision_field_range
        self.radius = size
        # shape is what is used to draw the robot
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.color = color
        self.body.mass = 1
        self.shape.collision_type = 1
        self.body.collision_type = 1
        space.add(self.body, self.shape)

    def draw(self, window = None):
        # function to draw both the robot, and its vision field
        self.window = window
        # draw the vision field as an arc
        start_angle = self.body.angle - math.radians(self.vision_angle // 2)
        end_angle = self.body.angle + math.radians(self.vision_angle // 2)
        rect = pygame.Rect(self.body.position.x - self.vision_range, self.body.position.y - self.vision_range, self.vision_range * 2, self.vision_range * 2)
        pygame.draw.arc(window, (50, 200, 150), rect, -end_angle, -start_angle, 1)
        # draw lines at the start and end of the arc
        start_x = self.body.position.x + self.vision_range * math.cos(start_angle)
        start_y = self.body.position.y + self.vision_range * math.sin(start_angle)
        end_x = self.body.position.x + self.vision_range * math.cos(end_angle)
        end_y = self.body.position.y + self.vision_range * math.sin(end_angle)
        pygame.draw.line(self.window, (50, 200, 150), (self.body.position.x, self.body.position.y), (start_x, start_y), 1)
        pygame.draw.line(self.window, (50, 200, 150), (self.body.position.x, self.body.position.y), (end_x, end_y), 1)

        detected_objects = self.sense()
        for shape, point in detected_objects:
            color = (100, 100, 100)  # default color for unknown objects
            if shape.collision_type == Constants.WALL:
                color = (0, 0, 255)
            elif shape.collision_type == Constants.FOOD:
                color = (0, 255, 0)
            elif shape.collision_type == Constants.ENEMY:
                color = (255, 0, 0)

            # pygame.draw.circle(window, color, (int(point.x), int(point.y)), 5)

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

    def get_angle(self) -> float:
        # return the angle of the robot
        return self.body.angle

    def get_position(self) -> tuple:
        # return the position of the robot
        return self.body.position

    def sense(self):
        # detect objects within the robot's vision field
        detected_objects = []
        start_point = self.body.position

        for angle_offset in range(-self.vision_angle // 2, self.vision_angle // 2, 3):
            end_point = start_point + pymunk.Vec2d(self.vision_range, 0).rotated(self.body.angle + math.radians(angle_offset))
            query = self.space.segment_query_first(start_point, end_point, 1, pymunk.ShapeFilter())
            if query is not None:
                detected_objects.append((query.shape, query.point))
        print(detected_objects)
        return detected_objects

class Wall():
    # wall is a static segment
    def __init__(self, space, start_x, start_y, end_x, end_y, thickness=10):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (start_x, start_y), (end_x, end_y), thickness)
        self.shape.elasticity = 0.00
        self.shape.collision_type = 2
        self.shape.friction = 1.0
        space.add(self.body, self.shape)
        

class Food():
    def __init__(self, space, position, size=10):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, size)
        self.shape.color = (255, 0, 0)
        self.shape.collision_type = 3
        space.add(self.body, self.shape)