class Descuento:  # Abstracta


    def __init__(self, user, boleto):
        self.user = user  # El usuario al que se asigna el descuento
        self.boleto = boleto  # El boleto al que se aplica el descuento
        self.ahorrado = 0
        self.estado = "Generado"
        self.usado = False
        
    def guardar(self):
        self.estado = "Usado"
        self.usado = True
        self.user.descuentos.append(self)
        
    def getInfo(self):
        return f"Tipo: {self.tipo}, Estado: {self.estado}, Ahorrado: ${self.ahorrado}, Millas canjeadas: {self.costoMillas}"
    
    def generar(self, user, boleto):
        pass
    
    def aplicarDescuento(self):
        pass
    
    def getCostoMillas(self):
        return self.costoMillas
    
    def __str__(self):
        return self.getInfo()