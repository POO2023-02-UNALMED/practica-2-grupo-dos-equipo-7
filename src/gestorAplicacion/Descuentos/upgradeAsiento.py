from .Descuento import Descuento

class upgradeAsiento(Descuento):
    """
    Clase que representa una mejora de asiento.

    Atributos:
        asiento (Asiento): Asiento al que se quiere mejorar.
        costoMillas (int): Costo en millas de la mejora.
        tipo (str): Tipo de descuento.
    """
    
    def __init__(self, asiento):
        """
        Inicializa un objeto de la clase upgradeAsiento.
        """
        self.asiento = asiento
        self.costoMillas = 20
        self.tipo = "Mejora de asiento"

    def generar(self, user, boleto):
        """
        Genera la mejora de asiento para un usuario y un boleto específicos.
        """
        super().__init__(user, boleto)
        
    def aplicarDescuento(self):
        """
        Aplica la mejora de asiento al boleto del usuario.
        """
        prevAsiento = self.boleto.asiento  # Asiento original
        newAsiento = self.asiento  # Nuevo asiento
        
        # Mejora el asiento y obtiene el valor ahorrado
        ahorrado = self.boleto.upgradeAsientoMillas(prevAsiento, newAsiento)
        self.ahorrado = ahorrado
        
        # Guarda la mejora en los descuentos del usuario
        self.guardar()
        return ahorrado