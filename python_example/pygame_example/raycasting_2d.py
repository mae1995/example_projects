#   This script is based by the Youtube-Tutorial "Coding Challange #145: 2D Raycasting" created by "The Coding Train".
#   He using JavaScript and P5-Framework.
#   I have written it with Python and using the engine pygame.
#   I have adding some more stuff...
#   
#
#   Source:
#   Youtube-Video : https://www.youtube.com/watch?v=TOEi6T2mtHo&t
#
#
#   Michael A. Eckhardt, 28.08.2019
#



import pygame, random, math
from pygame.math import Vector2


# --- Init
pygame.init()

# --- Classes
class Boundary:

    def __init__(self, screen, pos_a, pos_b):
        self.position_a = pos_a
        self.position_b = pos_b
        self.screen = screen

    def show(self):
        pygame.draw.line(self.screen, (255, 255, 255), self.position_a, self.position_b)


class Particle:
    def __init__(self, screen):
        self.position = (400, 300)
        self.rays = []
        self.screen = screen

        #for i in range (0, 360):
        i = 0
        while i <= 360:
            self.rays.append(Ray(screen, self.position, math.radians(i)))
            i += 0.5

    def show(self):
        for ray in self.rays:
            ray.show()

    def look(self, walls):
        arr_points = []

        for ray in self.rays:
            closest = None
            record = 999999

            for wall in walls:
                pt = ray.cast(wall)
                if pt is not None:
                    vx = pt[0] - self.position[0]
                    vy = pt[1] - self.position[1]

                    dist = math.sqrt((vx * vx + vy * vy))
                    if dist < record:
                        record = dist
                        closest = pt

            if closest is not None:
                #pygame.draw.line(self.screen, (255, 255, 255), self.position, closest)
                arr_points.append(closest)

        pygame.draw.polygon(screen, (125,0,0), arr_points)
         
    def update(self, mouse_pos):
        for ray in self.rays:
            ray.set_pos(mouse_pos)

        self.position = mouse_pos

class Ray:

    def __init__(self, screen, pos, angle):
        self.screen = screen
        self.position = pos
        self.direction = (math.cos(angle), math.sin(angle)) #(0, -1)

    def set_pos(self, pos):
        self.position = pos

    def show(self):
        dir_x = self.direction[0] * 10
        dir_y = self.direction[1] * 10

        new_x = self.position[0] + dir_x
        new_y = self.position[1] + dir_y

        pygame.draw.line(self.screen, (255, 255, 255), self.position, (new_x, new_y))

    def lookAt(self, pos):
        dir_x = pos[0] - self.position[0]
        dir_y = pos[1] - self.position[1]

        self.direction = Vector2((dir_x, dir_y)).normalize()


    def cast(self, wall):
        x1 = wall.position_a[0]
        y1 = wall.position_a[1]
        x2 = wall.position_b[0]
        y2 = wall.position_b[1]

        x3 = self.position[0]
        y3 = self.position[1]
        x4 = self.position[0] + self.direction[0]
        y4 = self.position[1] + self.direction[1] 

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if den == 0:
            return None
        
        t = ((x1- x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1- x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if t > 0 and t < 1 and u > 0:
            pos_x = x1 + t * (x2 - x1)
            pos_y = y1 + t * (y2 - y1)

            return (pos_x, pos_y)
        else:
            return None

# --- Main
screen      =   pygame.display.set_mode((800, 600))
clock       =   pygame.time.Clock()
isRunning   =   True

walls       =   [] #Boundary(screen, (100, 100), (250, 250))
particle    =   Particle(screen)

for i in range(0, 5):
    walls.append(Boundary(screen, (random.randint(100, 400), random.randint(100, 400)),(random.randint(100, 400), random.randint(100, 400))))


walls.append(Boundary(screen, (400, 400), (400, 500)))
walls.append(Boundary(screen, (400, 400), (400, 400)))
walls.append(Boundary(screen, (700, 400), (400, 400)))
walls.append(Boundary(screen, (700, 400), (400, 500)))


walls.append(Boundary(screen, (0, 0), (800, 0)))
walls.append(Boundary(screen, (800, 0), (800, 800)))
walls.append(Boundary(screen, (0, 800), (800, 800)))
walls.append(Boundary(screen, (0, 0), (0, 800)))

# ---
pygame.display.set_caption("Raycasting")
pygame.mouse.set_visible(1)
pygame.key.set_repeat(1, 30)


# ---
while isRunning:

    clock.tick(30)

    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # ---

    
    particle.show()
    particle.look(walls)
    particle.update(pygame.mouse.get_pos())
    
    for wall in walls:
        wall.show()


    #if point is not None:
    #    pygame.draw.circle(screen, (255, 255, 255), (int(point[0]), int(point[1])), 10)
    
    # ---
    pygame.display.flip()


# ---





