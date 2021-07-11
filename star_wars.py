import random 
import pygame
import math
from pygame import mixer


########### Initialising Pygame
pygame.init()


########### Screen settings
screen = pygame.display.set_mode((800,600))

mixer.music.load("btmusic.mp3")
mixer.music.play(-1)
# mixer.music.get_volume()=0.4


######### Icon and header
pygame.display.set_caption("Star Wars")
ico=pygame.image.load("light.png")
pygame.display.set_icon(ico)


######### Background + Game Over saber
background=pygame.image.load("bagc.gif")
saber=pygame.image.load("linest.png")



######### Player controls and UX
playerImg= pygame.image.load("ufon.png")
player_x=360
player_y=490
x_change=0

def playerWeapon(x,y):
    screen.blit(playerImg, (x,y))



######### Enemy controls and UX
EnemyImg=[]
enemy_x=[]
enemy_y=[]
x_change_e=[]
y_change_e=[]
for i in range(0,6):
    EnemyImg.append(pygame.image.load("alien.png"))
    enemy_x.append(random.randint(0,736))
    enemy_y.append(random.randint(20,180))
    x_change_e.append(0.4)
    y_change_e.append(134)

def EnemyStrike(x,y,i):
    screen.blit(EnemyImg[i], (x,y))    



######### Bullet Firing 
bulletImg= pygame.image.load("bullets.png")
bullet_x=360
bullet_y=390
x_change_b=0
y_change_b=2
b_state="static"

def bulletFire(x,y):
    global b_state
    b_state="fired"
    screen.blit(bulletImg,(x+18,y+10))


######### Collide function for Bullet and Alien
def collide(x1,x2,y1,y2):
    dist= math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,20))
    if dist<27:
        return True
    else:
        return False


######### Score Meter
points=0
font=pygame.font.Font("freesansbold.ttf", 30)

def scorer(x,y):
    score=font.render("Score: " + str(points), True, (255,255,255))
    screen.blit(score, (x,y))


######### Game Over Display
over_font=pygame.font.Font("freesansbold.ttf", 80)

def Game_Over():
    over=over_font.render("Game Over", True, (255,255,255))    
    screen.blit(over, (200,250))

#
running=True

#Before MainLoop
#########################################################################
#MainLoop Starts

while running:

######### Normal Display
    screen.blit(background, (0,0))
    screen.blit(saber, (20,300))

######### Loop for running the game infinitely
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False 

################## Control Key Setup
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                x_change= 1

            if event.key==pygame.K_LEFT:
                x_change= -1   

            if event.key==pygame.K_SPACE:
                fireMusic = mixer.Sound("fire.wav")
                fireMusic.play()
                fireMusic.set_volume(0.2)
                if b_state=="static":
                    bullet_x=player_x
                    bulletFire(bullet_x,bullet_y)       


        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
                x_change= 0                      

       
        

######### Player Motion
    player_x += x_change

    if player_x<=0:
        player_x=0
    elif player_x>=736:
        player_x=736



######### Alien Motion
    for i in range(6):


        if enemy_y[i]>=380:
            for j in range(6):
                enemy_y[j]=1000
            Game_Over()

        enemy_x[i] += x_change_e[i]

        if enemy_x[i]<=0:
            x_change_e[i]=0.4
            enemy_y[i] += y_change_e[i]
        elif enemy_x[i] >= 736:
            x_change_e[i] = -0.4
            enemy_y[i] += y_change_e[i]
        


######### Hitting Enemy

        collision=collide(bullet_x,enemy_x[i],bullet_y,enemy_y[i])
        if collision:
            bullet_y=390
            b_state="static"
            points+=1
            enemy_y[i]=random.randint(20,180)
            enemy_x[i]=random.randint(0,736)

            blastSound=mixer.Sound("blast.wav")
            blastSound.play()
            # blast)

        EnemyStrike(enemy_x[i],enemy_y[i],i)

        


######### Bullet Firing
    if bullet_y<=0:
        bullet_y=390
        b_state="static"

    if b_state=="fired":
        bullet_y -= y_change_b
        bulletFire(bullet_x,bullet_y)




######### Player Call + Score display
    playerWeapon(player_x, player_y)
    scorer(10,10)


    pygame.display.update()   