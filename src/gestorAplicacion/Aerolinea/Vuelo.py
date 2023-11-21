from .Asiento import Asiento
import random

class Vuelo:
    """
    Clase que representa un vuelo.
    """

    def __init__(self, origen, destino, horaSalida, id):
        """
        Inicializa un objeto de la clase Vuelo.
        """
        self.ORIGEN = origen        
        self.DESTINO = destino
        self.ID = id
        self.horaSalida = horaSalida
        self.asientos = []

    @staticmethod
    def generarVuelos(cantidad, origen, destino):
        """
        Genera una lista de vuelos.
        """
        return [ Vuelo(
            origen,
            destino,
            Vuelo.generarHora(),
            i + 1
        ) for i in range(cantidad) ]

    @staticmethod
    def generarHora():
        """
        Genera una hora aleatoria de salida.
        """
        horas = [
            "08:00 AM",
            "09:15 AM",
            "10:30 AM",
            "11:45 AM",
            "12:00 PM",
            "01:15 PM",
            "02:30 PM",
            "03:45 PM",
            "04:00 PM",
            "05:15 PM"
        ]
        return random.choice(horas)

    def generarAsientos(self, economicos,  premium, base):
        """
        Genera asientos para el vuelo.
        """
        self.asientos = []
        for i in range(0, premium):
            self.asientos.append(Asiento("Vip", i, (base * 1.25)))

        for j in range(premium, economicos + premium):
            self.asientos.append(Asiento("Economico", j, base))
    
        return self.asientos
    
    def getOrigenDestino(self):
        """
        Obtiene el origen y destino del vuelo.
        """
        return f"{self.ORIGEN} - {self.DESTINO}"

    def getInfo(self):
        """
        Obtiene la información del vuelo.
        """
        return f"{self.ID}. Origen: {self.ORIGEN}, Destino: {self.DESTINO}, Hora salida: {self.horaSalida}"

    def getStr(self):
        """
        Obtiene la representación en cadena de la información del vuelo.
        """
        return f"{self.ID}. Origen: {self.ORIGEN}, Destino: {self.DESTINO}, Hora salida: {self.horaSalida}"
    
    def __str__(self):
        """
        Obtiene la representación en cadena de la información del vuelo.
        """
        return self.getInfo()