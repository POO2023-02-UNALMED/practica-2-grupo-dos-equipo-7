from .Descuento import Descuento

class descuentoVuelo(Descuento):    


    def __init__(self):
        self.costoMillas = 20
        self.descuento = 20
        
    def generar(self, user, boleto):
        super().__init__(user, boleto)
        self.tipo = "Descuento Vuelo"

    def aplicarDescuento(self, boleto):
        self.boleto = boleto
        retorno = 0.2  # Porcentaje de retorno del costo del vuelo al usuario
        valorVuelo = self.boleto.getValorInicial()
        # Aplicar el descuento al costo del vuelo
        self.boleto.setValorInicial((valorVuelo * 0.8))
        # Depositar un porcentaje del valor original en la cuenta del usuario
        self.user.depositarDinero((valorVuelo * retorno))
        self.boleto.updateValorBase()  # Actualizar el valor base del boleto
        self.usar()  # Marcar el descuento como usado

    def getCostoMillas(self):
        return self.costoMillas