import pygame
from pygame.locals import QUIT,MOUSEBUTTONDOWN as MBD
from math import sin, cos, radians
from random import randint
pygame.init()
pygame.display.set_caption("Straight Fishing")
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
w, h = screen.get_size()
s = min(w, h)
t = 0

#Water top
wtrtop = pygame.image.load("assets/water_top.png").convert_alpha()
wtrtop = pygame.transform.rotozoom(wtrtop,0,
w//100)
wtrtopr = wtrtop.get_rect()
wtrtopr.top = h//10

wtrs = [wtrtopr.copy() for _ in range(7)] 
for i in range(7):
    wtrs[i].left = i * (w//7)
    
#Boat
boat = pygame.image.load("assets/boat.png").convert_alpha()
boat = pygame.transform.rotozoom(boat,0,
s//300)
boatr = boat.get_rect()
boatr.right = w
boatr.top = wtrtopr.top

#Stick
stick = pygame.image.load("assets/stick.png").convert_alpha()
stick = pygame.transform.rotozoom(stick,0,
s//200)
stickr = stick.get_rect()
stickr.center = boatr.topleft

#Hook
hook0 = pygame.image.load("assets/hook.png").convert_alpha()
hook0 = pygame.transform.rotozoom(hook0,0,
s//350)  
hookr0 = hook0.get_rect() 
hookr0.center = stickr.topleft
hookr = hookr0.copy()
swing = True
angle = 0
swingf = 0
long = 0
speed = 7 
back = False

#Fishs
fish_red = pygame.image.load("assets/fish_red.png").convert_alpha()
fish_green = pygame.image.load("assets/fish_green.png").convert_alpha()
fish_orange = pygame.image.load("assets/fish_orange.png").convert_alpha()
fish_red = pygame.transform.rotozoom(fish_red, 0,
s//150)  
fish_green = pygame.transform.rotozoom(fish_green, 0,
s//150)  
fish_orange = pygame.transform.rotozoom(fish_orange, 0,
s//150)
fish = [fish_red, fish_green, fish_orange]
fishr = [f.get_rect() for f in fish]
for fr in fishr:
    fr.center = randint(fr.width//2,w), randint(wtrtopr.bottom,h) 
fishvx = [3, 7, 11]
fishvy = [-2, -1, -0.5]

#Win
def win():
    return False
 
#Colors
OCEAN = pygame.color.Color("#1C6BA0")
DEEP = pygame.color.Color("#0F52BA")
SKY = pygame.color.Color("#3B88C8") 
WHITE = pygame.color.Color("#FFFFFF")

#Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT: 
            running = False
        if event.type == MBD:#MOUSEBUTTONDOWN
            if swing:
                swing = False
            else:
                back = True
    #Swing or through
    if swing:
        if swingf and angle < 90:
            angle += 1  
        elif not swingf and angle > -90: 
            angle -= 1
        else:
            swingf = not swingf
        hook = pygame.transform.rotozoom(hook0,angle,1) 
        rad = radians(angle) 
        hookr  = hook.get_rect(center = (
            hookr0.center[0] + (hookr0.height//2) * sin(rad),
            hookr0.center[1] + (hookr0.height//2) * cos(rad)))  
    else:
        if hookr.x >w or hookr.x <0 or hookr.y >h or back:
            back = True
            hookr.x -= sin(rad) * speed
            hookr.y -= cos(rad) * speed
            long -= 1
            if long <= 0: 
                back = False
                swing = True
        else:
            hookr.x += sin(rad) * speed
            hookr.y += cos(rad) * speed
            long += 1
        
    screen.fill(SKY)
    for wtr in wtrs:
        screen.blit(wtrtop,wtr)
    pygame.draw.rect(screen, DEEP, (0, wtrtopr.bottom, w, h))
    screen.blit(boat,boatr)
    screen.blit(stick,stickr)
    pygame.draw.line(screen,WHITE, hookr0.center, (hookr.center[0] + (hookr0.height//-2 ) * sin(rad), hookr.center[1] + (hookr0.height//-2) * cos(rad)), 2)
    screen.blit(hook,hookr)
    for i in range(3):
       if not fishr[i]:
           continue
       elif fishr[i].colliderect(hookr): 
            fishr[i].center = hookr.center
            if long == 0:
                fishr[i] = None
                continue 
       else:
            if fishr[i].x < 0 or fishr[i].x > w:
                fishvx[i] *= -1
                fish[i] = pygame.transform.flip(fish[i], True, False)
            if fishr[i].y < wtrtopr.bottom or fishr[i].y > h: 
                fishvy[i] *= -1
            fishr[i].x += fishvx[i]
            fishr[i].y += fishvy[i]
       screen.blit(fish[i],fishr[i])
    if fishr == [None for _ in range(3)]:
        running = win()
    pygame.display.update()
pygame.quit()