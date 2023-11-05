from .Descuento import Descuento

class descuentoMaleta(Descuento):
    
    costoMillas = 20   
    descuento = 20
    
    def __init__(self, user):
        self.init(user)
        self.tipo = "Descuento de maleta"
    
    def aplicarDescuento(self, boleto):
        self.boleto = boleto
        retorno = 0.2 # Porcentaje de retorno del costo del equipaje al usuario
        valorEquipaje = self.boleto.getValorEquipaje()
        boleto.setValorEquipaje((valorEquipaje * 0.8)) # Aplicar el descuento al costo del equipaje
        self.user.depositarDinero((valorEquipaje * retorno)) # Depositar un porcentaje del valor original en la cuenta del usuario
        boleto.updateValorBase() # Actualizar el valor base del boleto
        self.usar() # Marcar el descuento como usado
    

