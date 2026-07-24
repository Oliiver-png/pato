import pygame
import sys
from scripts.personajes import FisicasPersonaje
from scripts.herramientas import cargar_imagen

# pygame setup
class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Duck Game") # titulo del juego

        self.screen = pygame.display.set_mode((640, 610)) #tamaño de la ventana
        self.display = pygame.Surface((320, 305)) #superficie de dibujo

        self.clock = pygame.time.Clock() #define el reloj para controlar los FPS

        self.movement = [False, False] # [arriba, abajo, izquierda, derecha]
       
        self.player = FisicasPersonaje(self, 'player', (10, 152), (32, 32)) 

        self.assets = {
            'player': cargar_imagen('personajes/player/duck.png')
        }
    def run(self):
        while True:
            self.display.fill((14, 219, 248))

            self.tilemap.render(self.display)       

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0, 0))
            pygame.display.update()
            self.clock.tick(60) #limita los FPS a 60

Game().run()
