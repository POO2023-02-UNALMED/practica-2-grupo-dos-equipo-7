from .Descuento import Descuento

class upgradeAsiento(Descuento):
    

    def __init__(self, asiento):
        self.asiento = asiento
        self.costoMillas = 20
        self.tipo = "Mejora de asiento"

    def iniciar(self, user, boleto):
        super().__init__(user, boleto)
        self.tipo = "Mejora de asiento"
        self.asiento = boleto.asiento
        self.estado = "Activo"
        self.usado = False
        self.guardar()
        
    def aplicarDescuento(self, boleto):
        self.boleto = boleto
        self.estado = "Usado"  # Cambia el estado del descuento a "Usado"
        self.usar()  # Marca el descuento como usado
