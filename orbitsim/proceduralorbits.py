from random import randint
import orbits
import math


def main():
    masses = []
    bodies = randint(3, 10)
    for i in range(bodies):
        mass = 10 ** randint(7, 15)
        velocity = [randint(0, 5), randint(0, 5)]
        pos = [randint(0, orbits.WIDHT), randint(0, orbits.HEIGHT)]

        radius =  (math.log10(mass)/ 10 ** 15) * (10 ** 15) / 4
        print(f'mass {mass} radius {radius}')


        masses.append(orbits.new_mass(mass, velocity, pos , radius))

    orbits.pygame_rendering(masses)

if __name__ == "__main__":
    main()