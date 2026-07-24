from include.screens.level_screen import BaseLevelScreen

class Nivel1(BaseLevelScreen):
    def __init__(self, game_state):
        # Heredamos todo de BaseLevelScreen y le pasamos el ID "1"
        super().__init__(game_state, level_id="1")
        
    def custom_enter(self):
        """Este código se ejecuta justo después de cargar el nivel."""
        print("El Nivel 1")
        
    def custom_update(self, dt):
        """Este código se ejecuta en cada frame, ideal para eventos de gameplay."""
        if self.player and self.player.rect.x > 1000:
            pass 
