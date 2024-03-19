import pygame
import pymunk
import pymunk.pygame_util
import math
import character

pygame.init()
WIDTH, HEIGHT = 1000, 1000
window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()


def add_wall(space, start_x, start_y, end_x, end_y, thickness=10):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (start_x, start_y), (end_x, end_y), thickness)
    shape.elasticity = 0.5
    space.add(body, shape)
    return body

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps 

    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    robot = character.Robot("robot")
    robot.draw(window, space, 500, 500, (200, 50, 50, 30), 30)

    walls = [
        (20, 20, width - 20, 20),
        (20, 20, 20, height - 20),
        (20, height - 20, width - 20, height - 20),
        (width - 20, 20, width - 20, height - 20)
    ]

    for wall in walls:
        add_wall(space, *wall)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(fps)
    
    pygame.quit()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)