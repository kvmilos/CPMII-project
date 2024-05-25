import pymunk
from classes import Robot, Wall, Constants, Food, Enemy

class Simulation():
    # class to create the simulation environment
    def run(self):
    # function to run the simulation
        space = pymunk.Space()
        space.gravity = (0.0, 0.0)
        space.iterations = 30

        robot = Robot("robot", space, (Constants.WIDTH // 2, Constants.HEIGHT // 2))

        for cords in Constants.WALLS:
            wall = Wall(space, *cords)

        #TODO: Add random food spawning
        #TODO: Add enemy spawning
        #TODO: Add enemy movement
        #TODO (optional): Add random walls spawning
        #TODO: Implement player-food collision - eating
        #TODO: Implement player-enemy collision - dying/HP system (?)
        #TODO: Add sprites for the robot, food, enemies
        #TODO (optional): Add sounds
        #TODO: Train an AI to play the game


        Food(space, (400, 500))
        Enemy(space, (500, 600))

        return space, robot