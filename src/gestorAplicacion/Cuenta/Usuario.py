class Usuario:

    def __init__(self, nombre, mail, contrasena, id):
        self.dinero = None
        self.millas = None

        self.historial = []
        self.descuentos = []
        self.nombre = nombre
        self.id = id
        self.mail = mail
        self.contrasena = contrasena

    def comprarBoleto(self, boleto):
        self.dinero -= boleto.getValor()
        self.millas += boleto.getValor() * 0.1
        self.historial.append(boleto)
        boleto.setStatus("Comprado")

    def comprarBoletoReasig(self, boleto):
        self.dinero -= boleto.getValor()
        self.millas += boleto.getValor() * 0.1
        boleto.setStatus("Comprado")

    def reasignarBoleto(self, boleto):
        self.dinero += (boleto.getValor() * 0.9)
        self.millas -= boleto.getValor() * 0.1

    def cancelarBoleto(self, boleto):
        self.dinero += (boleto.getValor() * 0.5)
        self.millas -= (boleto.getValor() * 0.1)

    def getInfo(self):
        return f"Usuario: {self.nombre} // ID - {self.id}\nBalance: {self.dinero}\nMillas: {self.millas}\nVuelos comprados: {len(self.historial)}\nDescuentos canjeados: {len(self.descuentos)}"

    def verificarContrasena(self, contrasena):
        if (self.contrasena == (contrasena)):
            return True
        else:
            return False

    def depositarDinero(self, valor):
        self.dinero += valor

    def realizarPago(self, valor):
        self.dinero -= valor

    def addDescuento(self, descuento):
        self.descuentos.add(descuento)

    def descontarMillas(self, valor):
        self.millas -= valor

    def getDinero(self):
        return self.dinero

    def setDinero(self, dinero):
        self.dinero = dinero

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getNombre(self):
        return self.nombre

    def setNombre(self, nombre):
        self.nombre = nombre

    def getMillas(self):
        return self.millas

    def setMillas(self, millas):
        self.millas = millas

    def getHistorial(self):
        return self.historial

    def setHistorial(self, historial):
        self.historial = historial

    def getDescuentos(self):
        return self.descuentos

    def setDescuentos(self, descuentos):
        self.descuentos = descuentos

    def getMail(self):
        return self.mail

    def setMail(self, mail):
        self.mail = mail

    def getContrasena(self):
        return self.contrasena

    def setContrasena(self, contrasena):
        self.contrasena = contrasena
