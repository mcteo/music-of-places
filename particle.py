#!/usr/bin/env python

import random, colorsys
import pygame as pg
from pygame.locals import *

if not pg.font: print 'Warning, fonts disabled'
if not pg.mixer: print 'Warning, sound disabled'

NUM_PARTICLES = 1000
CONTINUOS = True
SPEED_BLEED_FACTOR = 0.98
MAX_FPS = 30

class Particle:

    def __init__(self, surface, size):
        self.surface = surface
        self.screen_width = size[0]
        self.screen_height = size[1]
        self.x = (random.randrange(self.screen_width * 10) / 10)
        self.y = (random.randrange(self.screen_height * 10) / 10)
        self.ox = 0.0
        self.oy = 0.0
        self.vx = (random.randrange(20) - 10)
        self.vy = (random.randrange(20) - 10)
        self.colour = (255, 0, 0)

    def draw(self):
         
        self.ox = self.x
        self.oy = self.y
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        
        if self.x < 0:
            self.x = 0
            self.vx = -self.vx
            
        if self.x > self.screen_width:
            self.x = self.screen_width
            self.vx = -self.vx

        if self.y < 0:
            self.y = 0
            self.vy = -self.vy

        if self.y > self.screen_height:
            self.y = self.screen_height
            self.vy = -self.vy
            
        self.vx = self.vx * SPEED_BLEED_FACTOR
        self.vy = self.vy * SPEED_BLEED_FACTOR

        pg.draw.line(self.surface, self.colour, (self.ox, self.oy), (self.x, self.y), 3)

    def set_colour(self, colour):
        self.colour = colour
        
def main():
        
    pg.init()
    screen = pg.display.set_mode((1280, 960))#, pg.FULLSCREEN)
    pg.display.set_caption('Particles')

    height, width = screen.get_size()
    bg = pg.Surface((height, width))
    bg = bg.convert()
    bg.fill((0, 0, 0))
    
    particles = []
    for i in range(NUM_PARTICLES):
        particles.append(Particle(bg, screen.get_size()))
    mx, my = -1, -1
        
    screen.blit(bg, (0, 0))
    pg.display.flip()
        
    clock = pg.time.Clock()
    
    max_dist = (((width**2) + (height**2))**0.5)
    
    while 1:
        clock.tick(MAX_FPS)

        for event in pg.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == 27:
                    return
            if CONTINUOS == True:
                if event.type == MOUSEMOTION:
                    mx, my = event.pos
            elif CONTINUOS == False:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button in (1, 2, 3):
                        mx, my = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mx, my = -1, -1
            """
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play() #punch
                    chimp.punched()
                else:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()
            """
           
         
        if (mx != -1) and (my != -1):
            a = 5
            for p in particles:
                d = ((p.x - mx) * (p.x - mx)) + ((p.y - my) * (p.y - my))
                d = (d**0.5)
                
                if d > 0:
                    p.vx = p.vx - (a / d) * (p.x - mx)
                    p.vy = p.vy - (a / d) * (p.y - my)
                
                    (h, s, v) = colorsys.rgb_to_hsv(p.colour[0], p.colour[1], p.colour[2])
                    h = (1.0 * d) / max_dist
                    p.set_colour((colorsys.hsv_to_rgb(h, s, v)))
                
        bg.fill((0, 0, 0))
        for particle in particles:
            particle.draw()

        screen.blit(bg, (0, 0))
        pg.display.flip()

if __name__ == "__main__":
    main() 
