import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Animaciones
        self.animations = {'idle': [], 'walk': [], 'fly': []}
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
        self.gravity = 1200 # Gravedad más suave
        self.jump_force = -550 # Fuerza de salto hacia arriba
        self.fly_force = -300 # Aleteo más suave
        self.max_fall_speed = 600 # Límite de velocidad al caer
        
        self.on_ground = False
        self.jump_key_was_pressed = False
        
    def load_animations(self):
        base_path = os.path.join(os.path.dirname(__file__), "..", "datos", "imagenes", "personajes", "player")
        
        # Cargar idle (duck.png)
        idle_path = os.path.join(base_path, "duck.png")
        if os.path.exists(idle_path):
            img = pygame.image.load(idle_path).convert_alpha()
            # Escalar a 48x48 para evitar que choque muy fácil con esquinas
            img = pygame.transform.scale(img, (48, 48))
            img.set_colorkey((255, 255, 255)) # Quitar fondo blanco
            self.animations['idle'].append(img)
            
        # Cargar caminar (1.png a 10.png desde la carpeta caminar)
        for i in range(1, 11):
            walk_path = os.path.join(base_path, "caminar", f"{i}.png")
            if os.path.exists(walk_path):
                img = pygame.image.load(walk_path).convert_alpha()
                img = pygame.transform.scale(img, (48, 48))
                img.set_colorkey((255, 255, 255)) # Quitar fondo blanco
                self.animations['walk'].append(img)
                
        # Cargar volar (A1.png a A5.png desde la carpeta volar)
        for i in range(1, 6):
            fly_path = os.path.join(base_path, "volar", f"A{i}.png")
            if os.path.exists(fly_path):
                img = pygame.image.load(fly_path).convert_alpha()
                img = pygame.transform.scale(img, (48, 48))
                img.set_colorkey((255, 255, 255)) # Quitar fondo blanco
                self.animations['fly'].append(img)
                
        # Fallback si no encuentra imágenes
        if not self.animations['idle']:
            surf = pygame.Surface((48, 48))
            surf.fill((255, 100, 100))
            self.animations['idle'].append(surf)
        if not self.animations['walk']:
            self.animations['walk'] = self.animations['idle']
        if not self.animations['fly']:
            self.animations['fly'] = self.animations['idle']

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
            
        # Salto y Vuelo
        jump_key_is_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP]
        
        if jump_key_is_pressed and not self.jump_key_was_pressed:
            if self.on_ground:
                self.velocity_y = self.jump_force
                self.on_ground = False
            else:
                # Volar
                # Asignamos directamente la fuerza para que el aleteo sea consistente
                # en lugar de sumar fuerzas y salir volando incontrolablemente.
                self.velocity_y = self.fly_force
                
        # Altura de salto variable (si sueltas el botón, caes más rápido)
        if not jump_key_is_pressed and self.velocity_y < -150:
            self.velocity_y = -150
                
        self.jump_key_was_pressed = jump_key_is_pressed
            
    def _apply_physics(self, dt, solid_rects):
        # Aplicar gravedad
        self.velocity_y += self.gravity * dt
        
        # Limitar la velocidad máxima de caída (terminal velocity)
        if self.velocity_y > self.max_fall_speed:
            self.velocity_y = self.max_fall_speed
        
        # Mover en X y comprobar colisiones
        self.rect.x += int(self.velocity_x * dt)
        self._check_collisions(solid_rects, "x")
        
        # Mover en Y y comprobar colisiones
        move_y = int(self.velocity_y * dt)
        # Truco para detectar el piso: si la gravedad nos tira hacia abajo pero el dt es muy pequeño
        # forzamos 1 pixel de movimiento para que colisione y confirme que estamos on_ground.
        if move_y == 0 and self.velocity_y > 0:
            move_y = 1
            
        self.rect.y += move_y
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
                    
    def draw(self, screen, camera_x=0):
        # Dibujarlo restando la cámara
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def _update_animation(self, dt):
        if not self.on_ground:
            new_anim = 'fly'
        elif self.velocity_x != 0:
            new_anim = 'walk'
        else:
            new_anim = 'idle'
            
        if self.current_anim != new_anim:
            self.current_anim = new_anim
            self.frame_index = 0
            self.anim_timer = 0
            
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            frames = len(self.animations[self.current_anim])
            if frames > 0:
                self.frame_index = (self.frame_index + 1) % frames
                
        # Obtener la imagen actual
        frames = self.animations[self.current_anim]
        if frames:
            if self.frame_index >= len(frames):
                self.frame_index = 0
            self.image = frames[self.frame_index]
            
        # Voltear horizontalmente si va a la izquierda
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
