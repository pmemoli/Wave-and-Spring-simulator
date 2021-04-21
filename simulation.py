import pygame, sys
sys.path.insert(0, './Assets/Objects')
from elements import *
from ui import *

def draw_line(start, end):
    pygame.draw.line(screen, (255, 255, 255), start, end, 4)

class GameManger:
    def __init__(self):
        self.state = "set up"
        
        # Physical variables
        self.mass = 5
        self.k = 6
        self.lo = 0


    def state_manager(self):
        if self.state == "set up":
            self.prepare()
        elif self.state == "run":
            self.run()
        elif self.state == "settings":
            self.instructions()


    def prepare(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Item placement with mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_particle = Particle(pygame.mouse.get_pos(), self.mass)
                    particle_group.add(new_particle)
                
                elif event.button == 3:
                    for particle in particle_group:
                        if particle.rect.collidepoint(pygame.mouse.get_pos()):
                            self.connect_spring(particle)

                elif event.button == 2:
                    new_particle = Block(pygame.mouse.get_pos())
                    particle_group.add(new_particle)

            if event.type == pygame.KEYDOWN:
                # Run simulation
                if event.key == pygame.K_RETURN:
                    self.state = "run"

                # Delete all current physics objects
                if event.key == pygame.K_BACKSPACE:
                    particle_group.empty()
                    spring_group.empty()
                    wall_group.empty()

                # Open Instructions pop up
                if event.key == pygame.K_i:
                    instructions.create()
                    instructions.run()

                # Open Settings pop up
                if event.key == pygame.K_q:
                    settings.create()
                    settings.run()
                    self.mass, self.k, self.lo = settings.mass, settings.k, settings.lo

        particle_group.draw(screen)
        spring_group.draw(screen)
        

    def connect_spring(self, particle_1):
        
        connected = False

        while not connected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for particle_2 in particle_group:
                        if particle_2.rect.collidepoint(pygame.mouse.get_pos()):
                            new_spring = Spring(particle_1, particle_2, self.k, self.lo)
                            spring_group.add(new_spring)
                            connected = True

                    for particle_2 in wall_group:
                        if particle_2.rect.collidepoint(pygame.mouse.get_pos()):
                            new_spring = Block(particle_1, particle_2, self.k, self.lo)
                            spring_group.add(new_spring)
                            connected = True

                    connected = True

            # drawing
            screen.fill(black)
            screen.blit(ui, (0, 0))
            screen.blit(unit, (40, 550))

            draw_line(particle_1.rect.center, pygame.mouse.get_pos())
            
            particle_group.draw(screen)
            spring_group.draw(screen)

            pygame.display.update()
            clock.tick(60)


    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                self.state = "set up"

        # drawing
        screen.fill(black)
        screen.blit(ui, (0, 0))
        screen.blit(unit, (40, 550))

        particle_group.draw(screen)
        spring_group.draw(screen)

        particle_group.update()
        spring_group.update()


# General setup
pygame.init()
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)

ui = pygame.image.load(".\\Assets\\ui.png")
unit = pygame.image.load(".\\Assets\\unit.png")

# Game screen
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Objects
particle_group = pygame.sprite.Group()
spring_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()

game = GameManger()
instructions = Instructions()
settings = Settings()

while True:
    # drawing
    screen.fill(black)
    screen.blit(ui, (0, 0))
    screen.blit(unit, (40, 550))

    # Selecting proper game state
    game.state_manager()

    # Updating
    pygame.display.update()
    clock.tick(60)
