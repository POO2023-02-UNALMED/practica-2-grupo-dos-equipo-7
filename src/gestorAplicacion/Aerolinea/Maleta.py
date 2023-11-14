from .RestriccionesMaleta import RestriccionesMaleta
class Maleta(RestriccionesMaleta):

    precioMaleta = 10.0
    excedente = 0

    def __init__(self, id, peso):
        self.id = id
        self.peso = peso

        self.boleto = None

    def calcularPrecio(self):
        # Valor fijo de $5
        return ((self.peso * 0.5)) + 3  # Convertimos el resultado final a int

    def asignarBoleto(self, boleto):
        self.boleto = boleto
        self.destino_origen = boleto.getOrigenDestino()