import pygame  # pygame package loaded
import random  # random package loaded
import math  # math package loaded
from pygame import mixer  # mixer package loaded

pygame.init()  # pygame initialised

screen = pygame.display.set_mode((1200, 700))  # screen created

# BACKGROUND
background = pygame.image.load("space.png")

# BACKGROUND SOUND
mixer.music.load("background_space.wav")
mixer.music.play(-1)  # to play on loop

# TITLE AND ICON
pygame.display.set_caption("SPACE WARS")
icon = pygame.image.load("astro_icon.png")
pygame.display.set_icon(icon)

# PLAYER
player_img = pygame.image.load("spaceship.png")
playerX = 370  # player's X coordinate
playerY = 480  # player's Y coordinate
playerX_change = 0  # change in X position of the player

# ENEMY LIST REGISTER
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 20

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("enemyship.png"))
    enemyX.append(random.randint(0, 735))  # enemy's random X coordinate
    enemyY.append(random.randint(50, 150))  # enemy's random Y coordinate
    enemyX_change.append(10)  # change in X position of the enemy
    enemyY_change.append(20)  # change in Y position of the enemy

# BULLET
bullet_img = pygame.image.load("shoot.png")
bulletX = 0  # bullet's random X coordinate
bulletY = 480  # bullet's random Y coordinate
bulletX_change = 0  # change in X position of the bullet
bulletY_change = 30  # change in Y position of the bullet
bullet_state = "ready"  # ready state means bullet not visible

# SCORE
score_value = 0
font = pygame.font.Font("cartoon_text.ttf", 30)
textX, textY = 10, 10

# GAME OVER TEXT
over_font = pygame.font.Font("cartoon_text.ttf", 56)


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER \n SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (140, 250))


def player(x, y):  # to draw the player on given coordinates
    screen.blit(player_img, (x, y))


def enemy(x, y, i):  # to draw the player on given coordinates
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):  # to be invoked when we fire the bullet
    global bullet_state  # to access the state of bullet from main
    bullet_state = "fire"  # bullet currently being fired
    screen.blit(bullet_img, (x, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 32:
        return True
    else:
        return False


# GAME LOOP
running = True  # screen running truth check
while running:

    # RGB
    screen.fill((0, 0, 0))

    # BACKGROUND IMAGE ADD
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # to quit game
        if event.type == pygame.QUIT:
            running = False

        # check if a key has been pressed
        if event.type == pygame.KEYDOWN:
            # check left and right movement
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # only fire when ready
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # stores playerX position and fires bullet from there
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # check if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # registering the change in position of player
    playerX += playerX_change

    # make game borders for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):  # to display multiple enemies

        # GAME OVER
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break

        # registering the change in position of enemy
        enemyX[i] += enemyX_change[i]

        # make game borders for enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -6
            enemyY[i] += enemyY_change[i]

        # COLLISION
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision == True:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)  # enemy's random X coordinate (respawn)
            enemyY[i] = random.randint(50, 150)  # enemy's random Y coordinate (respawn)


        # CALLING ENEMY FUNCTION
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # CALLING PLAYER FUNCTION
    player(playerX, playerY)

    # CALLING FUNCTION TO RENDER THE SCORE VALUE
    show_score(textX, textY)

    pygame.display.update()
