from include import functions

class Screen:
    def __init__(self, game_state):
        self.game = game_state
        
    def enter(self, screen):
        """Se llama al entrar a la pantalla."""
        pass
        
    def exit(self):
        """Se llama al salir de la pantalla para limpiar."""
        pass
        
    def update(self, dt, screen):
        """Se llama cada frame."""
        pass