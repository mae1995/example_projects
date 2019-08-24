#   AUTHOR  :   Michael A. Eckhardt
#   Date    :   24.08.2019
#
#   Title   :   Intersection 01
#
#   


import pygame, math, random
from pygame.math import Vector2

# --- Classes ---

class Boundary:

    def __init__(self, screen, start_pos, end_pos, color):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.screen = screen

        v_p1_x = random.randint(-1, 1)
        v_p1_y = random.randint(-1, 1)
        v_p2_x = random.randint(-1, 1)
        v_p2_y = random.randint(-1, 1)

        if v_p1_x == 0:
            v_p1_x = 1
        
        if v_p1_y == 0:
            v_p1_y = -1

        if v_p2_x == 0:
            v_p2_x = -1
        
        if v_p2_y == 0:
            v_p2_y = 1

        self.v_p1 = (v_p1_x, v_p1_y)
        self.v_p2 = (v_p2_x, v_p2_y)

    def draw_endpoints(self):
        width   = 6
        height  = 6

        s_x = self.start_pos[0] - (width / 2)
        s_y = self.start_pos[1] - (height / 2)

        e_x = self.end_pos[0] - (width / 2)
        e_y = self.end_pos[1] - (height / 2)

        pygame.draw.ellipse(self.screen, self.color, (s_x, s_y, width, height))
        pygame.draw.ellipse(self.screen, self.color, (e_x, e_y, width, height))

    def draw_line(self):
        pygame.draw.line(self.screen, self.color, self.start_pos, self.end_pos)

    def draw_intersection(self, point):
        width   = 6
        height  = 6
        color   = (255,0,0)

        x = point[0] - (width / 2)
        y = point[1] - (height / 2)

        pygame.draw.ellipse(self.screen, color, (x, y, width, height))

    def draw_boundary(self):
        self.draw_endpoints()
        self.draw_line()

    def move_points(self):
        v_speed = random.randint(1, 3)

        pos_x1 = (self.start_pos[0] + (v_speed * self.v_p1[0])) % 400
        pos_y1 = (self.start_pos[1] + (v_speed * self.v_p1[1])) % 400
        pos_x2 = (self.end_pos[0] + (v_speed * self.v_p2[0])) % 400
        pos_y2 = (self.end_pos[1] + (v_speed * self.v_p2[1])) % 400

        self.start_pos = (pos_x1, pos_y1) 
        self.end_pos = (pos_x2, pos_y2)


    def is_collide(self, wall):
        x1 = self.start_pos[0]
        y1 = self.start_pos[1]
        x2 = self.end_pos[0]
        y2 = self.end_pos[1]

        x3 = wall.start_pos[0]
        y3 = wall.start_pos[1]
        x4 = wall.end_pos[0]
        y4 = wall.end_pos[1]

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if den == 0:
            return None

        if den != 0:
            t1 = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
            t2 = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            t = t1 / t2

            u1 = (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)
            u2 = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            u = (u1 / u2) * -1

            if(t >= 0 and t <= 1) and (u >= 0 and u <= 1):
                px = x1 + t * (x2 - x1)
                py = y1 + t * (y2 - y1)

                return (px, py)
    

# --- Main ---
screen      =   pygame.display.set_mode((800, 600))
clock       =   pygame.time.Clock()
isRunning   =   True



wall_1 = Boundary(screen, (21,30), (200, 100), (255,255,255))
wall_2 = Boundary(screen, (70,20), (70, 100), (255,255,0))

walls = [wall_1, wall_2]


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

    for wall in walls:
        wall.draw_boundary()
        wall.move_points()

    pt = wall_1.is_collide(wall_2)
    if pt is not None:
        wall_1.draw_intersection(pt)
        print("intersection : " + str(pt))
    else:
        print("intersection : None")


    
    pygame.display.flip()
