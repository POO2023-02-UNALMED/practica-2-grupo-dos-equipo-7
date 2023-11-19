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
        self.mascotas = [] # aquí se guardarn las mascotas que se quieran llevar en el vuelo
        self.equipaje = [] # aquí se van a guardar las maletas que se quieran llevar en el vuelo
        self.descuentos = [] #aquí se van a guardar los descuentos que se quieran usar en el boleto
        self.serviciosContratados = [] # aquí se meten los diferentes servicios que se hayan contratado para el vuelo

        self.valorEquipaje = 0 # este es el numero de equipajes
        
        self.cantidadMascotasCabina = 0 # numero de mascotas en cabina
        self.cantidadMascotasBodega = 0 #  numero de mascotas en la bodega
        
        self.status = "Pendiente" # estado del chakin 
        self.checkInRealizado = False # estado del check in
        
        # Set asiento
        self.setAsiento(asiento)


    def setAsiento(self, asiento): # aquí se le va a asignar a los atributos 
        self.asiento = asiento     #relacionados al asiento comprado su debido valor
        self.valorInicial = asiento.valorBase
        self.valor = self.valorInicial
        self.tipo = asiento.tipo

    def addEquipaje(self, maleta): # se adiciona la maleta al atributo equipaje
        self.equipaje.append(maleta)
        self.updateValor()
    
    def updateValor(self): # actualiza la cantidad de equipajes y su precio total
        temp = 0
        for maleta in self.equipaje:
            temp += maleta.calcularPrecio()

        self.valorEquipaje = temp
        self.valor = self.valorInicial + temp
        
    def calcularReasignacion(self, boletoAnterior): #calcula el valor total del boleto despues de ser reasignado el asiento
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
    
    def makeCheckIn(self): # define el estado del check in como True
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
        self.serviciosContratados.append(servicio)
        self.user.realizarPago(servicio.precio)

    def comprarServicioMascota(self, mascota): # se compra el servicio para mascotas y se añade la mascota 
        self.mascotas.append(mascota)           # al respectivo atributo
        self.cantidadMascotasCabina += 1
        self.comprarServicio(ServiciosEspeciales.MASCOTA_EN_CABINA)
    
    def resetEquipaje(self): # vacia el atributo equipaje
        self.equipaje = []

    def getOrigenDestino(self): # devuelve el destino y origen del vuelo como un unico string
        return self.origen + " - " + self.destino

    def getInfo(self): # devuelve el estado actual del boleto en un diccionario
        return {
            "Origen-Destino" : self.getOrigenDestino(),
            "Valor" : self.valor,
            "Tipo asiento" : self.tipo,
            "Numero de asiento" : self.asiento.n_silla,
            "Cantidad maletas" : len(self.equipaje),
            "Estado": self.status,
            "Servicios contratados": len(self.serviciosContratados)
        }
        
    def getStr(self): # devuelve el estado de los atributos principales del boleto para su visualizacion
        return f"Origen-Destino: {self.getOrigenDestino()}, Valor: {self.valor}, Tipo asiento: {self.tipo}, Cantidad maletas: {len(self.equipaje)}, Estado: {self.status}, Servicios: {len(self.serviciosContratados)}"