import pygame
import pymunk
import math

class Robot():
    # robot is a circle with a vision field
    def __init__(self, name, space, position = (100, 100), size = 30, angle = 0, color = (50, 50, 200, 100), vision_field_angle = 90, vision_field_range = 150):
        self.name = name
        self.body = pymunk.Body(1, 1)
        self.body.position = position
        self.body.angle = angle
        self.vision_angle = vision_field_angle
        self.vision_range = vision_field_range
        self.radius = size
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.color = color
        space.add(self.body, self.shape)


    def draw(self, window, space):
        # function to draw both the robor, and its vision field
        # draw the vision field as an arc
        start_angle = math.radians(self.body.angle - self.vision_angle // 2)
        end_angle = math.radians(self.body.angle + self.vision_angle // 2)
        rect = pygame.Rect(self.body.position.x - self.vision_range, self.body.position.y - self.vision_range, self.vision_range * 2, self.vision_range * 2)
        pygame.draw.arc(window, (50, 200, 150), rect, start_angle, end_angle, 1)
        # draw lines at the start and end of the arc
        start_x = self.body.position.x + self.vision_range * math.cos(start_angle)
        start_y = self.body.position.y + self.vision_range * math.sin(start_angle)
        end_x = self.body.position.x + self.vision_range * math.cos(end_angle)
        end_y = self.body.position.y + self.vision_range * math.sin(end_angle)
        # add a segment
        pygame.draw.line(window, (50, 200, 150), (self.body.position.x, self.body.position.y), (start_x, start_y), 1)
        pygame.draw.line(window, (50, 200, 150), (self.body.position.x, self.body.position.y), (end_x, end_y), 1)
        # draw space onto window
        space.debug_draw(pymunk.pygame_util.DrawOptions(window))
        return window

    def rotate(self, angle):
        # rotate the robot by angle
        self.angle = self.angle + angle
        return self.angle

    def move(self, dist):
        # move the robot by dist in the direction of its angle
        self.position = (self.position[0] + dist * math.cos(self.angle), self.position[1] + dist * math.sin(self.angle))
        return self.position