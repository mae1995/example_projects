#   AUTHOR  :   Michael A. Eckhardt
#   Date    :   24.08.2019
#
#   Title   :   BezierCurve 02
#
#   


import pygame, math, random
from pygame.math import Vector2

# --- Classes ---
class BezierCurve:
    def __init__(self, screen, p1, p2, p3):
        self.screen = screen

        self.b_1 = Boundary(screen, p1, p2, (255, 125, 125))
        self.b_2 = Boundary(screen, p3, p1, (255, 125, 125))
        self.b_3 = Boundary(screen, p2, p3, (255, 125, 125))

        self.point_0 = self.b_1.start_pos   #
        self.point_2 = self.b_3.start_pos   #   <- Definition like in Wikipedia-Page
        self.point_1 = self.b_2.start_pos   #

        self.Boundaries = [self.b_1, self.b_2, self.b_3]
        self.points = []

    def Show_Lines(self):
        for boundary in self.Boundaries:
            boundary.draw_boundary()

    def Move_Boundaries(self, mouse_pressed, mouse_pos):
        for boundary in self.Boundaries:
            boundary.move_points(mouse_pressed, mouse_pos)

       
    def CreatePoints(self):  
        self.point_0 = self.b_1.start_pos
        self.point_2 = self.b_3.start_pos
        self.point_1 = self.b_2.start_pos

        b0_x = self.point_0[0]
        b0_y = self.point_0[1]
        b1_x = self.point_1[0]
        b1_y = self.point_1[1]
        b2_x = self.point_2[0]
        b2_y = self.point_2[1]

        pieces = 1000

        self.points = []

        for num in range(0, pieces):
            t = num / pieces

            result_x = ((b0_x - (2*b1_x) + b2_x) * (t*t)) + ((-2*b0_x + 2*b1_x) * t) + b0_x
            result_y = ((b0_y - (2*b1_y) + b2_y) * (t*t)) + ((-2*b0_y + 2*b1_y) * t) + b0_y

            self.points.append((result_x, result_y))

    def ShowPoints(self):
        for point in self.points:
            p_x = point[0] - 1
            p_y = point[1] - 1

            pygame.draw.ellipse(self.screen, (255,0,0), (p_x, p_y, 1, 1))
    

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

bc_1 = BezierCurve(screen, (400,200), (100, 400), (50, 50))
bc_2 = BezierCurve(screen, (300,200), (100, 500), (60, 50))
bc_3 = BezierCurve(screen, (200,200), (100, 200), (50, 70))

arr_bc = [bc_1, bc_2, bc_3]

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

    for bc in arr_bc:
        bc.Show_Lines()
        bc.Move_Boundaries(mouse_pressed, mouse_pos)
        bc.CreatePoints()
        bc.ShowPoints()

    
    pygame.display.flip()
