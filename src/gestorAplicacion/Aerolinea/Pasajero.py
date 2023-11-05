class Pasajero:

    def __init__(self, user, boleto):
        self.nombre = user.getNombre()
        self.user = user
        self.boleto = boleto

    def getNombre(self):
        return self.nombre

    def setNombre(self, nombre):
        self.nombre = nombre

    def getUser(self):
        return self.user

    def setUser(self, user):
        self.user = user

    def getBoleto(self):
        return self.boleto

    def setBoleto(self, boleto):
        self.boleto = boleto
