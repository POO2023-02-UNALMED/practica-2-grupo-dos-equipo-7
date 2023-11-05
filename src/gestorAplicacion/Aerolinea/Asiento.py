class Asiento:

    def __init__(self, tipo, n_silla,  valor):
        self.tipo = tipo
        self.n_silla = n_silla
        self.valor = valor
        self.disponible = True  # Indica si el asiento está disponible o no
        # Estado del asiento (ejemplo: "Disponible", "Asignado")
        self.status = "Disponible"

        self.vip = None  # Indica si es un asiento VIP o no
        self.pasajero = None  # asignado al asiento
        self.boleto = None  # asociado al asiento

    def asignarBoleto(self, boleto):
        self.boleto = boleto
        self.pasajero = boleto.getPasajero()
        self.disponible = False
        self.status = "Asignado"

    def desasignarBoleto(self):
        self.boleto = None
        self.pasajero = None
        self.disponible = True
        self.status = "Disponible"

    def getInfo(self):
        return f"{self.n_silla}. Tipo: {self.tipo}, Valor: ${self.valor}"

    # Métodos de acceso (Getters y Setters)

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getPasajero(self):
        return self.pasajero

    def setPasajero(self, pasajero):
        self.pasajero = pasajero

    def getN_silla(self):
        return self.n_silla

    def setN_silla(self, n_silla):
        self.n_silla = n_silla

    def isDisponible(self):
        return self.disponible

    def getDisponible(self):
        return self.disponible

    def setDisponible(self, disponible):
        self.disponible = disponible

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def getBoleto(self):
        return self.boleto

    def setBoleto(self, boleto):
        self.boleto = boleto

    def getValor(self):
        return self.valor
