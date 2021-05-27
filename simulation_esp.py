from Assets.Objects.elements import *
from Assets.Objects.utilities import *

class Simulation:
    def __init__(self):
        # State variables
        self.running = False
        self.show_instructions = False
        self.instructions_position = 600
        self.show_parameters = False
        self.parameters_position = 600
        self.fps = 60
        self.parameter_selection_fps = 60

        # General physical variables
        self.pixel_meter_ratio = 1/30  # meter/pixel
        self.gravity = False

        # String physical variables
        self.string_mass = 140  # kg
        self.objects_in_string = 200  # parameter
        self.density = self.string_mass / self.objects_in_string  # Bugs arise if tension/density relation is too large
        self.initial_tension = 200  # N  parameter

        self.string_points = []
        self.blocks = []
        self.drawing_string = False
        self.string_drawn = False

        # Mass-Spring discrete physical variables
        self.mass = 4  # kg parameter
        self.spring_constant = 4  # parameter
        self.setting_spring = False
        self.spring_particle = None

    def run(self):
        while True:  # Main loop
            # Drawing background
            screen.fill(black)
            screen.blit(background, (0, 0))

            # Drawing string
            self.draw_spring_logic()

            # Drawing spring
            if self.setting_spring:
                self.set_spring()

            # Draw states status (run and gravity)
            self.draw_states()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.object_creation_management(event)

                if event.type == pygame.KEYDOWN:
                    self.state_management(event)  # Manages different states

            spring_group.draw(screen)
            particle_group.draw(screen)

            if self.running:
                particle_group.update(gravity=self.gravity)
                spring_group.update()

            if self.show_instructions:
                self.instructions()
                self.parameters_position = 600
                self.show_parameters = False

            if self.show_parameters:
                self.parameters()
                self.instructions_position = 600
                self.show_instructions = False
                self.parameters_management()

            # Displaying
            pygame.display.update()
            if self.show_parameters:
                clock.tick(self.parameter_selection_fps)
            else:
                clock.tick(self.fps)

    def draw_spring_logic(self):
        draw_string_key = pygame.mouse.get_pressed()[0]

        if draw_string_key and not self.drawing_string:
            for particle in particle_group:
                if particle.rect.collidepoint(pygame.mouse.get_pos()) and particle.mass > 10000:
                    self.fps *= 5
                    self.drawing_string = True
                    self.blocks.append(particle)

        elif not draw_string_key and self.drawing_string:
            self.fps /= 5
            found_block = False
            for particle in particle_group:
                if particle.rect.collidepoint(pygame.mouse.get_pos()) and particle != self.blocks[0]:
                    found_block = True
                    self.string_drawn = True
                    self.blocks.append(particle)

            if not found_block:
                self.string_points = []
                self.blocks = []

            self.drawing_string = False

        # Create spring model of string if drawn
        if self.string_drawn:
            self.set_string()

        # Draws spring
        for point in self.string_points:
            pygame.draw.circle(screen, white, point, 2)

        if self.drawing_string:
            self.string_points.append(pygame.mouse.get_pos())

    def set_string(self):  # Creates a string from string_points based on parameters once drawn
        start_point = min(self.string_points[0][0], self.string_points[-1][0])
        end_point = max(self.string_points[0][0], self.string_points[-1][0])
        x_range = np.linspace(start_point, end_point, self.objects_in_string)
        spaced_string_points = []
        for x in x_range:
            spaced_string_points.append(punto_mas_proximo(x, self.string_points))

        self.string_points = spaced_string_points

        # Create masses
        first_block, last_block = block_selection(self.blocks)

        masses = [first_block]
        for point in self.string_points:
            masses.append(Particle(point, self.density))

        masses.append(last_block)

        # Connect them with springs
        springs = []
        k = self.initial_tension / ((x_range[1] - x_range[0]) * self.pixel_meter_ratio)
        if k > self.density * 3000:  # Mas alla de 3000 empieza a romperse numpy y otras cosas que ni idea
            k = self.density * 3000

        for i in range(len(masses) - 1):
            springs.append(Spring(masses[i], masses[i + 1], k, 0))

        for i in range(len(masses)):
            particle_group.add(masses[i])
            if i < len(springs):
                spring_group.add(springs[i])

        self.string_drawn = False
        self.string_points = []
        self.blocks = []

    def set_spring(self):
        # Connects one mass with another using a spring
        particle_1 = self.spring_particle
        is_clicking = pygame.mouse.get_pressed()[0]

        for particle_2 in particle_group:
            if particle_2.rect.collidepoint(pygame.mouse.get_pos()) and is_clicking:
                if pygame.key.get_pressed()[pygame.K_r]:  # rod mode
                    difference = np.linalg.norm(np.subtract(np.asarray(particle_1.center), np.asarray(particle_2.center)))
                    rod_approx_constant = min(particle_1.mass, particle_2.mass) * 3400  # El k del resorte depende de la masa para no romper con masas chicas
                    new_spring = Spring(particle_1, particle_2, rod_approx_constant, difference, color=gray)
                else:
                    new_spring = Spring(particle_1, particle_2, self.spring_constant, 0)

                self.setting_spring = False
                self.spring_particle = None
                spring_group.add(new_spring)

                break

        # Draws spring
        draw_line(screen, particle_1.rect.center, pygame.mouse.get_pos(), white)

    def state_management(self, event):
        # Run simulation
        if event.key == pygame.K_RETURN:
            self.running = not self.running

        # Resets current objects
        if event.key == pygame.K_BACKSPACE:
            particle_group.empty()
            spring_group.empty()
            self.blocks = []
            self.running = False

        if event.key == pygame.K_i:
            self.show_instructions = not self.show_instructions
            self.instructions_position = 600

        if event.key == pygame.K_q:
            self.show_parameters = not self.show_parameters
            self.parameters_position = 600

        if event.key == pygame.K_g:
            self.gravity = not self.gravity

    def object_creation_management(self, event):
        if event.button == 1:  # Creates a particle
            avoid_creating = False
            for particle in particle_group:  # Doesn't create a particle if it's on top of another
                if particle.rect.collidepoint(pygame.mouse.get_pos()):
                    avoid_creating = True

            if not avoid_creating:
                new_particle = Particle(pygame.mouse.get_pos(), self.mass, radius=7)
                particle_group.add(new_particle)

        # Creates an unmovable particle
        if event.button == 2:
            new_particle = Block(pygame.mouse.get_pos())
            particle_group.add(new_particle)

        if event.button == 3:
            for particle in particle_group:
                if particle.rect.collidepoint(pygame.mouse.get_pos()):
                    self.setting_spring = True
                    self.spring_particle = particle

    def draw_states(self):
        if self.running:
            screen.blit(on, (730, 7))
        else:
            screen.blit(off, (730, 7))

        if self.gravity:
            screen.blit(on, (725, 557))
        else:
            screen.blit(off, (725, 557))

    def instructions(self):  # Involves animation
        y_top = 80
        speed = -40

        screen.blit(instructions, (200, self.instructions_position))

        if self.instructions_position > y_top:
            self.instructions_position += speed

    def parameters(self):
        y_top = 120
        speed = -40

        screen.blit(parameters, (220, self.parameters_position))

        if self.parameters_position > y_top:
            self.parameters_position += speed
        else:
            draw_text(parameter_font, screen, str(round(self.mass, 2)) + " kg", (470, 201))  # Mass
            draw_text(parameter_font, screen, str(round(self.spring_constant, 2)), (490, 240))  # Spring Constant
            draw_text(parameter_font, screen, str(self.string_mass) + " kg", (450, 280))  # String Mass
            draw_text(parameter_font, screen, str(self.initial_tension) + " N", (495, 318))  # Equilibrium tension
            draw_text(parameter_font, screen, str(self.objects_in_string), (460, 380))  # Particles per string
            draw_text(parameter_font, screen, "x " + str(round(self.fps/60, 3)), (440, 418))  # Animation seconds/simulation seconds

    def parameters_management(self):
        if pygame.key.get_pressed()[pygame.K_t] and self.mass - 0.06 > 0:
            self.mass -= 0.06
        elif pygame.key.get_pressed()[pygame.K_y]:
            self.mass += 0.06

        if pygame.key.get_pressed()[pygame.K_a] and self.spring_constant - 0.06 > 0:
            self.spring_constant -= 0.06
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.spring_constant += 0.06

        if pygame.key.get_pressed()[pygame.K_z] and self.string_mass - 1 > 0:
            self.string_mass -= 1
        elif pygame.key.get_pressed()[pygame.K_x]:
            self.string_mass += 1

        if pygame.key.get_pressed()[pygame.K_e] and self.initial_tension - 1 > 10:
            self.initial_tension -= 1
        elif pygame.key.get_pressed()[pygame.K_r]:
            self.initial_tension += 1

        if pygame.key.get_pressed()[pygame.K_d] and self.objects_in_string - 1 > 2:
            self.objects_in_string -= 1
        elif pygame.key.get_pressed()[pygame.K_f]:
            self.objects_in_string += 1

        if pygame.key.get_pressed()[pygame.K_c] and self.fps - 1 > 10:
            self.fps -= 1
        elif pygame.key.get_pressed()[pygame.K_v]:
            self.fps += 1


# General Setup
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
parameter_font = pygame.font.Font('.\\Assets\\ReemKufi.ttf', 22)

# Game screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Images and variables
black = (0, 0, 0)
white = (255, 255, 255)
gray = (93, 93, 93)

background = pygame.image.load('.\\Assets\\Images\\esp\\background.png').convert_alpha()
instructions = pygame.image.load('.\\Assets\\Images\\esp\\instructions.png').convert_alpha()
parameters = pygame.image.load('.\\Assets\\Images\\esp\\parameters.png').convert_alpha()
on = pygame.image.load('.\\Assets\\Images\\esp\\on.png').convert_alpha()
off = pygame.image.load('.\\Assets\\Images\\esp\\off.png').convert_alpha()

# Objects
particle_group = pygame.sprite.Group()
spring_group = pygame.sprite.Group()

simulation = Simulation()

simulation.run()
