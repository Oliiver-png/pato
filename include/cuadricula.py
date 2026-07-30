import pygame
import json
import os
import config

class Cuadricula:
    def __init__(self):
        self.original_images = {}
        self.tiles_images = {}
        self.nivel_data = None
        self.matriz_tiles = {} # Almacena los tiles del mundo (se mueven con la cámara)
        self.matriz_fija = {}  # Almacena los tiles de UI del menú inferior (fijos en pantalla)
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
                            img.set_colorkey((255, 255, 255)) # Quitar fondo blanco de los tiles
                            self.original_images[key] = img
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
        
        # El tamaño de los bloques es fijo a 64x64 para permitir niveles verticales
        self.tile_height = 64
        self.tile_width = 64
        
        # num_x y num_y ahora solo sirven para definir "qué tan largo y alto" es el nivel para la cámara
        
        # Escalar las imágenes originales a este nuevo tamaño
        for key, img in self.original_images.items():
            self.tiles_images[key] = pygame.transform.scale(img, (self.tile_width, self.tile_height))
            
        # Parsear las posiciones (vienen en formato "x,y")
        self.matriz_tiles = {}
        tiles_raw = level_data.get("tiles", {})
        for coord_str, tile_name in tiles_raw.items():
            if tile_name == "aire":
                continue
            if tile_name in self.original_images or tile_name == "meta":
                try:
                    x, y = map(int, coord_str.split(','))
                    self.matriz_tiles[(x, y)] = tile_name
                except ValueError:
                    pass

    def appendBottomLevel(self, level_data):
        """
        Añade otro nivel en la parte inferior de la cuadrícula actual (ej. para un menú inferior).
        Los tiles de este nivel se añaden a matriz_fija, por lo que no se moverán con la cámara
        ni tendrán colisiones en el mundo del juego.
        """
        menu_num_y = level_data.get("Cuadricula", {}).get("num_y", 0)
        pantalla_tiles_y = config.SCREEN_SIZE[1] // 64
        offset_y = pantalla_tiles_y - menu_num_y
        
        # Asegurarnos de que el tamaño sea 64
        self.tile_height = 64
        self.tile_width = 64
        
        for key, img in self.original_images.items():
            self.tiles_images[key] = pygame.transform.scale(img, (self.tile_width, self.tile_height))
            
        tiles_raw = level_data.get("tiles", {})
        for coord_str, tile_name in tiles_raw.items():
            if tile_name == "aire":
                continue
            if tile_name in self.original_images:
                try:
                    x, y = map(int, coord_str.split(','))
                    # Guardamos en matriz_fija para que actúen como UI superpuesta
                    self.matriz_fija[(x, y + offset_y)] = tile_name
                except ValueError:
                    pass

    def render_world(self, screen, camera_x=0, camera_y=0):
        """Dibuja los tiles del mundo."""
        for (x, y), tile_name in self.matriz_tiles.items():
            img = self.tiles_images.get(tile_name)
            if img:
                pos_x = (x * self.tile_width) - camera_x
                pos_y = (y * self.tile_height) - camera_y
                # Solo dibujar si está (al menos parcialmente) dentro de la pantalla
                if pos_x + self.tile_width > 0 and pos_x < config.SCREEN_SIZE[0] and pos_y + self.tile_height > 0 and pos_y < config.SCREEN_SIZE[1]:
                    screen.blit(img, (pos_x, pos_y))

    def render_ui(self, screen):
        """Dibuja los tiles de la interfaz gráfica (UI)."""
        for (x, y), tile_name in self.matriz_fija.items():
            img = self.tiles_images.get(tile_name)
            if img:
                pos_x = (x * self.tile_width)
                pos_y = y * self.tile_height
                if pos_x + self.tile_width > 0 and pos_x < config.SCREEN_SIZE[0]:
                    screen.blit(img, (pos_x, pos_y))

    def obtener_colisiones(self):
        """
        Devuelve una lista de pygame.Rect correspondientes a los tiles sólidos.
        Solo se toman en cuenta los tiles del mundo (matriz_tiles) para evitar chocar con la UI.
        """
        rects = []
        for (x, y), tile_name in self.matriz_tiles.items():
            if tile_name != "meta":
                pos_x = x * self.tile_width
                pos_y = y * self.tile_height
                rects.append(pygame.Rect(pos_x, pos_y, self.tile_width, self.tile_height))
        return rects
        
    def obtener_rects_por_tipo(self, tipo):
        """Devuelve una lista de pygame.Rect para todos los tiles de un tipo específico."""
        rects = []
        for (x, y), tile_name in self.matriz_tiles.items():
            if tile_name == tipo:
                pos_x = x * self.tile_width
                pos_y = y * self.tile_height
                rects.append(pygame.Rect(pos_x, pos_y, self.tile_width, self.tile_height))
        return rects
