import pygame
import json
import os
import config

class Cuadricula:
    def __init__(self):
        self.tiles_images = {}
        self.nivel_data = None
        self.matriz_tiles = {}
        self.tile_width = 0
        self.tile_height = 0
        self.num_x = 0
        self.num_y = 0
        self._cargar_texturas()
        
    def _cargar_texturas(self):
        """Carga y mapea las texturas desde tiles.json"""
        ruta_tiles = os.path.join(os.path.dirname(__file__), "data", "tiles.json")
        try:
            with open(ruta_tiles, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for key, path in data.items():
                    if path.endswith(".png") or path.endswith(".jpg"):
                        try:
                            # Cargar la imagen original (el path es relativo a la ejecución del main script)
                            img = pygame.image.load(path).convert_alpha()
                            self.tiles_images[key] = img
                        except Exception as e:
                            print(f"[ERROR] No se pudo cargar la imagen {path}: {e}")
        except Exception as e:
            print(f"[ERROR] No se pudo cargar {ruta_tiles}: {e}")

    def loadLevel(self, level_data):
        """
        Carga la información de un nivel (cuadrícula y tiles).
        level_data proviene del NivelManager.aDict()
        """
        self.nivel_data = level_data
        
        # Calcular dimensiones de tiles
        self.num_x = level_data.get("Cuadricula", {}).get("num_x", 1)
        self.num_y = level_data.get("Cuadricula", {}).get("num_y", 1)
        
        # Evitar división por cero
        if self.num_x == 0: self.num_x = 1
        if self.num_y == 0: self.num_y = 1
        
        # Escalar tiles automáticamente para encajar exacto en pantalla
        self.tile_width = config.SCREEN_SIZE[0] // self.num_x
        self.tile_height = config.SCREEN_SIZE[1] // self.num_y
        
        # Escalar las imágenes cargadas a este nuevo tamaño
        for key in self.tiles_images:
            img = self.tiles_images[key]
            self.tiles_images[key] = pygame.transform.scale(img, (self.tile_width, self.tile_height))
            
        # Parsear las posiciones (vienen en formato "x,y")
        self.matriz_tiles = {}
        tiles_raw = level_data.get("tiles", {})
        for coord_str, tile_name in tiles_raw.items():
            if tile_name == "aire":
                pass
            elif tile_name in self.tiles_images:
                try:
                    x, y = map(int, coord_str.split(','))
                    self.matriz_tiles[(x, y)] = tile_name
                except ValueError:
                    pass

    def render(self, screen):
        """Dibuja todos los tiles en la pantalla"""
        for (x, y), tile_name in self.matriz_tiles.items():
            img = self.tiles_images.get(tile_name)
            if img:
                pos_x = x * self.tile_width
                pos_y = y * self.tile_height
                screen.blit(img, (pos_x, pos_y))

    def obtener_colisiones(self):
        """Devuelve una lista de pygame.Rect correspondientes a los tiles sólidos"""
        rects = []
        for (x, y), tile_name in self.matriz_tiles.items():
            pos_x = x * self.tile_width
            pos_y = y * self.tile_height
            rects.append(pygame.Rect(pos_x, pos_y, self.tile_width, self.tile_height))
        return rects
