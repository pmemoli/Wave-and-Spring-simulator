import pygame
import numpy as np

# Simulation is run at 60 fps
delta_time = 1 / 60

black = (0, 0, 0)
white = (255, 255, 255)

class Particle(pygame.sprite.Sprite):
    def __init__(self, center, mass, velocity=[0, 0]):
        super().__init__()

        # Useful attributes
        radius = 7
        self.mass = int(mass)
        self.center = center
        self.acceleration = np.array([0, 0])
        self.speed = np.array(velocity)

        # Drawing cirlce
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()

        pygame.draw.circle(self.image, white, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = self.center


    def update(self, gravity=False):
        # Takes gravity
        if gravity:
            self.apply_force(np.array([0, 400]))

        center = np.asarray(self.center)
        new_center = np.add(center, self.speed * delta_time)  # Metodo de euler
        self.rect.center = tuple(new_center)
        self.center = tuple(new_center)


    def apply_force(self, force_vector):
        self.acceleration = (1 / self.mass) * force_vector
        self.speed = np.add(self.speed, self.acceleration * delta_time)



class Block(pygame.sprite.Sprite): # TODO: Eliminar el calculo de fuerzas para el bloque
    def __init__(self, center):
        super().__init__()

        # Useful attributes
        radius = 7
        self.mass = 10000000000000000000000000000  # Virtually unmovable
        self.center = center
        self.acceleration = np.array([0, 0])
        self.speed = np.array([0, 0])

        # Drawing cirlce
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(white)

        self.rect = self.image.get_rect()
        self.rect.center = self.center


    def update(self, gravity=False):
        center = np.asarray(self.center)
        new_center = np.add(center, self.speed * delta_time)  # Esta mal la fisica
        self.rect.center = tuple(new_center)
        self.center = tuple(new_center)


    def apply_force(self, force_vector):
        self.acceleration = (1 / self.mass) * force_vector
        self.speed = np.add(self.speed, self.acceleration * delta_time)



class Spring(pygame.sprite.Sprite):
    def __init__(self, node1, node2, k, lo):
        super().__init__()

        self.k = int(k)
        self.lo = int(lo)

        self.node1 = node1
        self.node2 = node2

        # Drawing cirlce
        node1_position, node2_position = np.asarray(self.node1.rect.center), np.asarray(self.node2.rect.center)

        width = abs(node1_position[0] - node2_position[0])
        height = abs(node1_position[1] - node2_position[1])

        self.image = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()

        start, end = self.line_positions(node1_position, node2_position, width, height)

        pygame.draw.line(self.image, white, start, end, 4)

        self.rect = self.image.get_rect()
        self.rect.center = np.add(node1_position, node2_position) / 2


    def spring_force(self):
        node1_position = np.asarray(self.node1.center)
        node2_position = np.asarray(self.node2.center)

        distance_vector = np.subtract(node1_position, node2_position)
        distance_magnitude = np.linalg.norm(distance_vector)

        if self.lo == 0:
            force = -self.k * distance_vector  # Force applied to node 1, node 2 recieves the opposite force.
        else:
            force_magnitude = -self.k * (distance_magnitude - self.lo)
            force_direction = distance_vector / distance_magnitude
            force = force_magnitude * force_direction

        return force


    def update(self):
        force = self.spring_force()

        self.node1.apply_force(force)
        self.node2.apply_force(-force)

        # Drawing cirlce
        node1_position, node2_position = np.asarray(self.node1.rect.center), np.asarray(self.node2.rect.center)

        width = abs(node1_position[0] - node2_position[0])
        height = abs(node1_position[1] - node2_position[1])

        self.image = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()

        start, end = self.line_positions(node1_position, node2_position, width, height)

        pygame.draw.line(self.image, white, start, end, 4)

        self.rect = self.image.get_rect()
        self.rect.center = np.add(node1_position, node2_position) / 2


    def line_positions(self, position_1, position_2, width, height):
        if position_1[0] <= position_2[0]:
            if position_1[1] > position_2[1]:
                start = (0, height)
                end = (width, 0)

            else:
                start = (0, 0)
                end = (width, height)

        else:
            if position_1[1] < position_2[1]:
                start = (0, height)
                end = (width, 0)

            else:
                start = (0, 0)
                end = (width, height)

        return start, end
