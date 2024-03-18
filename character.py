import pygame
import pymunk
import math

class Robot():
    def __init__(self, name):
        self.name = name

    def draw(self, window, space, x, y, color, radius, vision_angle=90, vision_range=150):
        self.body = pymunk.Body(1, 1)
        self.body.position = (x, y)
        self.body.angle = 0
        self.color = color
        self.vision_angle = vision_angle
        self.vision_range = vision_range
        self.radius = radius
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.color = self.color
        space.add(self.body, self.shape)
        # TODO: Draw vision
        # start_angle = math.radians(self.body.angle - self.vision_angle // 2)
        # end_angle = math.radians(self.body.angle + self.vision_angle // 2)
        # vision_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
        # pygame.draw.arc(vision_surface, (100, 100, 100, 30), (self.body.position[0] - self.vision_range, self.body.position[1] - self.vision_range, self.vision_range * 2, self.vision_range * 2), start_angle, end_angle, 1)
        # window.blit(vision_surface, (0, 0))
        return self.body

    def rotate(self, angle):
        self.angle = angle
        return self.angle

    def move(self, x, y):
        self.position = (x, y)
        return self.position

    def get_position(self):
        return self.position

    def get_angle(self):
        return self.angle