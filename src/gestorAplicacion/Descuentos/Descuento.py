from abc import ABC, abstractmethod

class Descuento(ABC):
    """
    Clase abstracta que representa un descuento.

    Atributos:
        user (Usuario): Usuario al que se asigna el descuento.
        boleto (Boleto): Boleto al que se aplica el descuento.
        ahorrado (float): Cantidad de dinero ahorrada con el descuento.
        estado (str): Estado del descuento ("Generado" o "Usado").
        usado (bool): Indica si el descuento ya fue usado.
    """

    def __init__(self, user, boleto):
        """
        Inicializa un objeto de la clase Descuento.
        """
        self.user = user
        self.boleto = boleto
        self.ahorrado = 0
        self.estado = "Generado"
        self.usado = False
        
    def guardar(self):
        """
        Define si el descuento ya fue asignado a un boleto.
        """
        self.estado = "Usado"
        self.usado = True
        self.user.descuentos.append(self)
        
    def getInfo(self):
        """
        Devuelve la información de los atributos principales del descuento.
        """
        return f"Tipo: {self.tipo}, Estado: {self.estado}, Ahorrado: ${self.ahorrado}, Millas canjeadas: {self.costoMillas}"
    
    @abstractmethod
    def generar(self, user, boleto):
        """
        Método abstracto para generar el descuento.
        """
        pass
    
    @abstractmethod
    def aplicarDescuento(self):
        """
        Método abstracto para aplicar el descuento.
        """
        pass
    
    def getCostoMillas(self):
        """
        Devuelve el costo en millas del descuento.
        """
        return self.costoMillas
    
    def __str__(self):
        """
        Devuelve la representación en cadena de la información del descuento.
        """
        return self.getInfo()