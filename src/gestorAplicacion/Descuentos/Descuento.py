from abc import ABC , abstractmethod
class Descuento (ABC):  # Abstracta


    def __init__(self, user, boleto):
        self.user = user  # El usuario al que se asigna el descuento
        self.boleto = boleto  # El boleto al que se aplica el descuento
        self.ahorrado = 0
        self.estado = "Generado"
        self.usado = False
        
    def guardar(self): # aquí se define si el descuento ya fue asignado a un boleto
        self.estado = "Usado"
        self.usado = True
        self.user.descuentos.append(self)
        
    def getInfo(self): # este metodo devuelve la informacion de los atributos principales del descuento
        return f"Tipo: {self.tipo}, Estado: {self.estado}, Ahorrado: ${self.ahorrado}, Millas canjeadas: {self.costoMillas}"
    
    @abstractmethod
    def  generar(self, user, boleto):
        pass
    
    @abstractmethod
    def aplicarDescuento(self):
        pass
    
    def getCostoMillas(self):  # devuelve el costo en millas del descuento
        return self.costoMillas
    
    def __str__(self):
        return self.getInfo()