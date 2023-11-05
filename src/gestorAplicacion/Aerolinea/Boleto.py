from .Pasajero import Pasajero
from .ServiciosEspeciales import ServiciosEspeciales

class Boleto:

    cont = 0

    def __init__(self, origen, destino, propietario, vuelo):
        Boleto.cont += 1
        self.origen = origen
        self.destino = destino
        self.user = propietario
        self.vuelo = vuelo
        self.pasajero = Pasajero(propietario, self)
        self.id = Boleto.cont

        self.cantidadMascotasCabina = 0
        self.cantidadMascotasBodega = 0
        self.status = "Pendiente"
        self.checkInRealizado = False

        self.mascotas = []
        self.equipaje = []
        self.descuentos = []
        self.serviciosContratados = []

        self.tipo = None
        self.valor = None
        self.asiento = None
        self.valorInicial = None
        self.valorEquipaje = None

    def updateValor(self):
        temp = 0
        for maleta in self.equipaje:
            temp += maleta.calcularPrecio()

        self.valorEquipaje = temp
        self.valor = self.valorInicial + temp

    # Actualiza el valor, va en relacion con la funcionalidad reasignar asiento

    def updateValorBase(self):
        self.valor = self.valorInicial + self.valorEquipaje

    def asignarAsiento(self, asiento):
        asiento.asignarBoleto(self)

    def setAsiento(self, asiento):
        self.asiento = asiento
        self.valorInicial = asiento.getValor()
        self.valor = self.valorInicial
        self.tipo = asiento.getTipo()

    # Actualiza un asiento asignado a un boleto a otro asiento, va de la mano con
    # la funcionalidad reasignar asiento

    def upgradeAsiento(self, prevAsiento, newAsiento):
        self.asiento = newAsiento
        self.valorInicial = newAsiento.getValor()
        self.valor = self.valorInicial
        self.tipo = newAsiento.getTipo()

        temp = 0
        for maleta in self.equipaje:
            temp += maleta.calcularPrecio()

        self.valorEquipaje = temp
        self.valor = self.valorInicial + temp

        prevAsiento.desasignarBoleto()
        newAsiento.asignarBoleto(self)

    # Actualiza el asiento a vip segun lo que seleccione el usuario, va de la mano
    # con la funcionalidad canjear millas
    def upgradeAsientoMillas(self, prevAsiento, newAsiento):
        self.asiento = newAsiento
        self.valorInicial = prevAsiento.getValor()
        self.valor = self.valorInicial
        self.tipo = newAsiento.getTipo()
        self.valor = self.valorInicial + self.valorEquipaje
        prevAsiento.desasignarBoleto()
        newAsiento.asignarBoleto(self)

    def reasignarAsiento(self, asiento):
        self.asiento = asiento
        self.valorInicial = asiento.getValor() * (float)(1.1)
        self.valor = self.valorInicial
        self.tipo = asiento.getTipo()

    def anadirServiciosEspeciales(self, servicio):
        if (servicio == ServiciosEspeciales.MASCOTA_EN_CABINA):
            self.cantidadMascotasCabina += 1
        if (servicio == ServiciosEspeciales.MASCOTA_EN_BODEGA):
            self.cantidadMascotasBodega += 1
        self.serviciosContratados.append(servicio)

    def anadirServiciosMascota(self, mascota):
        self.mascotas.append(mascota)

    def resetEquipaje(self):
        self.equipaje = []

    def getOrigenDestino(self):
        return self.origen + "-" + self.destino

    def addEquipaje(self, maleta):
        self.equipaje.append(maleta)
        self.updateValor()

    def getInfo(self):

        return f"Precio: ${self.valor}, Tipo: {self.tipo}, Origen-Destino: {self.getOrigenDestino()}, Numero de asiento: {self.asiento.getN_silla()}, Estado: {self.status}, N. Maletas: {len(self.equipaje)}, Servicios contratados: {len(self.serviciosContratados)}"

    # ...Metodos def get yself set...

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getUser(self):
        return self.user

    def setUser(self, user):
        self.user = user

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def getOrigen(self):
        return self.origen

    def setOrigen(self, origen):
        self.origen = origen

    def getDestino(self):
        return self.destino

    def setDestino(self, destino):
        self.destino = destino

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getEquipaje(self):
        return self.equipaje

    def setEquipaje(self, equipaje):
        self.equipaje = equipaje

    def getAsiento(self):
        return self.asiento

    def getPasajero(self):
        return self.pasajero

    def setPasajero(self, pasajero):
        self.pasajero = pasajero

    def getValorInicial(self):
        return self.valorInicial

    def setValorInicial(self, valorInicial):
        self.valorInicial = valorInicial

    def getValorEquipaje(self):
        return self.valorEquipaje

    def setValorEquipaje(self, valorEquipaje):
        self.valorEquipaje = valorEquipaje

    def getVuelo(self):
        return self.vuelo

    def setVuelo(self, vuelo):
        self.vuelo = vuelo

    def getCheckInRealizado(self):
        return self.checkInRealizado

    def setCheckInRealizado(self, checkInRealizado):
        self.checkInRealizado = checkInRealizado

    def getServiciosContratados(self):
        return self.serviciosContratados

    def setServiciosContratados(self, serviciosContratados):
        self.serviciosContratados = serviciosContratados

    def getMascotasEnCabina(self):
        return self.cantidadMascotasCabina

    def getMascotasEnBodega(self):
        return self.cantidadMascotasBodega

    def getMascotas(self):
        return self.mascotas
