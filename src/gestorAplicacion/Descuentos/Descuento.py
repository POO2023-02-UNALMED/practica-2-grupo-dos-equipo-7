class Descuento:  # Abstracta

    def __init__(self, user, boleto):
        self.user = user  # El usuario al que se asigna el descuento
        self.boleto = boleto  # El boleto al que se aplica el descuento
        self.tipo = None  # El tipo de descuento

    def usar(self):
        self.estado = "Usado"
        self.usado = True
        self.guardar()

    def isUsado(self):
        return self.usado

    def getTipo(self):
        return self.tipo

    def guardar(self):
        if (not self.guardado):
            self.user.addDescuento(self)
            self.guardado = True


    def aplicarDescuento(self, boleto):
        pass

    def getInfo(self):
        return f"Tipo: {self.tipo}, Estado: {self.estado}"
