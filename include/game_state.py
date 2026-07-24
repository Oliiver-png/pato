class GameState:
    def __init__(self):
        # Estado de la pantalla actual
        self.pantalla_actual = None
    
    def reset(self):
        """Reinicia el estado del juego."""
        self.pantalla_actual = None

# Instancia global del estado
game_state = GameState()
