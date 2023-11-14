from .RestriccionesMaleta import RestriccionesMaleta
class Maleta(RestriccionesMaleta):

    precioMaleta = 10.0
    excedente = 0

    def __init__(self, id, peso):
        self.id = id
        self.peso = peso

        self.pasajero = None
        self.boleto = None
        self.destino_origen = None
        self.estado = None

    def verificarRestricciones(self):
        if (self.peso <= RestriccionesMaleta.peso and self.ancho <= RestriccionesMaleta.ancho
                and self.alto <= RestriccionesMaleta.alto and self.largo <= RestriccionesMaleta.largo
                and self.peso <= RestriccionesMaleta.peso):
            return True
        else:
            return False

    def calcularPrecio(self):
        # Valor fijo de $5
        return ((self.peso * 0.5)) + 3  # Convertimos el resultado final a int

    def asignarBoleto(self, boleto):
        self.boleto = boleto
        self.destino_origen = boleto.getOrigenDestino()

    # ...Metodos def get y set.

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getPeso(self):
        return self.peso

    def setPeso(self, peso):
        self.peso = peso

    def getLargo(self):
        return self.largo

    def setLargo(self, largo):
        self.largo = largo

    def getAncho(self):
        return self.ancho

    def setAncho(self, ancho):
        self.ancho = ancho

    def getAlto(self):
        return self.alto

    def setAlto(self, alto):
        self.alto = alto

    def getPasajero(self):
        return self.pasajero

    def setPasajero(self, pasajero):
        self.pasajero = pasajero

    def getBoleto(self):
        return self.boleto

    def setBoleto(self, boleto):
        self.boleto = boleto

    def getDestino_origen(self):
        return self.destino_origen

    def setDestino_origen(self, destino_origen):
        self.destino_origen = destino_origen

    def getEstado(self):
        return self.estado

    def setEstado(self, estado):
        self.estado = estado
