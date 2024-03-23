import pymunk
import character

WIDTH, HEIGHT = 1000, 1000

WALLS = [
    (20, 20, WIDTH - 20, 20),
    (20, 20, 20, HEIGHT - 20),
    (20, HEIGHT - 20, WIDTH - 20, HEIGHT - 20),
    (WIDTH - 20, 20, WIDTH - 20, HEIGHT - 20)
]

def add_wall(space, start_x, start_y, end_x, end_y, thickness=10):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (start_x, start_y), (end_x, end_y), thickness)
    shape.elasticity = 0.5
    space.add(body, shape)
    return body

def run_simulation():
    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    robot = character.Robot("robot")

    for wall in WALLS:
        add_wall(space, *wall)

    return space, robot