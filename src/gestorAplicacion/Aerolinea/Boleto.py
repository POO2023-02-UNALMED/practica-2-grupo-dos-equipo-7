from .ServiciosEspeciales import ServiciosEspeciales

class Boleto:

    cont = 0

    def __init__(self, origen, destino, asiento, usuario):
        Boleto.cont += 1
        
        self.origen = origen
        self.destino = destino
        
        self.user = usuario
        
        self.id = Boleto.cont
        
        self.mascotas = []
        self.equipaje = []
        self.descuentos = []
        self.serviciosContratados = []
        
        self.valorEquipaje = 0

        self.cantidadMascotasCabina = 0
        self.cantidadMascotasBodega = 0
        self.status = "Pendiente"
        self.checkInRealizado = False
        
        # Set asiento
        self.setAsiento(asiento)
        

        

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
        self.valorInicial = asiento.valorBase
        self.valor = self.valorInicial
        self.tipo = asiento.tipo

    # Actualiza un asiento asignado a un boleto a otro asiento, va de la mano con
    # la funcionalidad reasignar asiento

    def upgradeAsiento(self, prevAsiento, newAsiento):
        self.asiento = newAsiento
        self.valorInicial = newAsiento.valorBase
        self.valor = self.valorInicial
        self.tipo = newAsiento.tipo

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
        return {
            "Origen-Destino" : self.getOrigenDestino(),
            "Precio:" : self.valor,
            "Tipo asiento" : self.tipo,
            "Numero de asiento" : self.asiento.getN_silla(),
            "Cantidad maletas" : len(self.equipaje),
            "Estado": self.status,
            "Servicios contratados": len(self.serviciosContratados)
        }