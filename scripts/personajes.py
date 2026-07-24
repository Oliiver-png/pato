import math
import random

import pygame

class FisicasPersonaje:
    def __init__(self, game, e_type, pos, size):
        self.game = game 
        self.type = e_type
        self.pos = list(pos) #da a cada personaje su propia lista de posición para que no se muevan todos juntos
        self.size = size
        self.velocity = [0, 0] #vector velocidad inicializado en 0
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        
    def update(self, movement):

        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}        

        #determina el movimiento del personaje en cada frame sumando la velocidad a la posición
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[0] += frame_movement[0] #movimiento horizontal del personaje
        entity_rect = self.rect()

        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x        

        self.pos[1] += frame_movement[1] #movimiento vertical del personaje
        entity_rect = self.rect()
        
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        
    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos) #dibuja el personaje en la pantalla en la posición actual

