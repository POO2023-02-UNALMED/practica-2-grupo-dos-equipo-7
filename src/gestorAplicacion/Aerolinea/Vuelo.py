from .Asiento import Asiento
import random


class Vuelo:

    def __init__(self, origen, destino, horaSalida, id):
        
        self.ORIGEN = origen        
        self.DESTINO = destino
        self.ID = id
        self.horaSalida = horaSalida
        
        self.asientos = []

    @staticmethod
    def generarVuelos(cantidad, origen, destino):
        vuelos = []
        for x in range(0, cantidad):
            aerolinea = "Nn"
            id = str(x)
            hSalida = Vuelo.generarHora()
            hLlegada = "Nn"
            vuelos.append(
                Vuelo(origen, destino, aerolinea, id, hSalida, hLlegada))
        return vuelos

    @staticmethod
    def generarHora():
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
        for i in range(0, premium):
            self.asientos.append(Asiento("Vip", i, (base * 1.25)))

        for j in range(0, economicos):
            self.asientos.append(Asiento("Economico", j, base))
    
        return self.asientos
    
    def getOrigenDestino(self):
        return f"{self.ORIGEN} - {self.DESTINO}"

    def getInfo(self):
        return f"Id: {self.ID}, Origen: {self.ORIGEN} , Destino: {self.DESTINO} , Hora salida: {self.horarioSalida}"

    def __str__(self):
        return self.getInfo()
