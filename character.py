import pygame
import pymunk
import math

class Robot():
    def __init__(self, name, position = (500, 500), size = 30, angle = 0, color = (50, 50, 200, 100), vision_field_angle = 90, vision_field_range = 150):
        self.name = name
        self.body = pymunk.Body(1, 1)
        self.body.position = position
        self.body.angle = angle
        self.vision_angle = vision_field_angle
        self.vision_range = vision_field_range
        self.radius = size
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.color = color

    def draw(self, window, space):
        space.add(self.body, self.shape)
        # TODO: Draw vision field
        # start_angle = math.radians(self.body.angle - self.vision_angle // 2)
        # end_angle = math.radians(self.body.angle + self.vision_angle // 2)
        # vision_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
        # pygame.draw.arc(vision_surface, (50, 200, 150, 30), (self.body.position[0] - self.vision_range, self.body.position[1] - self.vision_range, self.vision_range * 2, self.vision_range * 2), start_angle, end_angle, 1)
        # window.blit(vision_surface, self.body.position)
        return self.body

    def rotate(self, angle):
        self.angle = self.angle + angle
        return self.angle

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)
        return self.position

    def get_position(self):
        return self.position

    def get_angle(self):
        return self.angle