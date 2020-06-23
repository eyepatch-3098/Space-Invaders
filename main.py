import pygame                               #pygame package loaded

pygame.init()                               #pygame initialised

screen=pygame.display.set_mode((800,600))   #screen created

#TITLE AND ICON
pygame.display.set_caption("RULER SUCKS ASS")
icon=pygame.image.load("hen_1.png")
pygame.display.set_icon(icon)

#PLAYER
player_img=pygame.image.load("ruler.png")
playerX=370                                 #player's X coordinate
playerY=480                                 #player's Y coordinate
playerX_change=0                            #change in X position of the player

def player(x,y):                            #to draw the player on given coordinates
    screen.blit(player_img,(x,y))

#GAME LOOP
running=True                                #screen running truth check
while running:

    # hex value
    col=pygame.Color("#09094D")
    screen.fill(col)

    for event in pygame.event.get():        #to quit game
        if event.type==pygame.QUIT:
            running=False

        #check if a key has been pressed
        if event.type==pygame.KEYDOWN:
            #check left and right movement
            if event.key==pygame.K_LEFT:
                playerX_change=-0.2
            if event.key==pygame.K_RIGHT:
                playerX_change=0.2

        #check if key is released
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0

    #registering the change in position
    playerX+=playerX_change

    #make game borders
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
        
    player(playerX,playerY)

    pygame.display.update()