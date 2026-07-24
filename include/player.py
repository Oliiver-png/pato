import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Animaciones
        self.animations = {'idle': [], 'walk': []}
        self.load_animations()
        
        self.current_anim = 'idle'
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.1 # segundos por frame
        self.facing_right = True
        
        # Imagen inicial
        self.image = self.animations[self.current_anim][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Físicas
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 300 # pixels por segundo
        self.gravity = 1500 # pixels por segundo cuadrado
        self.jump_force = -650 # Fuerza de salto hacia arriba
        
        self.on_ground = False
        
    def load_animations(self):
        base_path = os.path.join(os.path.dirname(__file__), "..", "datos", "imagenes", "personajes", "player")
        
        # Cargar idle (duck.png)
        idle_path = os.path.join(base_path, "duck.png")
        if os.path.exists(idle_path):
            img = pygame.image.load(idle_path).convert_alpha()
            # Escalar a 48x48 para evitar que choque muy fácil con esquinas
            img = pygame.transform.scale(img, (48, 48))
            self.animations['idle'].append(img)
            
        # Cargar caminar (1.png a 8.png)
        for i in range(1, 9):
            walk_path = os.path.join(base_path, f"{i}.png")
            if os.path.exists(walk_path):
                img = pygame.image.load(walk_path).convert_alpha()
                img = pygame.transform.scale(img, (48, 48))
                self.animations['walk'].append(img)
                
        # Fallback si no encuentra imágenes
        if not self.animations['idle']:
            surf = pygame.Surface((48, 48))
            surf.fill((255, 100, 100))
            self.animations['idle'].append(surf)
        if not self.animations['walk']:
            self.animations['walk'] = self.animations['idle']

    def update(self, dt, solid_rects):
        self._handle_input()
        self._apply_physics(dt, solid_rects)
        self._update_animation(dt)
        
    def _handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Movimiento horizontal
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing_right = True
            
        # Salto
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = self.jump_force
            self.on_ground = False
            
    def _apply_physics(self, dt, solid_rects):
        # Aplicar gravedad
        self.velocity_y += self.gravity * dt
        
        # Mover en X y comprobar colisiones
        self.rect.x += int(self.velocity_x * dt)
        self._check_collisions(solid_rects, "x")
        
        # Mover en Y y comprobar colisiones
        self.rect.y += int(self.velocity_y * dt)
        self.on_ground = False
        self._check_collisions(solid_rects, "y")
        
    def _check_collisions(self, solid_rects, direction):
        for solid in solid_rects:
            if self.rect.colliderect(solid):
                if direction == "x":
                    if self.velocity_x > 0: # Moviéndose a la derecha
                        self.rect.right = solid.left
                    elif self.velocity_x < 0: # Moviéndose a la izquierda
                        self.rect.left = solid.right
                    self.velocity_x = 0
                elif direction == "y":
                    if self.velocity_y > 0: # Cayendo
                        self.rect.bottom = solid.top
                        self.on_ground = True
                    elif self.velocity_y < 0: # Saltando y golpeando el techo
                        self.rect.top = solid.bottom
                    self.velocity_y = 0
                    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def _update_animation(self, dt):
        if self.velocity_x != 0:
            self.current_anim = 'walk'
        else:
            self.current_anim = 'idle'
            
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_anim])
            
        # Refrescar imagen
        # Asegurarse de que el frame index sea válido si cambiamos de animación abruptamente
        if self.frame_index >= len(self.animations[self.current_anim]):
            self.frame_index = 0
            
        img = self.animations[self.current_anim][self.frame_index]
        
        # Voltear la imagen si miramos a la izquierda
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)
            
        self.image = img
