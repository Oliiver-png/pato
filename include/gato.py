import pygame
import os

class Gato(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.animations = []
        self.load_animations()
        
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.1 # segundos por frame
        self.facing_right = True
        
        # Imagen inicial
        if self.animations:
            self.image = self.animations[self.frame_index]
        else:
            self.image = pygame.Surface((48, 48))
            self.image.fill((255, 0, 0))
            
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Físicas
        self.velocity_x = -100 # Velocidad horizontal (empieza hacia la izquierda)
        self.velocity_y = 0
        self.gravity = 1200
        self.max_fall_speed = 600
        
        self.on_ground = False
        self.is_dead = False
        self.shoot_timer = 0

    def load_animations(self):
        base_path = os.path.join(os.path.dirname(__file__), "..", "datos", "imagenes", "personajes", "gatos", "caminar")
        
        for i in range(1, 11): 
            walk_path = os.path.join(base_path, f"{i}.png")
            if os.path.exists(walk_path):
                img = pygame.image.load(walk_path).convert_alpha()
                # Escalar a tamaño apropiado (48x48)
                img = pygame.transform.scale(img, (48, 48))
                img.set_colorkey((255, 255, 255))
                self.animations.append(img)
                
    def update(self, dt, solid_rects, projectiles_list=None):
        if self.is_dead:
            return
            
        self._apply_physics(dt, solid_rects)
        self._update_animation(dt)
        
        # Lógica de disparo
        if projectiles_list is not None:
            self.shoot_timer += dt
            if self.shoot_timer >= 3.0:
                self.shoot_timer = 0
                from include.projectile import Projectile
                vx = 250 if self.facing_right else -250
                vy = -400
                proj = Projectile(self.rect.centerx, self.rect.centery, vx, vy)
                projectiles_list.append(proj)
        
    def _apply_physics(self, dt, solid_rects):
        # Aplicar gravedad
        self.velocity_y += self.gravity * dt
        if self.velocity_y > self.max_fall_speed:
            self.velocity_y = self.max_fall_speed
            
        # Movimiento X
        self.rect.x += int(self.velocity_x * dt)
        self._check_collisions(solid_rects, "x")
        
        # Movimiento Y
        move_y = int(self.velocity_y * dt)
        if move_y == 0 and self.velocity_y > 0:
            move_y = 1
            
        self.rect.y += move_y
        self.on_ground = False
        self._check_collisions(solid_rects, "y")
        
        # Evitar caer por precipicios (girar si no hay piso adelante)
        if self.on_ground:
            # Crear un pequeño rectángulo justo enfrente y un poco debajo del gato
            if self.velocity_x > 0:
                check_rect = pygame.Rect(self.rect.right, self.rect.bottom, 2, 4)
            else:
                check_rect = pygame.Rect(self.rect.left - 2, self.rect.bottom, 2, 4)
                
            has_ground = False
            for solid in solid_rects:
                if solid.colliderect(check_rect):
                    has_ground = True
                    break
                    
            if not has_ground:
                self.velocity_x *= -1
                # Pequeña compensación visual
                if self.velocity_x > 0:
                    self.rect.x += 2
                else:
                    self.rect.x -= 2
        
        # Actualizar dirección de mirada según velocidad
        if self.velocity_x > 0:
            self.facing_right = True
        elif self.velocity_x < 0:
            self.facing_right = False
            
    def _check_collisions(self, solid_rects, direction):
        for solid in solid_rects:
            if self.rect.colliderect(solid):
                if direction == "x":
                    if self.velocity_x > 0:
                        self.rect.right = solid.left
                        self.velocity_x *= -1 # Rebote
                    elif self.velocity_x < 0:
                        self.rect.left = solid.right
                        self.velocity_x *= -1 # Rebote
                elif direction == "y":
                    if self.velocity_y > 0:
                        self.rect.bottom = solid.top
                        self.on_ground = True
                    elif self.velocity_y < 0:
                        self.rect.top = solid.bottom
                    self.velocity_y = 0
                    
    def draw(self, screen, camera_x=0):
        if self.is_dead:
            return
        # Dibujarlo restando la cámara
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))
        
    def _update_animation(self, dt):
        if not self.animations:
            return
            
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations)
            
        self.image = self.animations[self.frame_index]
        
        # Voltear horizontalmente si va a la izquierda
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
