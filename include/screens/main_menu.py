import pygame
import os
from include.screens.baseScreen import Screen
from include import functions
import config

class MainMenu(Screen):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.background = pygame.Surface(config.SCREEN_SIZE)
        self.load_background()
        
        self.action_key_was_pressed = False
        self.mouse_was_pressed = False
        
        # Areas de los botones
        self.btn_jugar = pygame.Rect(355, 250, 205, 70)
        self.btn_opciones = pygame.Rect(355, 345, 205, 70)
        
    def load_background(self):
        base_path = os.path.join(os.path.dirname(__file__), "..", "..", "datos", "imagenes", "menu")
        
        cols = 10
        rows = 9
        tile_w = config.SCREEN_SIZE[0] // cols
        tile_h = config.SCREEN_SIZE[1] // rows
        
        # Cargar los 90 tiles y ensamblarlos en el fondo
        for i in range(1, 91):
            path = os.path.join(base_path, f"_{i}.png")
            img = functions.get_image(path)
            
            idx = i - 1
            x = (idx % cols) * tile_w
            y = (idx // cols) * tile_h
            
            if img:
                # Escalar el tile por si su resolución no coincide exactamente con tile_w/tile_h
                img = pygame.transform.scale(img, (tile_w, tile_h))
                self.background.blit(img, (x, y))
            else:
                # Fallback si no encuentra un tile
                pygame.draw.rect(self.background, (255, 0, 255), (x, y, tile_w, tile_h))

    def enter(self, screen):
        print("Menu Principal")
        self.action_key_was_pressed = True # Para evitar saltar instantáneamente
        self.mouse_was_pressed = True
        
    def update(self, dt, screen):
        # Dibujar el fondo ensamblado
        screen.blit(self.background, (0, 0))
        
        # Obtener entradas
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        keys = pygame.key.get_pressed()
        
        # Comprobar colisión del mouse con los botones
        hover_jugar = self.btn_jugar.collidepoint(mouse_pos)
        hover_opciones = self.btn_opciones.collidepoint(mouse_pos)
        
        # Efecto hover (aclara un poco el botón al pasar el mouse por encima)
        if hover_jugar:
            overlay = pygame.Surface((self.btn_jugar.width, self.btn_jugar.height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 60)) # Blanco semitransparente
            screen.blit(overlay, self.btn_jugar.topleft)
            
        if hover_opciones:
            overlay = pygame.Surface((self.btn_opciones.width, self.btn_opciones.height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 60))
            screen.blit(overlay, self.btn_opciones.topleft)
            
        # Lógica de clics en los botones
        if mouse_pressed and not self.mouse_was_pressed:
            if hover_jugar:
                self.start_game()
            elif hover_opciones:
                print("Botón OPCIONES presionado (pantalla no implementada aún)")
                
        self.mouse_was_pressed = mouse_pressed
        
        # Mantener el atajo de teclado (Espacio o Enter) para jugar rápido
        action_key_is_pressed = keys[pygame.K_SPACE] or keys[pygame.K_RETURN]
        if action_key_is_pressed and not self.action_key_was_pressed:
            self.start_game()
            
        self.action_key_was_pressed = action_key_is_pressed
        
    def start_game(self):
        from include.screens.nivel1 import Nivel1
        self.game.pantalla_actual = Nivel1(self.game)
        self.game.pantalla_actual.enter(pygame.display.get_surface())
