from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Producto:
    """
    Clase que representa un producto de Mercado Libre.
    Utiliza dataclass para simplificar la creación de objetos con atributos.
    """
    titulo: str
    precio: str
    link: str
    imagen: str
    metodo: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    id: Optional[str] = None
    capacidad: Optional[str] = None
    color: Optional[str] = None
    ram: Optional[str] = None

    def __post_init__(self):
        """
        Método que se ejecuta después de la inicialización.
        Extrae información adicional del título y asigna un ID basado en características.
        """
        # Extraer información del título
        self._extraer_info_del_titulo()

        # Generar un ID único basado en características si no se proporcionó uno
        if not self.id:
            # Crear un ID usando características del producto
            self.id = f"{self._get_safe_value(self.titulo)[:10]}_{self._get_ram()}_{self._get_capacidad()}"

    def _extraer_info_del_titulo(self):
        """Extrae información como capacidad, RAM y color del título del producto."""
        titulo = self.titulo.lower()

        # Extraer capacidad (256gb, 512gb, etc.)
        if "256gb" in titulo or "256 gb" in titulo:
            self.capacidad = "256GB"
        elif "512gb" in titulo or "512 gb" in titulo:
            self.capacidad = "512GB"
        elif "1tb" in titulo or "1 tb" in titulo:
            self.capacidad = "1TB"

        # Extraer RAM
        if "12gb ram" in titulo or "12 gb ram" in titulo:
            self.ram = "12GB"
        elif "8gb ram" in titulo or "8 gb ram" in titulo:
            self.ram = "8GB"

        # Extraer color
        colores = {
            "titanium black": "Negro",
            "titanium gray": "Gris",
            "titanium violet": "Violeta",
            "titanium yellow": "Amarillo",
            "negro": "Negro",
            "gris": "Gris",
            "violeta": "Violeta",
            "lavanda": "Lavanda"
        }

        for color_en, color_es in colores.items():
            if color_en in titulo:
                self.color = color_es
                break

    def _get_capacidad(self):
        """Retorna la capacidad o valor por defecto."""
        return self.capacidad or "N/A"

    def _get_ram(self):
        """Retorna la RAM o valor por defecto."""
        return self.ram or "N/A"

    def _get_safe_value(self, value):
        """Convierte un valor a una cadena segura para usar en IDs."""
        if value:
            return value.replace(" ", "_").replace("/", "_").replace("\\", "_")
        return "unknown"

    def to_dict(self):
        """Convierte el objeto Producto a un diccionario."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'precio': self.precio,
            'link': self.link,
            'imagen': self.imagen,
            'método': self.metodo,
            'capacidad': self.capacidad,
            'ram': self.ram,
            'color': self.color,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Producto a partir de un diccionario."""
        return cls(
            titulo=data.get('titulo', 'No disponible'),
            precio=data.get('precio', 'No disponible'),
            link=data.get('link', 'No disponible'),
            imagen=data.get('imagen', 'No disponible'),
            metodo=data.get('método', 'Desconocido'),
            timestamp=data.get('timestamp', datetime.now().isoformat()),
            id=data.get('id'),
            capacidad=data.get('capacidad'),
            color=data.get('color'),
            ram=data.get('ram')
        )