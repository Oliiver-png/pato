import config
from include.cuadricula import Cuadricula
from include.niveles import obtenerNivelManager
from include.player import Player

class BaseLevelScreen:
    def __init__(self, game_state, level_id):
        self.game = game_state
        self.level_id = str(level_id)
        self.cuadricula = Cuadricula()
        self.player = None
        self.camera_x = 0
        
    def custom_enter(self):
        """Hook para ser sobreescrito por las clases hijas (eventos iniciales)."""
        pass
        
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
            
            # Spawnear al jugador (posición x=100, y=100)
            self.player = Player(100, 100)
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
                
            # Movimiento suave de cámara (lerp) o asignación directa
            self.camera_x = target_camera_x
            
            # Obtener colisiones del escenario (las coordenadas reales no cambian)
            colisiones = self.cuadricula.obtener_colisiones()
            
            # Actualizar físicas y posición del jugador
            self.player.update(dt, colisiones)

        # Llamar al hook personalizado
        self.custom_update(dt)

        # Dibujar la cuadrícula de tiles restando la cámara
        self.cuadricula.render(screen, self.camera_x)
        
        # Dibujar al jugador restando la cámara
        if self.player:
            self.player.draw(screen, self.camera_x)
