from .Descuento import Descuento

class descuentoVuelo(Descuento):    

    def __init__(self):
        self.costoMillas = 20
        self.descuento = 20
        self.tipo = "Descuento Vuelo"

    def generar(self, user, boleto):
        super().__init__(user, boleto)
        pass
        
    def aplicarDescuento(self):        
        valorVuelo = self.boleto.valorInicial  # Obtener el valor base del vuelo
        
        # Aplicar el descuento al costo del vuelo
        self.boleto.valorInicial = (valorVuelo * 0.8)
        self.ahorrado = valorVuelo * 0.2
        
        # Depositar un porcentaje del valor original en la cuenta del usuario
        self.user.depositarDinero(self.ahorrado)
        
        self.guardar()
        return self.ahorrado