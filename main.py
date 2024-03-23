import pygame
import pymunk.pygame_util
import character
import simulation

pygame.init()
window = pygame.display.set_mode((simulation.WIDTH, simulation.HEIGHT))

def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps 

    space, robot = simulation.run_simulation()
    robot.draw(window, space)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
                break
        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(fps)
    pygame.quit()

if __name__ == "__main__":
    run(window, simulation.WIDTH, simulation.HEIGHT)