from enum import Enum

class ServiciosEspeciales(Enum):
    """
    Esta clase enumera los servicios especiales disponibles y sus precios.
    """
    COMIDA_A_LA_CARTA = ("Comida a la carta", 40)
    MASCOTA_EN_CABINA = ("Mascota en cabina", 50)
    ACOMPANANTE_PARA_MENOR = ("Acompañante para menor", 15)
    ASISTENCIA_NECESIDADES_ESPECIALES = ("Asistencia para pasajero con necesidades especiales", 0)
    TRANSPORTE_TERRESTRE = ("Transporte terrestre", 70)

    def __init__(self, servicio, precio):
        """
        Inicializa el servicio con su nombre y precio.
        """
        self.servicio = servicio
        self.precio = precio

    def get_servicio(self):
        """
        Devuelve el nombre del servicio.
        """
        return self.servicio

    def get_precio(self):
        """
        Devuelve el precio del servicio.
        """
        return self.precio
    
    def __str__(self):
        """
        Devuelve una representación en cadena del servicio.
        """
        return f"Tipo: {self.servicio}, Valor pagado: {self.precio}"