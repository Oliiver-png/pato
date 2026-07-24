import pygame
import config

image_cache = {}

def preloadAssets(paths):
    """Carga imágenes en memoria para un acceso más rápido."""
    for path in paths:
        if path not in image_cache:
            try:
                image_cache[path] = pygame.image.load(path).convert_alpha()
                if config.DEBUG:
                    print("Pre-cargada:", path)
            except FileNotFoundError:
                if config.DEBUG:
                    print(f"[WARNING] preloadAssets no encontró la imagen: {path}")

def get_image(path):
    """Obtiene una imagen de la caché o la carga si no existe."""
    if path not in image_cache:
        try:
            image_cache[path] = pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"[ERROR] No se pudo cargar la imagen {path}: {e}")
            return None
    return image_cache[path]

def pollEvents():
    """Procesa los eventos básicos como cerrar la ventana."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.running = False
