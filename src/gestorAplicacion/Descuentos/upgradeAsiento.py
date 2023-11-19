from .Descuento import Descuento

class upgradeAsiento(Descuento):
    
    def __init__(self, asiento):
        self.asiento = asiento
        self.costoMillas = 20
        self.tipo = "Mejora de asiento"

    def generar(self, user, boleto):# este metodo genera un descuento de tipo upgradeasiento
        super().__init__(user, boleto)
        
    def aplicarDescuento(self): # se añade al atributo descuentos del usuario 
        prevAsiento = self.boleto.asiento #y mejora el tipo de asiento economico al vip
        newAsiento = self.asiento
        
        ahorrado = self.boleto.upgradeAsientoMillas(prevAsiento, newAsiento)
        self.ahorrado = ahorrado
        self.guardar()
        return ahorrado