from .RestriccionesMaleta import RestriccionesMaleta
class Maleta(RestriccionesMaleta):

    precioMaleta = 10.0
    excedente = 0

    def __init__(self, id, peso, boleto):
        self.id = id
        self.peso = peso
        self.boleto = boleto
        self.destino_origen = boleto.getOrigenDestino()
        self.boleto.addEquipaje(self)
        
    def calcularPrecio(self):
        # Valor fijo de $5
        return ((self.peso * 0.5)) + 3  # Convertimos el resultado final a int