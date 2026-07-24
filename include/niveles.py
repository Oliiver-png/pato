import json
import os

class Nivel:
    """Representa un nivel del juego"""
    
    def __init__(self, nivel_id, data):
        """
        Inicializa un nivel con sus propiedades
        
        Args:
            nivel_id: Identificador del nivel (ej: '1')
            data: Diccionario con las propiedades del nivel
        """
        self.id = nivel_id
        
        # Parsear cuadrícula
        cuadricula = data.get("Cuadricula", {})
        self.num_x = cuadricula.get("num_x", 0)
        self.num_y = cuadricula.get("num_y", 0)
        
        # Parsear tiles
        self.tiles = data.get("tiles", {})
        
    def __repr__(self):
        return f"Nivel({self.id}, {self.num_x}x{self.num_y})"
    
    def aDict(self):
        """Convierte el nivel a diccionario"""
        return {
            "id": self.id,
            "Cuadricula": {
                "num_x": self.num_x,
                "num_y": self.num_y
            },
            "tiles": self.tiles
        }

class NivelManager:
    """Gestor centralizado de niveles del juego"""
    
    def __init__(self, jsonPath=None):
        """
        Inicializa el NivelManager cargando los niveles desde JSON
        
        Args:
            jsonPath: Ruta al archivo JSON de configuración.
                     Si es None, busca en 'include/data/datosNiveles.json'
        """
        self.niveles = {}
        
        if jsonPath is None:
            # Ruta relativa al archivo de configuración
            jsonPath = os.path.join(
                os.path.dirname(__file__),
                "data",
                "datosNiveles.json"
            )
        
        self.jsonPath = jsonPath
        self._cargarNiveles()
    
    def _cargarNiveles(self):
        """Carga los niveles desde el archivo JSON"""
        try:
            with open(self.jsonPath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cargar niveles
            niveles_data = data.get("niveles", {})
            for nivel_id, nivel_data in niveles_data.items():
                self.niveles[nivel_id] = Nivel(nivel_id, nivel_data)
            
            print(f"[NivelManager] Cargados {len(self.niveles)} niveles desde {self.jsonPath}")
        
        except FileNotFoundError:
            print(f"[ERROR] No se encontró el archivo de configuración: {self.jsonPath}")
            self.niveles = {}
        except json.JSONDecodeError as e:
            print(f"[ERROR] Error al decodificar JSON: {e}")
            self.niveles = {}
    
    def obtenerNivel(self, nivel_id):
        """
        Obtiene un nivel por su ID
        
        Args:
            nivel_id: ID del nivel a obtener (como string)
            
        Returns:
            Nivel si existe, None en caso contrario
        """
        return self.niveles.get(str(nivel_id))
    
    def obtenerTodosNiveles(self):
        """
        Obtiene todos los niveles
        
        Returns:
            Lista de niveles
        """
        return list(self.niveles.values())


# Instancia global para usar en todo el proyecto
_nivelManagerInstance = None

def obtenerNivelManager():
    """Obtiene la instancia global de NivelManager (patrón Singleton)"""
    global _nivelManagerInstance
    if _nivelManagerInstance is None:
        _nivelManagerInstance = NivelManager()
    return _nivelManagerInstance

def reinicializarNivelManager(jsonPath=None):
    """Reinicializa el NivelManager (útil para testing)"""
    global _nivelManagerInstance
    _nivelManagerInstance = NivelManager(jsonPath)
