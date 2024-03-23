import pygame
import pymunk.pygame_util
import character
from simulation import Simulation, WIDTH, HEIGHT

class Screen():
    # class with the window, to display
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("CPM II: Robot Simulation")
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.window.fill("white")

    # function to run the pygame window
    def run(self, width, height, simulation):
        run = True
        clock = pygame.time.Clock()
        fps = 60
        dt = 1/fps 

        space, robot = simulation.run()
        robot.draw(self.window, space)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                    break
            pygame.display.update()
            space.step(dt)
            clock.tick(fps)
        pygame.quit()

if __name__ == "__main__":
    simulation = Simulation()
    window = Screen()
    window.run(WIDTH, HEIGHT, simulation)