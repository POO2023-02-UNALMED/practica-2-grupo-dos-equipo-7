from .Descuento import Descuento

class upgradeAsiento(Descuento):
    
    def __init__(self, asiento):
        self.asiento = asiento
        self.costoMillas = 20
        self.tipo = "Mejora de asiento"

    def generar(self, user, boleto):
        super().__init__(user, boleto)
        
    def aplicarDescuento(self):
        prevAsiento = self.boleto.asiento
        newAsiento = self.asiento
        
        ahorrado = self.boleto.upgradeAsientoMillas(prevAsiento, newAsiento)
        self.ahorrado = ahorrado
        self.guardar()
        return ahorrado