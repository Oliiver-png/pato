import pygame
import os

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        
        # Cargar imagen
        image_path = os.path.join(os.path.dirname(__file__), "..", "datos", "imagenes", "personajes", "gatos", "gatos_disparo.png")
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            # Escalar a un tamaño adecuado para un proyectil
            self.image = pygame.transform.scale(self.image, (24, 24))
            self.image.set_colorkey((255, 255, 255))
        else:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 255, 0))
            
        # Lo creamos desde el centro para que salga desde el centro del gato
        self.rect = self.image.get_rect(center=(x, y))
        
        # Físicas
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = 900 # Gravedad (parábola)
        self.max_fall_speed = 600
        
        self.is_dead = False
        
    def update(self, dt, solid_rects):
        if self.is_dead:
            return
            
        # Gravedad
        self.velocity_y += self.gravity * dt
        if self.velocity_y > self.max_fall_speed:
            self.velocity_y = self.max_fall_speed
            
        # Movimiento X
        self.rect.x += int(self.velocity_x * dt)
        if self._check_collisions(solid_rects):
            self.is_dead = True
            return
            
        # Movimiento Y
        self.rect.y += int(self.velocity_y * dt)
        if self._check_collisions(solid_rects):
            self.is_dead = True
            
    def _check_collisions(self, solid_rects):
        for solid in solid_rects:
            if self.rect.colliderect(solid):
                return True
        return False
        
    def draw(self, screen, camera_x=0):
        if not self.is_dead:
            screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))
