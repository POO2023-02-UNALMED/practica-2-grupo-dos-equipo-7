from .Descuento import Descuento

class descuentoVuelo(Descuento):    
    """
    Clase que representa un descuento en el costo del vuelo.

    Atributos:
        costoMillas (int): Costo en millas del descuento.
        descuento (int): Porcentaje de descuento.
        tipo (str): Tipo de descuento.
    """
    
    def __init__(self): 
        """
        Inicializa un objeto de la clase descuentoVuelo.
        """
        self.costoMillas = 20
        self.descuento = 20
        self.tipo = "Descuento Vuelo"

    def generar(self, user, boleto):
        """
        Genera el descuento para un usuario y un boleto específicos.
        """
        super().__init__(user, boleto)
        
    def aplicarDescuento(self):        
        """
        Aplica el descuento al costo del vuelo.
        """
        valorVuelo = self.boleto.valorInicial  # Obtener el valor base del vuelo
        
        # Aplicar el descuento al costo del vuelo
        self.boleto.valorInicial = (valorVuelo * 0.8)
        self.ahorrado = valorVuelo * 0.2
        
        # Depositar un porcentaje del valor original en la cuenta del usuario
        self.user.depositarDinero(self.ahorrado)
        
        self.guardar()
        return self.ahorrado