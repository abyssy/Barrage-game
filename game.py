# Import
import pygame
import math
import random
from pygame.locals import *

# Initialize the game
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption("Help rabbit!")
enemytimer = 100
enemytimer1 = 0
enemytimer2 = 0
badguys = [[640,100]]
enemys = [[100, 480]]
healthvalue = 194
boss = [400, 300]
speed = [1, 1]
bosstimer = 30
keys = [False, False, False, False]
playerpos = [100,100]
acc = [0,0]
arrows = []
pygame.mixer.init()

# Load images
enemyimg1 = pygame.image.load("images/badguy2.png")
bossimg = pygame.image.load("images/kid.png")
player = pygame.image.load("images/dude.png")
backimg = pygame.image.load("images/grass.png")
arrow = pygame.image.load("images/bullet.png")
badguyimg1 = pygame.image.load("images/badguy4.png")
healthbar = pygame.image.load("images/healthbar.png")
health = pygame.image.load("images/health.png")
gameover = pygame.image.load("images/gameover.png")
youwin = pygame.image.load("images/youwin.png")
start = pygame.image.load("images/start5.png")
pygame.mixer.music.load('PUPA.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)
badguyimg = badguyimg1
enemyimg = enemyimg1

# start page
running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = 0
                break
    screen.blit(start, (0,0))
    pygame.display.flip()

# start
running = 1
exitcode = 0
while running:
    enemytimer -= 1
    bosstimer -= 1
    screen.fill(0)
    
    # draw the screen elements
    for x in range(10):
        for y in range(10):
            screen.blit(backimg,(100 * x,100 * y))
    screen.blit(bossimg, boss)
    
    # Set player position and rotation
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)
    
    # Draw arrows
    for bullet in arrows:
        index=0
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] <- 0 or bullet[1] > 640 or bullet[2] <- 0 or bullet[2] > 480:
            arrows.pop(index)
        index+=1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
            
    # Draw boss
    velx = 1
    vely = 1
    if bosstimer == 0:
        velx = random.randint(-3, 3)
        vely = random.randint(-3, 3)
        bosstimer = 50
    if boss[1] + velx >= 560:
        velx = 0 - velx
    if boss[1] + velx <= 150:
        velx = 0 - velx
    if boss[0] + vely >= 400:
        vely = 0 - vely
    if boss[0] + vely <= 50:
        vely = 0 - vely
    boss[0] += velx
    boss[1] += vely
    
    # Draw badgers
    if enemytimer <= 0:
        enemys.append([random.randint(50,590), 0])
        badguys.append([640, random.randint(50,430)])
        enemytimer = 100 - (enemytimer1 * 2)
        if enemytimer1 >= 35:
            enemytimer1 = 35
        else:
            enemytimer1 += 5
    
    # Check for death
    playrect = pygame.Rect(player.get_rect())
    playrect.top = playerpos[1]
    playrect.left = playerpos[0]
    index=0
    for badguy in badguys:
        badguyrect = pygame.Rect(badguyimg.get_rect())
        badguyrect.top = badguy[1]
        badguyrect.left = badguy[0]
        if playrect.colliderect(badguyrect):
            #Lose check
            badguys.pop(index)
            running = 0
            exitcode = 0
        if badguy[0] <= 0:
            badguys.pop(index)
        badguy[0] -= 7
        index += 1

    index1 = 0
    for badguy in badguys:
        screen.blit(badguyimg, badguy)
    for enemy in enemys:
        enemyrect = pygame.Rect(enemyimg.get_rect())
        enemyrect.top = enemy[1]
        enemyrect.left = enemy[0]
        if playrect.colliderect(enemyrect):
            #Lose check
            enemys.pop(index1)
            running = 0
            exitcode = 0
        if enemy[1] >= 480:
            enemys.pop(index1)
        enemy[1] += 5
        index1 += 1

    # Check for attack
    index2 = 0
    bossrect = pygame.Rect(bossimg.get_rect())
    bossrect.top = boss[1]
    bossrect.left = boss[0]
    for bullet in arrows:
        bullrect = pygame.Rect(arrow.get_rect())
        bullrect.left = bullet[1]
        bullrect.top = bullet[2]
        if bossrect.colliderect(bullrect):
            acc[0] += 1
            arrows.pop(index2)
            healthvalue -= 5
        index2 += 1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)
    for enemy in enemys:
        screen.blit(enemyimg, enemy)
    
    # Draw health bar
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8))
    
    pygame.display.flip()

    # rabbit moving
    for event in pygame.event.get():
        if event.type==pygame.locals.QUIT:
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key==K_w:
                keys[0]=True
            elif event.key==K_a:
                keys[1]=True
            elif event.key==K_s:
                keys[2]=True
            elif event.key==K_d:
                keys[3]=True
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_w:
                keys[0]=False
            elif event.key==pygame.K_a:
                keys[1]=False
            elif event.key==pygame.K_s:
                keys[2]=False
            elif event.key==pygame.K_d:
                keys[3]=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            position=pygame.mouse.get_pos()
            acc[1]+=1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
    if keys[0]:
        if playerpos[1] in range(2, 480):
            playerpos[1]-=2
        else:
            continue
    elif keys[2]:
        if playerpos[1] in range(0, 478):
            playerpos[1]+=2
        else:
            continue
    if keys[1]:
        if playerpos[0] in range(2, 640):
            playerpos[0]-=2
        else:
            continue
    elif keys[3]:
        if playerpos[0] in range(0, 638):
            playerpos[0]+=2
        else:
            continue
    
    # Win check
    if healthvalue <= 0:
        running = 0
        exitcode = 1
    if acc[1]!=0:
        accuracy=acc[0]*1.0/acc[1]*100
    else:
        accuracy=0

# Win/lose display
pygame.mixer.music.stop()
if exitcode==0: 
    screen.blit(gameover, (0,0))
else:
    screen.blit(youwin, (0,0))

# game over
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
