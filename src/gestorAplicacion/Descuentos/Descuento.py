class Descuento:  # Abstracta

    def __init__(self, user, boleto):
        self.user = user  # El usuario al que se asigna el descuento
        self.boleto = boleto  # El boleto al que se aplica el descuento

    def usar(self):
        self.estado = "Usado"
        self.usado = True
        self.guardar()

    def isUsado(self):
        return self.usado

    def getTipo(self):
        return self.tipo

    def aplicarDescuento(self):
        pass

    def getInfo(self):
        return f"Tipo: {self.tipo}, Estado: {self.estado}"
