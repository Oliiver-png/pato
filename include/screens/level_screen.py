import config
import pygame
from include.cuadricula import Cuadricula
from include.niveles import obtenerNivelManager
from include.player import Player

class BaseLevelScreen:
    def __init__(self, game_state, level_id):
        self.game = game_state
        self.level_id = str(level_id)
        self.cuadricula = Cuadricula()
        self.player = None
        self.enemies = []
        self.projectiles = []
        self.player_projectiles = []
        self.camera_x = 0
        self.camera_y = 0
        self.score = 0
        self.health = 100
        self.max_health = 100
        self.invulnerable_timer = 0
        self.bg_image = None
        
    def custom_enter(self):
        """Hook para ser sobreescrito por las clases hijas (eventos iniciales)."""
        pass
        
    def siguiente_nivel(self):
        siguiente_id = str(int(self.level_id) + 1)
        from include.niveles import obtenerNivelManager
        import pygame
        nivel_manager = obtenerNivelManager()
        
        if nivel_manager.obtenerNivel(siguiente_id):
            print(f"Cargando el nivel {siguiente_id}...")
            # Instanciar BaseLevelScreen genérico para los siguientes niveles
            from include.screens.level_screen import BaseLevelScreen
            self.game.pantalla_actual = BaseLevelScreen(self.game, level_id=siguiente_id)
            self.game.pantalla_actual.enter(pygame.display.get_surface())
        else:
            print("¡Juego terminado! Volviendo al menú principal...")
            from include.screens.main_menu import MainMenu
            self.game.pantalla_actual = MainMenu(self.game)
            self.game.pantalla_actual.enter(pygame.display.get_surface())
        
    def custom_update(self, dt):
        """Hook para ser sobreescrito por las clases hijas (lógica cada frame)."""
        pass
        
    def enter(self, screen):
        """Se llama al entrar a la pantalla."""
        nivel_manager = obtenerNivelManager()
        nivel = nivel_manager.obtenerNivel(self.level_id)
        
        if nivel:
            self.cuadricula.loadLevel(nivel.aDict())
            
            # Cargar y añadir el menú inferior (menuButton)
            menu_level = nivel_manager.obtenerNivel("menuButton")
            if menu_level:
                self.cuadricula.appendBottomLevel(menu_level.aDict())
            else:
                print("[WARNING] No se encontró 'menuButton' en datosNiveles.json")
                
            print(f"[Level {self.level_id}] Nivel cargado exitosamente con {len(self.cuadricula.matriz_tiles)} tiles.")
            
            # Spawnear al jugador (basado en tiles)
            spawn_data = nivel.aDict().get("spawn", {"x": 1, "y": 1})
            spawn_x = spawn_data.get("x", 1) * self.cuadricula.tile_width
            spawn_y = spawn_data.get("y", 1) * self.cuadricula.tile_height
            self.player = Player(spawn_x, spawn_y)
            
            from include.gato import Gato
            self.enemies = []
            
            # Cargar fondo
            import os
            import pygame
            bg_path = os.path.join(os.path.dirname(__file__), "..", "..", "datos", "imagenes", "escenario", f"nivel {self.level_id}", f"nivel {self.level_id}.png")
            if os.path.exists(bg_path):
                img = pygame.image.load(bg_path).convert_alpha()
                # Escalar inteligentemente según si el nivel es vertical u horizontal
                if self.cuadricula.num_y > 7:
                    # Nivel vertical: escalamos para que cubra el ancho de la pantalla
                    ratio = 640 / img.get_width()
                else:
                    # Nivel horizontal: escalamos para que cubra el alto visible
                    ratio = 448 / img.get_height()
                    
                new_width = int(img.get_width() * ratio)
                new_height = int(img.get_height() * ratio)
                self.bg_image = pygame.transform.scale(img, (new_width, new_height))
                
            # Aparecer enemigos desde los datos del nivel (las coordenadas ahora están en tiles)
            for e_data in nivel.enemigos:
                if e_data.get("tipo") == "gato":
                    spawn_x = e_data.get("x", 0) * self.cuadricula.tile_width
                    spawn_y = e_data.get("y", 0) * self.cuadricula.tile_height
                    self.enemies.append(Gato(spawn_x, spawn_y))
        else:
            print(f"[ERROR] No se encontró el nivel {self.level_id} en NivelManager")
            
        # Llamar al hook personalizado
        self.custom_enter()
        
    def exit(self):
        """Se llama al salir de la pantalla para limpiar."""
        pass
        
    def update(self, dt, screen):
        """Se llama cada frame."""
        # Actualizar cámara si el jugador existe
        if self.player:
            # Calcular hacia dónde debería mirar la cámara (centrada en el jugador)
            target_camera_x = self.player.rect.x - (config.SCREEN_SIZE[0] / 2)
            
            # Evitar que la cámara se vaya más atrás del inicio (x=0)
            if target_camera_x < 0:
                target_camera_x = 0
                
            # Evitar que la cámara pase del borde derecho del nivel
            max_camera_x = (self.cuadricula.num_x * self.cuadricula.tile_width) - config.SCREEN_SIZE[0]
            if max_camera_x < 0:
                max_camera_x = 0
            if target_camera_x > max_camera_x:
                target_camera_x = max_camera_x
                
            self.camera_x = target_camera_x
            
            # Calcular target_camera_y (centrado en el jugador verticalmente)
            target_camera_y = self.player.rect.y - (config.SCREEN_SIZE[1] / 2)
            
            if target_camera_y < 0:
                target_camera_y = 0
                
            max_camera_y = (self.cuadricula.num_y * self.cuadricula.tile_height) - config.SCREEN_SIZE[1]
            if max_camera_y < 0:
                max_camera_y = 0
            if target_camera_y > max_camera_y:
                target_camera_y = max_camera_y
                
            self.camera_y = target_camera_y
            
            # Obtener colisiones del escenario (las coordenadas reales no cambian)
            colisiones = self.cuadricula.obtener_colisiones()
            
            # Actualizar físicas y posición del jugador
            self.player.update(dt, colisiones, self.player_projectiles)
            
            # Chequear victoria/meta
            meta_rects = self.cuadricula.obtener_rects_por_tipo("meta")
            for m_rect in meta_rects:
                if self.player.rect.colliderect(m_rect):
                    self.siguiente_nivel()
                    return # Salimos del update para no mezclar estados
            
            if self.invulnerable_timer > 0:
                self.invulnerable_timer -= dt
                
            # Actualizar enemigos y verificar colisión
            for enemy in self.enemies:
                if not enemy.is_dead:
                    enemy.update(dt, colisiones, self.projectiles, self.player)
                    
                    if self.player.rect.colliderect(enemy.rect):
                        # Si el jugador está cayendo (velocity_y > 0) y su parte inferior 
                        # está arriba del centro del enemigo
                        if self.player.velocity_y > 0 and self.player.rect.bottom < enemy.rect.centery:
                            enemy.is_dead = True
                            self.score += 100
                            self.player.velocity_y = -550 # Pequeño rebote
                        elif self.invulnerable_timer <= 0:
                            # Toca por el lado, recibe daño
                            self.health -= 25
                            self.invulnerable_timer = 1.5 # 1.5 segundos de inmunidad tras el golpe
                            
                            # Empuje hacia atrás (knockback)
                            if self.player.rect.centerx < enemy.rect.centerx:
                                # Enemigo a la derecha, empujar a la izquierda
                                self.player.apply_knockback(-400, -300)
                            else:
                                # Enemigo a la izquierda, empujar a la derecha
                                self.player.apply_knockback(400, -300)
                            
                            if self.health < 0:
                                self.health = 0
                                # Más adelante podemos poner que vuelva a empezar el nivel
                                
            # Actualizar proyectiles
            for proj in self.projectiles[:]:
                proj.update(dt, colisiones)
                
                # Chequear colisión con jugador
                if not proj.is_dead and self.player and self.player.rect.colliderect(proj.rect):
                    if self.invulnerable_timer <= 0:
                        self.health -= 15
                        self.invulnerable_timer = 1.5
                        if self.player.rect.centerx < proj.rect.centerx:
                            self.player.apply_knockback(-300, -200)
                        else:
                            self.player.apply_knockback(300, -200)
                        if self.health < 0:
                            self.health = 0
                    proj.is_dead = True
                    
                if proj.is_dead:
                    self.projectiles.remove(proj)
                    
            # Actualizar proyectiles del jugador
            for proj in self.player_projectiles[:]:
                proj.update(dt, colisiones)
                
                # Chequear colisión con enemigos
                if not proj.is_dead:
                    for enemy in self.enemies:
                        if not enemy.is_dead and proj.rect.colliderect(enemy.rect):
                            enemy.is_dead = True
                            self.score += 100
                            proj.is_dead = True
                            break
                            
                if proj.is_dead:
                    self.player_projectiles.remove(proj)

        # Llamar al hook personalizado
        self.custom_update(dt)

        # Dibujar fondo si existe
        if self.bg_image:
            screen.blit(self.bg_image, (-self.camera_x, -self.camera_y))

        # Dibujar la cuadrícula del mundo restando la cámara
        self.cuadricula.render_world(screen, self.camera_x, self.camera_y)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(screen, self.camera_x, self.camera_y)
            
        # Dibujar proyectiles
        for proj in self.projectiles:
            proj.draw(screen, self.camera_x, self.camera_y)
            
        # Dibujar proyectiles del jugador
        for proj in self.player_projectiles:
            proj.draw(screen, self.camera_x, self.camera_y)
            
        # Dibujar al jugador restando la cámara
        if self.player:
            self.player.draw(screen, self.camera_x, self.camera_y)
            
        # Dibujar la barra de vida DETRÁS de la UI
        self.draw_health_bar(screen)
        
        # Dibujar la interfaz de cuadrícula encima de los personajes
        self.cuadricula.render_ui(screen)
        
        # Dibujar elementos superpuestos de la interfaz (Score)
        self.draw_score(screen)

    def draw_health_bar(self, screen):
        # 1. Barra de vida dinámica
        # Coordenadas estimadas basándonos en la cuadrícula (UI empieza en y=448)
        bar_x = 167
        bar_y = 489
        max_width = 185
        bar_height = 25
        
        current_width = int(max_width * (self.health / self.max_health))
        if current_width > 0:
            # Color verde brillante, rojo si está baja
            color = (50, 220, 50) if self.health > 30 else (220, 50, 50)
            
            # Parpadeo rápido si es invulnerable por daño reciente
            if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0:
                color = (255, 255, 255)
                
            pygame.draw.rect(screen, color, (bar_x, bar_y, current_width, bar_height))
        
    def draw_score(self, screen):
        # 2. Score 0 con fuente pixelada
        import os
        font_path = os.path.join(os.path.dirname(__file__), "..", "..", "datos", "PressStart2P.ttf")
        try:
            font = pygame.font.Font(font_path, 20)
        except Exception as e:
            print("Error cargando fuente:", e)
            font = pygame.font.SysFont("impact", 36)
            
        # Color marrón oscuro
        score_surf = font.render(str(self.score), True, (80, 40, 20))
        # Ajustado al lado del texto "SCORE"
        screen.blit(score_surf, (270, 546))
