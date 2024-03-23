import pymunk
import character

# constants for the window
WIDTH, HEIGHT = 800, 800

# walls of the window
WALLS = [
    (20, 20, WIDTH - 20, 20),
    (20, 20, 20, HEIGHT - 20),
    (20, HEIGHT - 20, WIDTH - 20, HEIGHT - 20),
    (WIDTH - 20, 20, WIDTH - 20, HEIGHT - 20)
]

class Simulation():
    # class to create the simulation environment
    def add_wall(self, space, start_x, start_y, end_x, end_y, thickness=10):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, (start_x, start_y), (end_x, end_y), thickness)
        shape.elasticity = 0.5
        space.add(body, shape)
        return body

    # function to run the simulation
    def run(self):
        space = pymunk.Space()
        space.gravity = (0.0, 0.0)

        robot = character.Robot("robot", space, (WIDTH // 2, HEIGHT // 2))

        for wall in WALLS:
            self.add_wall(space, *wall)

        # TODO: Add vision field for robot using segment_query_first (?)
        # TODO: Add collision detection
        # TODO: Add movement + rotation
        # TODO: Add food(?)
        # TODO: masks (?) for the robot to differentiate between walls, and food

        return space, robot