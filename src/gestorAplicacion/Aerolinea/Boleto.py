from .ServiciosEspeciales import ServiciosEspeciales

class Boleto:

    cont = 0

    def __init__(self, origen, destino, vuelo, asiento, usuario):
        Boleto.cont += 1
        
        self.origen = origen
        self.destino = destino
        self.vuelo = vuelo
        self.user = usuario
        
        self.id = Boleto.cont
        
        # Inicializar
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


    def setAsiento(self, asiento):
        self.asiento = asiento
        self.valorInicial = asiento.valorBase
        self.valor = self.valorInicial
        self.tipo = asiento.tipo

    def addEquipaje(self, maleta):
        self.equipaje.append(maleta)
        self.updateValor()
    
    def updateValor(self):
        temp = 0
        for maleta in self.equipaje:
            temp += maleta.calcularPrecio()

        self.valorEquipaje = temp
        self.valor = self.valorInicial + temp
        
    def calcularReasignacion(self, boletoAnterior):
        restante = self.valor - boletoAnterior.valor
        if restante >= 0:
            return round(self.valor * 1.10, 2)
        return restante + round(self.valor * 1.10, 2)

    # Actualiza el valor, va en relacion con la funcionalidad reasignar asiento

    def updateValorBase(self):
        self.valor = self.valorInicial + self.valorEquipaje

    def asignarAsiento(self, asiento):
        asiento.asignarBoleto(self)

    # Actualiza el asiento a vip segun lo que seleccione el usuario, va de la mano
    # con la funcionalidad canjear millas
    def upgradeAsientoMillas(self, prevAsiento, newAsiento):
        self.asiento = newAsiento
        self.tipo = newAsiento.tipo
        
        ahorrado = round(newAsiento.valorBase - prevAsiento.valorBase, 2)
        return ahorrado
    
    def makeCheckIn(self):
        self.status = "Confirmado"
        self.checkInRealizado = True
        pass
    
    
    # Actualiza un asiento asignado a un boleto a otro asiento, va de la mano con
    # la funcionalidad reasignar asiento
    def upgradeAsiento(self, newAsiento):
        self.asiento = newAsiento
        
        self.valorInicial = newAsiento.valorBase
        self.valor += 35
        self.tipo = newAsiento.tipo

        self.user.realizarPago(35)
        newAsiento.asignarBoleto(self)


    def comprarServicio(self, servicio):
        if (servicio == ServiciosEspeciales.MASCOTA_EN_CABINA):
            self.cantidadMascotasCabina += 1
        if (servicio == ServiciosEspeciales.MASCOTA_EN_BODEGA):
            self.cantidadMascotasBodega += 1
        
        self.serviciosContratados.append(servicio)
        self.user.realizarPago(servicio.get_precio())

    def comprarServicioMascota(self, mascota):
        self.mascotas.append(mascota)
        self.comprarServicio(ServiciosEspeciales.MASCOTA_EN_CABINA)
    
    def resetEquipaje(self):
        self.equipaje = []

    def getOrigenDestino(self):
        return self.origen + " - " + self.destino

    def getInfo(self):
        return {
            "Origen-Destino" : self.getOrigenDestino(),
            "Valor" : self.valor,
            "Tipo asiento" : self.tipo,
            "Numero de asiento" : self.asiento.n_silla,
            "Cantidad maletas" : len(self.equipaje),
            "Estado": self.status,
            "Servicios contratados": len(self.serviciosContratados)
        }
        
    def getStr(self):
        return f"Origen-Destino: {self.getOrigenDestino()}, Valor: {self.valor}, Tipo asiento: {self.tipo}, Cantidad maletas: {len(self.equipaje)}, Estado: {self.status}, Servicios: {len(self.serviciosContratados)}"