

class Asiento:
    """
    Representa un asiento en un avión o teatro.

    Atributos:
        tipo (str): Tipo de asiento (Ejemplo: "Vip", "Economico").
        n_silla (int): Numero de silla.
        valorBase (float): Valor base del asiento.
        disponible (bool): Indica si el asiento esta disponible o no.
        vip (bool): Indica si el asiento es vip o no.
        status (str): Estado del asiento (ejemplo: "Disponible", "Asignado").
        boleto (Boleto): Boleto asociado al asiento.

    Metodos:
        asignarBoleto(self, boleto): Asigna un boleto al asiento.
        desasignarBoleto(self): Desasigna el boleto del asiento.
        getInfo(self): Devuelve la informacion de los atributos principales.
        __str__(self): Devuelve la informacion de los atributos principales.
    """

    def __init__(self, tipo, n_silla,  valorBase):
        """
        Inicializa un objeto de la clase Asiento.

        Args:
            tipo (str): Tipo de asiento.
            n_silla (int): Numero de silla.
            valorBase (float): Valor base del asiento.
        """
        self.tipo = tipo
        self.n_silla = n_silla
        self.valorBase = valorBase
        self.disponible = True
        self.vip = True if tipo == "Vip" else False
        
        # Estado del asiento (ejemplo: "Disponible", "Asignado")
        self.status = "Disponible"
        self.boleto = None  # asociado al asiento

    def asignarBoleto(self, boleto):#se le asigna el boleto  del usuario 
        self.boleto = boleto        # que lo compró
        self.disponible = False
        self.status = "Asignado"

    def desasignarBoleto(self): #quita el boleto al que esté asignado
        self.boleto = None
        self.disponible = True
        self.status = "Disponible"

    def getInfo(self): # devuelve  la informacion de los atributos principales
        return f"{self.n_silla}. Tipo: {self.tipo}, Valor: ${self.valorBase}"
    
    def __str__(self):
        return self.getInfo()