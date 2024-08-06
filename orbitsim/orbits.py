"""
Simulates planitary orbits using newtonian equations
F = GmM/r^2
F = ma
"""
import math
import pygame
import sys
from random import randint
from copy import deepcopy

FPS = 60
SPEED_MULTIPLY = 3
verbose = 1
RESOLUTION = WIDHT, HEIGHT = 1920, 1080
BLACK = (0, 0, 0)
OBJECT_COLOR = (255, 255, 255)
SPEED_LIMIT = 300

G = 6.67 * (10**-11)  # Gravitational constant


class Mass():
    """an object that has mass, 'uniform sphere' """

    def __init__(self, mass, initial_velocity, pos, radius=1):
        """num, [x,y], [x,y], num"""
        self.mass = mass
        self.velocity = initial_velocity
        self.pos = pos
        self.radius = radius
        self.forces = [0, 0]
        self.emergency_force = [0, 0]

    def calc_pos(self):
        self.calc_velocity()
        self.pos[0] += self.velocity[0] * (1/FPS) * SPEED_MULTIPLY
        self.pos[1] += self.velocity[1] * (1/FPS) * SPEED_MULTIPLY

    def calc_velocity(self):
        self.velocity[0] += (self.forces[0] / self.mass) * (1/FPS) * SPEED_MULTIPLY
        self.velocity[1] += (self.forces[1] / self.mass) * (1/FPS) * SPEED_MULTIPLY

        # Speed Limits 
        # X
        if self.velocity[0] > SPEED_LIMIT:
            self.velocity[0] = SPEED_LIMIT
        if self.velocity[0] < -SPEED_LIMIT:
            self.velocity[0] = -SPEED_LIMIT
        # Y
        if self.velocity[1] > SPEED_LIMIT:
            self.velocity[1] = SPEED_LIMIT
        if self.velocity[1] < -SPEED_LIMIT:
            self.velocity[1] = -SPEED_LIMIT




    def calc_force(self, otherbody):
        """F = GmM/r^2"""
        #     .
        #    /|          SohCahToa
        #  d/ |          Tan-1(o/a) = angle(radians)
        #  /  |  Y
        # /t__|
        #  X
        # c^2 = a^2 + b^2
        dist = math.dist(self.pos, otherbody.pos)
        try:
            F_total = (G * self.mass * otherbody.mass) / (dist ** 2)
            #debug_print(f'F_total = {F_total}', 2)
        except ZeroDivisionError:
            dist = 0.0001
            F_total = (G * self.mass * otherbody.mass) / (dist ** 2)
            debug_print('Objects are at same pos reverting to last frame', 1)

        x = self.pos[0] - otherbody.pos[0]
        y = self.pos[1] - otherbody.pos[1]
        # T = o/a
        try:
            theta = math.atan(y/x)
        except ZeroDivisionError:
            print('Zero Division error')
            theta = math.atan((y - 0.001) /(x + 0.001))
        #thetay = math.atan(x/y)
        # reset forces after frame to prevent jerk
        F_x = math.fabs(F_total * math.cos(theta))
        F_y = math.fabs(F_total * math.sin(theta))

        # hard coded negatives
        if dist > (self.radius * 3):
            if x >= 0:
                self.forces[0] -= F_x
            else:
                self.forces[0] += F_x

            if y >= 0:
                self.forces[1] -= F_y
            else:
                self.forces[1] += F_y
        else:
            if x >= 0:
                self.forces[0] += F_x
            else:
                self.forces[0] -= F_x

            if y >= 0:
                self.forces[1] += F_y
            else:
                self.forces[1] -= F_y

        debug_print(
            f'Dist: {dist:.1f} T: {F_total:.2f} x: {F_x:.2f}, y: {F_y:.2f}', 2)

        return(1)

    def reset_forces(self):
        # Saving for error
        self.emergency_force = self.forces
        self.forces = [0, 0]


def main():
    masses = []

    

    #        mass       init_velocity,  pos        radius
    masses.append(new_mass(10 ** 6,    [5, 0],       [300, 600]   ))
    masses.append(new_mass(10 ** 15,   [0, 0.1],       [400, 400], 2))
    #new_mass(10 ** 14,    [-10, 0],       [500, 200]   )
    pygame_rendering(masses)

def new_mass(mass, init_velocity, pos, radius=1):
        """Call this to add another mass"""
        return((Mass(mass, init_velocity, pos, radius)))


def pygame_rendering(masses):
    global SPEED_MULTIPLY
    """Does all the rendering in here"""
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    clock = pygame.time.Clock()
    surfaces = []
    size_multiplier = 3

    prev_pos = []

    dot_surface = pygame.Surface((1,1))
    dot_surface.fill('White')
    for i in range(len(masses)):
        diameter = int(size_multiplier * masses[i].radius * 2)
        surfaces.append(pygame.Surface((diameter, diameter)))
        surfaces[i].fill((randint(10, 255),randint(10, 255), randint(10, 255)))

    render_objects = True

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #keys = pygame.key.get_pressed()
                if event.key == pygame.K_LEFT:
                    SPEED_MULTIPLY -= 1
                    print(SPEED_MULTIPLY)
                if event.key == pygame.K_RIGHT:
                    SPEED_MULTIPLY += 1
                    print(SPEED_MULTIPLY)
                if event.key == pygame.K_BACKSPACE:
                    if render_objects == True:
                        render_objects = False
                    else:
                        render_objects = True

        physics_tick(masses)
        screen.fill(BLACK)
        #print(prev_pos)
        for dot_pos in prev_pos:
            #print(dot_pos)
            screen.blit(dot_surface, dot_pos)

        for i in range(len(masses)):
            if render_objects:
                new_radius = masses[i].radius * size_multiplier
                screen.blit(surfaces[i], (masses[i].pos[0] - new_radius, masses[i].pos[1] - new_radius))
                cur_coords = deepcopy(masses[i].pos)
                prev_pos.append(cur_coords)

        #print(len(prev_pos))



        pygame.display.update()


def physics_tick(masses):
    """Call every frame to do the math"""

    # Add forces from all masses to eachother
    for mass in masses:
        mass.reset_forces()
        for otherbodies in masses:
            if mass != otherbodies:
                mass.calc_force(otherbodies)

        # Finished adding all forces
        mass.calc_pos()
        # Prevent flying off screen for funny stuff
        if mass.pos[0] < 0 or mass.pos[0] > WIDHT:
            mass.velocity[0] *= -1
            #mass.calc_pos()
        if mass.pos[1] < 0 or mass.pos[1] > HEIGHT:
            mass.velocity[1] *= -1

        debug_print(f'{mass.pos}', 3)


def debug_print(msg, v_level):
    """prints messages if the Verbose level of the script is greater
    than that of the v_level"""
    if verbose >= v_level:
        print(msg)


if __name__ == "__main__":
    main()
