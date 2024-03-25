import pygame
import pymunk
import math

class Robot():
    # robot is a circle with a vision field
    def __init__(self, name, space, position = (100, 100), size = 30, angle = 0, color = (50, 50, 200, 100), vision_field_angle = 90, vision_field_range = 500):
        self.name = name
        self.body = pymunk.Body(1, 1)
        self.body.position = position
        self.body.angle = angle
        self.space = space
        self.vision_angle = vision_field_angle
        self.vision_range = vision_field_range
        self.radius = size
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.color = color
        self.shape.elasticity = 0.00
        self.body.mass = 1
        space.add(self.body, self.shape)


    def draw(self, window = None):
        self.window = window
        # function to draw both the robor, and its vision field
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
        # draw space onto window
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(window))
        return self.window

    def rotate(self, angle):
        # rotate the robot by angle
        self.body.angle = self.body.angle + math.radians(angle)
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(self.window))
        return self.body.angle

    def move(self, dist):
        # move the robot by dist in the direction of its angle
        self.body.position = (self.body.position[0] + dist * math.cos(self.body.angle), self.body.position[1] + dist * math.sin(self.body.angle))
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(self.window))
        return self.body.position


class Wall():
    # wall is a static segment
    def __init__(self, space, start_x, start_y, end_x, end_y, thickness=10):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (start_x, start_y), (end_x, end_y), thickness)
        self.shape.elasticity = 0.00
        space.add(self.body, self.shape)
        