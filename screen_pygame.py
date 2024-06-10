import neat.config
import pygame
import pymunk.pygame_util
from simulation_pymunk import Constants, Simulation
import neat
import os

    #TODO: (optional) Add some 2D top-down sprites for the robot, food, enemies
    #TODO: (optional) Add sounds


agent_counter = 0

class Screen():
    # class with the window, to display
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("CPM II: Robot Simulation")
        self.window = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.window.fill("white")
        self.font = pygame.font.SysFont("Arial", 24)

    # function to run the pygame window
    def run(self, genomes, config):
        #global  environments, robots, ge, nets, simulations
        
        window = self.window
        run = True
        clock = pygame.time.Clock()
        fps = 60
        dt = 10/fps 
        
        #simulation = Simulation()
        #space = simulation.run()
        #robot = simulation.get_robot()
        #_ = robot.draw(self.window)
        
        environments = []
        simulations = []
        robots = []
        ge = []
        nets = []

        simulation = Simulation()
        simulations.append(simulation)
        space = simulation.run(2, n_robots=10)
        robots = simulation.get_robots()
       
        for genome_id, genome in genomes:

            environments.append(space)
            #robots.append(robot)
            ge.append(genome)
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            genome.fitness = 0

        global agent_counter
        agent_counter += 1
        
        #if agent_counter%10 == 0:
           # return
        
        start_ticks = pygame.time.get_ticks()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                    break
            self.window.fill("white")
            for robot in robots:
                _ = robot.draw(self.window)
                sensors = robot.draw(self.window)
            
            
            # update points every frame
            simulation.update_points(dt)
            simulation.update_position(dt)

           # simulation.check_if_stuck()

            self.display_points(simulation.points) 
            self.display_generation(agent_counter)         
           # TODO: where to put this? also, what exact info do we need to output?
            # # info for future training (?)
            # info = [robot.body.velocity.x, robot.body.velocity.y, sensors]
            # print(info) 

            # move the enemies
            #simulation.move_enemies()

            pygame.display.update()
            space.step(dt)
            clock.tick(fps)

                
            seconds = (pygame.time.get_ticks() - start_ticks)/1000
            if seconds > 20:
                break
            for robot in robots:
                index = robots.index(robot)
                #robot = simulation.get_robot()
                data = robot.get_data()
                output = nets[index].activate(data)
                choice = output.index(max(output))
                if choice == 0:
                    robot.move(0.1)
                elif choice == 1:
                    robot.rotate(1)
                else:
                    robot.rotate(-1)
            
            #print(len(genomes))
            for robot in robots:
                index = robots.index(robot)
                tmp = genomes[index][1].fitness

                tmp += simulation.points[index]
        #print("TMP new", tmp)
        #print()
                ge[index].fitness += simulation.points[index]/100
        
            #print('GENOMES:', genomes[index][1].fitness)
        for robot in robots:
            index = robots.index(robot)
            print(ge[index].fitness)
        print()
        #print(len(genomes))
        #print(simulation.points)
    #pygame.quit()

    def display_points(self, points):
        # render the points
        points_surface = []
        points_surface = self.font.render("Points:", True, "white")
        self.window.blit(points_surface, (35, 5))
    
        for i in range(0, len(points)):
            points_surface = self.font.render(f"{points[i]}", True, (Constants.COLORS2[i]))
            self.window.blit(points_surface, (50*(i%5)+50, 30*int(i/5)+30))
    
    def display_generation(self, agent_counter):
        points_surface = self.font.render(f"Generation: {agent_counter}", True, "white")
        self.window.blit(points_surface, (570, 5))

def ai_run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
        )
    pop = neat.Population(config)
    #simulation = Simulation()
    window = Screen()
    lol = pop.run(window.run, 1000)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    best_genome = pop.best_genome
    print('Best fitness: {0:3.5f} - size: {1!r}'.format(best_genome.fitness, best_genome.size()))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    ai_run(config_path)