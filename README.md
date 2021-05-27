# Spring-Simulator
Set any configuration of springs, particles, pendulums and waves on a 2D plane and see how it evolves.

Describa cualquier configuracion de resortes, particulas, pendulos y ondas/sogas en 2D para ver como evoluciona.

Pygame and Numpy required

Notes: Evolution speed is calculated as fps / 60, with 60 fps being used as a real simulation second. Tension withing masses of a string is
not allowed to exceed its mass * 3000 since numpy breaks for some reason.

Backspace deletes current configuration
