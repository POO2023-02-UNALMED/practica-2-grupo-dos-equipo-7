from .Descuento import Descuento

class descuentoMaleta(Descuento):
    """
    Clase que representa un descuento en el costo de la maleta.

    Atributos:
        costoMillas (int): Costo en millas del descuento.
        descuento (int): Porcentaje de descuento.
        tipo (str): Tipo de descuento.
    """
    
    def __init__(self):
        """
        Inicializa un objeto de la clase descuentoMaleta.
        """
        self.costoMillas = 80
        self.descuento = 60
        self.tipo = "Descuento de maleta"

    def generar(self, user, boleto):
        """
        Genera el descuento para un usuario y un boleto específicos.
        """
        super().__init__(user, boleto)
        
    def aplicarDescuento(self):        
        """
        Aplica el descuento al costo de la maleta.
        """
        valorEquipaje = self.boleto.valorEquipaje  # Obtener el valor base del vuelo
    
        # Aplicar el descuento al costo del equipaje
        self.boleto.valorEquipaje = (valorEquipaje * 0.6)
        self.ahorrado = valorEquipaje * 0.4
        
        # Depositar un porcentaje del valor original en la cuenta del usuario
        self.user.depositarDinero(self.ahorrado)
        
        self.guardar()
        return self.ahorrado