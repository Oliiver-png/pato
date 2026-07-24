import pygame

import config
from config import SCREEN_SIZE, MAX_FPS
import include.functions as functions
from include.game_state import game_state

# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Papas Chaza")
clock = pygame.time.Clock()
dt = 0

# Pre-cargar imágenes pesadas y comunes para evitar lag al cambiar de pantalla
images_to_preload = [
]
functions.preloadAssets(images_to_preload)

# Pantalla de inicio / inicio del juego
if game_state.pantalla_actual is None:
    from include.screens.nivel1 import Nivel1
    game_state.pantalla_actual = Nivel1(game_state)
    game_state.pantalla_actual.enter(screen)

#Loop principal
while config.running:
    
    # Limpiar pantalla
    screen.fill((0, 0, 0))
    
    # Actualizar y renderizar pantalla actual (tilemaps, sprites, etc)
    if game_state.pantalla_actual and hasattr(game_state.pantalla_actual, 'update'):
        game_state.pantalla_actual.update(dt, screen)

    # flip() the display to put your work on screen
    pygame.display.flip()
    
    # poll for events
    functions.pollEvents()
    
    # dt is delta time in seconds since last frame
    dt = clock.tick(MAX_FPS) / 1000

pygame.quit()