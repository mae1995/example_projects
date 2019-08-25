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
        self.color_cir_s = (125,125,125)
        self.color_cir_e = (125,125,125)
        self.screen = screen

        self.can_move = False
        self.move_s = False
        self.move_e = False


    def draw_endpoints(self):
        width   = 6
        height  = 6

        s_x = self.start_pos[0] - (width / 2)
        s_y = self.start_pos[1] - (height / 2)

        e_x = self.end_pos[0] - (width / 2)
        e_y = self.end_pos[1] - (height / 2)

        pygame.draw.ellipse(self.screen, self.color_cir_s, (s_x, s_y, width, height))
        pygame.draw.ellipse(self.screen, self.color_cir_e, (e_x, e_y, width, height))

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
        self.draw_line()
        self.draw_endpoints()
        

    def move_points(self, isMousePressed, mouse_pos):
        x1 = self.start_pos[0]
        y1 = self.start_pos[1]
        x2 = self.end_pos[0]
        y2 = self.end_pos[1]

        mx = mouse_pos[0]
        my = mouse_pos[1]

        width = 4
        height = 4

        mouse_above_s = False
        mouse_above_e = False
        mouse_pressed = isMousePressed

        if ((mx - width) < x1) and ((mx + width) > x1) and ((my - height) < y1) and ((my + height) > y1):
            self.color_cir_s = (255,0,255)
            mouse_above_s = True
        else:
            self.color_cir_s = (125,125,125)
            mouse_above_s = False

        if ((mx - width) < x2) and ((mx + width) > x2) and ((my - height) < y2) and ((my + height) > y2):
            self.color_cir_e = (255,0,255)
            mouse_above_e = True
        else:
            self.color_cir_e = (125,125,125)
            mouse_above_e = False

        if mouse_above_s is True and mouse_pressed is True:
            self.move_s = True
            self.can_move = True

        if mouse_above_e is True and mouse_pressed is True:
            self.move_e = True
            self.can_move = True

        if mouse_pressed is False:
            self.move_s = False
            self.move_e = False
            self.can_move = False

        if self.can_move is True:
            if self.move_s is True:
                self.start_pos = mouse_pos
            if self.move_e is True:
                self.end_pos = mouse_pos


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

mouse_pos       =   None
mouse_pressed   = False

wall_1 = Boundary(screen, (21,30), (200, 100), (255,255,255))
wall_2 = Boundary(screen, (70,20), (70, 100), (255,255,0))

walls = [wall_1, wall_2]


# ---
while isRunning:

    clock.tick(30)

    screen.fill((0,0,0))

    mouse_pos = pygame.mouse.get_pos()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pressed = False

    for wall in walls:
        wall.draw_boundary()
        wall.move_points(mouse_pressed, mouse_pos)

    pt = wall_1.is_collide(wall_2)
    if pt is not None:
        wall_1.draw_intersection(pt)
        print("intersection : " + str(pt))
    else:
        print("intersection : None")
        pass


    
    pygame.display.flip()
