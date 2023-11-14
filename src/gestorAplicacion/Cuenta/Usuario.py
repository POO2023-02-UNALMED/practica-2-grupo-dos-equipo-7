class Usuario:

    def __init__(self, nombre, mail, dinero):
        
        self.nombre = nombre
        self.mail = mail
        
        self.dinero = dinero
        self.millas = 100

        self.historial = []
        self.descuentos = []
        
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
        return {
            "Usuario": self.nombre,
            "Balance": self.dinero,
            "Millas": self.millas,
            "Vuelos comprados": len(self.historial),
            "Descuentos canjeados": len(self.descuentos)
        }
        
    def depositarDinero(self, valor):
        self.dinero += valor

    def realizarPago(self, valor):
        self.dinero -= valor

    def addDescuento(self, descuento):
        self.descuentos.add(descuento)

    def descontarMillas(self, valor):
        self.millas -= valor

    def getHistorial(self):
        return self.historial

