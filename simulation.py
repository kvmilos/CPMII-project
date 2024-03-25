import pymunk
from character import Robot, Wall

# constants for the window
class Constants:
    WIDTH, HEIGHT = 800, 800

    WALLS = [
        (20, 20, WIDTH - 20, 20),
        (20, 20, 20, HEIGHT - 20),
        (20, HEIGHT - 20, WIDTH - 20, HEIGHT - 20),
        (WIDTH - 20, 20, WIDTH - 20, HEIGHT - 20)
    ]

class Simulation():
    # class to create the simulation environment
    # function to run the simulation
    def run(self):
        space = pymunk.Space()
        space.gravity = (0.0, 0.0)
        space.iterations = 30

        robot = Robot("robot", space, (Constants.WIDTH // 2, Constants.HEIGHT // 2))

        for cords in Constants.WALLS:
            wall = Wall(space, *cords)
            

        # TODO: Add vision field for robot using segment_query_first (?)
        # TODO: Add collision handler
        # TODO: Add food(?)
        # TODO: masks (?) for the robot to differentiate between walls, and food

        return space, robot