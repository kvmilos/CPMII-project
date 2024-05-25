import pygame
import pymunk.pygame_util
from simulation_pymunk import Constants, Simulation

    #TODO: (optional) Add some 2D top-down sprites for the robot, food, enemies
    #TODO: (optional) Add sounds

    #TODO: Train an AI to play the game

class Screen():
    # class with the window, to display
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("CPM II: Robot Simulation")
        self.window = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.window.fill("white")
        self.font = pygame.font.SysFont("Arial", 30)

    # function to run the pygame window
    def run(self, simulation):
        window = self.window
        run = True
        clock = pygame.time.Clock()
        fps = 60
        dt = 1/fps 

        space, robot = simulation.run()
        _ = robot.draw(self.window)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False

            # move the robot using wasd
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                robot.move(2)
            if keys[pygame.K_s]:
                robot.move(-2)
            if keys[pygame.K_a]:
                robot.rotate(-1)
            if keys[pygame.K_d]:
                robot.rotate(1)

            self.window.fill("white")
            sensors = robot.draw(self.window)

            # update points every frame
            simulation.update_points(dt)
            
            # TODO: where to put this? also, what exact info do we need to output?
            # # info for future training (?)
            # info = [robot.body.velocity.x, robot.body.velocity.y, sensors]
            # print(info) 

            # move the enemies
            simulation.move_enemies()

            pygame.display.update()
            space.step(dt)
            clock.tick(fps)

        pygame.quit()
    
    def display_points(self, points):
        # render the points
        points_surface = self.font.render(f"Points: {points}", True, "black")
        self.window.blit(points_surface, (10, 10))


if __name__ == "__main__":
    simulation = Simulation()
    window = Screen()
    window.run(simulation)