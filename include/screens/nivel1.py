from include import functions
from include.cuadricula import Cuadricula
from include.niveles import obtenerNivelManager
from include.player import Player

class Nivel1:
    def __init__(self, game_state):
        self.game = game_state
        self.cuadricula = Cuadricula()
        self.player = None
        
    def enter(self, screen):
        """Se llama al entrar a la pantalla."""
        # Obtener los datos del nivel 1 usando el NivelManager
        nivel_manager = obtenerNivelManager()
        nivel = nivel_manager.obtenerNivel("1")
        
        if nivel:
            self.cuadricula.loadLevel(nivel.aDict())
            print(f"[Nivel 1] Nivel cargado exitosamente con {len(self.cuadricula.matriz_tiles)} tiles.")
            
            # Spawnear al jugador (posición x=100, y=100)
            self.player = Player(100, 100)
        else:
            print("[ERROR] No se encontró el nivel 1 en NivelManager")
        
    def exit(self):
        """Se llama al salir de la pantalla para limpiar."""
        pass
        
    def update(self, dt, screen):
        """Se llama cada frame."""
        # Dibujar la cuadrícula de tiles
        self.cuadricula.render(screen)
        
        # Actualizar y dibujar al jugador si existe
        if self.player:
            # Obtener colisiones del escenario
            colisiones = self.cuadricula.obtener_colisiones()
            
            # Actualizar físicas y posición
            self.player.update(dt, colisiones)
            
            # Dibujar personaje
            self.player.draw(screen)