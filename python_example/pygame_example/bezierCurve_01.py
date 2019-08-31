#   AUTHOR  :   Michael A. Eckhardt
#   Date    :   24.08.2019
#
#   Title   :   BezierCurve 01
#
#   


import pygame, math, random
from pygame.math import Vector2

# --- Classes ---

class BezierCurve:

    def __init__(self, screen, p1, p2, p3):
        self.point_0 = p1   #
        self.point_2 = p2   #   <- Definition like in Wikipedia-Page
        self.point_1 = p3   #

        self.points = []

        self.screen = screen

    def ShowControlPoints(self):
        width = 6
        height = 6

        p1_x = self.point_0[0] - (width / 2)
        p1_y = self.point_0[1] - (height / 2)
        p2_x = self.point_2[0] - (width / 2)
        p2_y = self.point_2[1] - (height / 2)
        p3_x = self.point_1[0] - (width / 2)
        p3_y = self.point_1[1] - (height / 2)

        pygame.draw.ellipse(self.screen, (255,255,255), (p1_x, p1_y, width, height))
        pygame.draw.ellipse(self.screen, (255,255,255), (p2_x, p2_y, width, height))
        pygame.draw.ellipse(self.screen, (255,255,255), (p3_x, p3_y, width, height))

    def ShowControlLines(self):
        pygame.draw.line(self.screen, (125,125,125), self.point_0, self.point_2)
        pygame.draw.line(self.screen, (125,125,0), self.point_0, self.point_1)
        pygame.draw.line(self.screen, (125,125,0), self.point_2, self.point_1)

    def ShowPoints(self):
        for point in self.points:
            p_x = point[0] - 1
            p_y = point[1] - 1

            pygame.draw.ellipse(self.screen, (255,0,0), (p_x, p_y, 1, 1))

    def CreatePoints(self):
        b0_x = self.point_0[0]
        b0_y = self.point_0[1]
        b1_x = self.point_1[0]
        b1_y = self.point_1[1]
        b2_x = self.point_2[0]
        b2_y = self.point_2[1]

        pieces = 1000

        for num in range(0, pieces):
            t = num / pieces

            result_x = ((b0_x - (2*b1_x) + b2_x) * (t*t)) + ((-2*b0_x + 2*b1_x) * t) + b0_x
            result_y = ((b0_y - (2*b1_y) + b2_y) * (t*t)) + ((-2*b0_y + 2*b1_y) * t) + b0_y

            self.points.append((result_x, result_y))
        



# --- Main ---
screen      =   pygame.display.set_mode((800, 600))
clock       =   pygame.time.Clock()
isRunning   =   True

bc_1 = BezierCurve(screen, (400,200), (100, 400), (50, 50))



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


    bc_1.ShowControlPoints()
    bc_1.ShowControlLines()

    bc_1.CreatePoints()
    bc_1.ShowPoints()

    
    pygame.display.flip()
