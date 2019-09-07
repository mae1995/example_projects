import pygame


# --- Init ---
pygame.init()


# --- Variables ---
screen      =   pygame.display.set_mode((800, 600))
clock       =   pygame.time.Clock()
isRunning   =   True

game_field  =   (300, 500) 
field_size  =   25

curr_figure =   [[0,0,0]
                ,[0,1,0]
                ,[1,1,1]]

# --- Methods ---
def Draw_Figure():
    startpos_x = 75
    startpos_y = 0

    x = 1
    y = 1

    for fig_map in curr_figure:
        x = 1
        
        for box in fig_map:
            if box == 1:
                pygame.draw.rect(screen, (0,255,255), ((startpos_x + 25 * x , startpos_y + 25 * y), (25,25)))
            x += 1

        y += 1   

def Draw_Field():
    # --- DRAW AREA ---
    pygame.draw.rect(screen, (125, 125, 125), ((50,50), game_field))
    pygame.draw.rect(screen, (0, 0, 0), ((75,50), (game_field[0] - 50, game_field[1] - 25)))

    # --- DRAW BOXES ---
    posX = 75
    posY = 50

    fieldNr = 0
    color = (200, 200, 200)
    
    while posX <= game_field[0]:
        posY = 50

        while posY <= game_field[1]:
            fieldNr += 1

            if(fieldNr % 2 == 0):
                color = (200, 200, 200)
            else:
                color = (175, 175, 175)

            pygame.draw.rect(screen, color, ((posX ,posY), (25,25)))
            posY += 25
        
        posX += 25

# --- Main Loop ---
while isRunning:

    clock.tick(30)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

                

    Draw_Field()
    Draw_Figure()
 
        

    pygame.display.flip()

