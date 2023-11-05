from .Descuento import Descuento

class descuentoVuelo(Descuento):

    costoMillas = 20
    descuento = 20

    def __init__(self, user):
        self.init(user)
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
