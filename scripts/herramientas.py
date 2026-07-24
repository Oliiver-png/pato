import pygame

DIRECCION_IMG = 'datos/imagenes/'

def cargar_imagen(direccion):
   imagen = pygame.image.load(DIRECCION_IMG + direccion).convert_alpha()
   imagen.set_colorkey((0, 0, 0))
   return imagen