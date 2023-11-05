from .Descuento import Descuento

class upgradeAsiento(Descuento):
    costoMillas = 20

    def __init__(self, user):
        self.init(user)
        self.tipo = "Mejora de asiento"

    def aplicarDescuento(self, boleto):
        self.boleto = boleto
        self.estado = "Usado"  # Cambia el estado del descuento a "Usado"
        self.usar()  # Marca el descuento como usado
