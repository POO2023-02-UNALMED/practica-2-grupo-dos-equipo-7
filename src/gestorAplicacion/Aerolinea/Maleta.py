from .RestriccionesMaleta import RestriccionesMaleta

class Maleta(RestriccionesMaleta):
    """
    Clase Maleta que hereda de RestriccionesMaleta.
    """

    precioMaleta = 10.0  # Precio base de la maleta

    def __init__(self, id, peso, boleto):
        """
        Inicializa una nueva instancia de la clase Maleta.

        Args:
            id (int): Identificador de la maleta.
            peso (float): Peso de la maleta.
            boleto (Boleto): Boleto asociado a la maleta.
        """
        self.id = id
        self.peso = peso
        self.boleto = boleto
        self.destino_origen = boleto.getOrigenDestino()
        self.boleto.addEquipaje(self)
        
    def calcularPrecio(self):
        """
        Calcula el precio de la maleta en base a su peso.

        Returns:
            float: Precio de la maleta.
        """
        return round((((self.peso * 0.5)) + 3), 2)  # Convertimos el resultado final a int