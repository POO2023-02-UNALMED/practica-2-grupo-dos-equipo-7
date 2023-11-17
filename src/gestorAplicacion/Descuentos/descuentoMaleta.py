from .Descuento import Descuento

class descuentoMaleta(Descuento):
    
    
    def __init__(self):
        self.costoMillas = 80
        self.descuento = 60
        self.tipo = "Descuento de maleta"

    def generar(self, user, boleto):
        super().__init__(user, boleto)
        
    def aplicarDescuento(self):        
        valorEquipaje = self.boleto.valorEquipaje  # Obtener el valor base del vuelo
    
        # Aplicar el descuento al costo del equipaje
        self.boleto.valorEquipaje = (valorEquipaje * 0.6)
        self.ahorrado = valorEquipaje * 0.4
        
        # Depositar un porcentaje del valor original en la cuenta del usuario
        self.user.depositarDinero(self.ahorrado)
        
        self.guardar()
        return self.ahorrado
