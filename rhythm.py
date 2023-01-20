import pygame
import numpy
import math
from random import *

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([1000, 500])
laneone = []
lanetwo = []
lanethree = []
lanefour = []
alllanes = [laneone, lanetwo, lanethree, lanefour]
timingindicators = []
score = 0

notecolor = (91, 35, 51)
margin = (screen.get_width() - 360)/2

clock = pygame.time.Clock()

class Note:
    def __init__(self):
        self.position = -30
        self.killpos = 500
        self.speed = 350
        self.height = 30
        self.forgiveness = 5
    def update(self,time):
        self.position += self.speed * time
    def hit(self):
        global timingindicators,score
        centeredpos = self.position + (self.height/2)
        scored = abs(centeredpos - 460)
        score += math.floor(-scored + 35)
        color = (0,0,0)
        if scored <= 35:
            color = (scored >= 10 and (255,255,0) or (0,255,0))
        else:
            color = (255,0,0)
        timingindicators.append(indicator(scored * (centeredpos - 460 < 0 and -1 or 1),color))
        return (scored <= self.height + self.forgiveness)

class indicator:
    def __init__(self,position,color):
        self.timeleft = 1
        self.pos = position
        self.col = color
running = True

laneone.append(Note())

timer = 0.3

while running:
    deltatime = clock.tick(clock.get_fps())/1000

    timer -= deltatime
    if timer <= 0:
        timer = 0.3
        alllanes[randint(0,len(alllanes)-1)].insert(len(alllanes),Note())

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and len(laneone) > 0:
                hit = laneone[0].hit()
                if hit:
                    laneone.pop(0)
            if event.key == pygame.K_s and len(lanetwo) > 0:
                hit = lanetwo[0].hit()
                if hit:
                    lanetwo.pop(0)
            if event.key == pygame.K_k and len(lanethree) > 0:
                hit = lanethree[0].hit()
                if hit:
                    lanethree.pop(0)
            if event.key == pygame.K_l and len(lanefour) > 0:
                hit = lanefour[0].hit()
                if hit:
                    lanefour.pop(0)
                
    
    screen.fill((21, 72, 63))
    #bg
    pygame.draw.rect(screen, (51, 102, 93),pygame.rect.Rect(margin,0,320,500))

    #hitline
    pygame.draw.rect(screen, (171, 154, 89),pygame.rect.Rect(margin,460-15,320,30))
    #lanelines
    for i in range(0,5):
        pygame.draw.rect(screen, (255,175,135),pygame.rect.Rect((80 * i) + margin,0,1,500))

    for i, lane in enumerate(alllanes):
        if len(lane) > 0:
            for num, note in enumerate(lane):
                note.update(deltatime)
                pygame.draw.rect(screen, notecolor, pygame.rect.Rect(margin + (80*i),note.position,80,note.height))
                if note.position >= note.killpos:
                    lane.pop(num)

    if len(timingindicators) > 0:
        for i, ind in enumerate(timingindicators):
            pygame.draw.rect(screen, ind.col, pygame.rect.Rect((screen.get_width() / 2) + ind.pos - 4,500-16,8,8))
            ind.timeleft -= deltatime
            if ind.timeleft <= 0:
                timingindicators.pop(i)

    pygame.display.flip()

pygame.quit()