from .ServiciosEspeciales import ServiciosEspeciales

class Boleto:
    """
    Representa un boleto de vuelo.

    Atributos:
        origen (str): Ciudad de origen del vuelo.
        destino (str): Ciudad de destino del vuelo.
        vuelo (Vuelo): Objeto de la clase Vuelo asociado al boleto.
        asiento (Asiento): Objeto de la clase Asiento asociado al boleto.
        usuario (Usuario): Objeto de la clase Usuario que adquiere el boleto.
        id (int): Identificador único del boleto.
        mascotas (list): Lista de mascotas que el usuario quiere llevar en el vuelo.
        equipaje (list): Lista de equipajes que el usuario quiere llevar en el vuelo.
        descuentos (list): Lista de descuentos que el usuario quiere aplicar al boleto.
        serviciosContratados (list): Lista de servicios contratados para el vuelo.
        valorEquipaje (int): Número de equipajes.
        cantidadMascotasCabina (int): Número de mascotas en cabina.
        cantidadMascotasBodega (int): Número de mascotas en la bodega.

    Métodos:
        __init__(self, origen, destino, vuelo, asiento, usuario): Inicializa un objeto de la clase Boleto.
    """
    
    cont = 0

    def __init__(self, origen, destino, vuelo, asiento, usuario):
        """
        Inicializa un objeto de la clase Boleto.

        Args:
            origen (str): Ciudad de origen del vuelo.
            destino (str): Ciudad de destino del vuelo.
            vuelo (Vuelo): Objeto de la clase Vuelo asociado al boleto.
            asiento (Asiento): Objeto de la clase Asiento asociado al boleto.
            usuario (Usuario): Objeto de la clase Usuario que adquiere el boleto.
        """
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

    def setAsiento(self, asiento):
        """
        Asigna un asiento al boleto y establece el valor inicial y el valor total del boleto.

        Args:
            asiento (Asiento): Objeto de la clase Asiento que se asignará al boleto.
        """
        self.asiento = asiento
        self.valorInicial = asiento.valorBase
        self.valor = self.valorInicial
        self.tipo = asiento.tipo

    def addEquipaje(self, maleta):
        """
        Añade una maleta al boleto y actualiza el valor total del boleto.

        Args:
            maleta (Equipaje): Objeto de la clase Equipaje que se añadirá al boleto.
        """
        self.equipaje.append(maleta)
        self.updateValor()

    def updateValor(self):
        """
        Actualiza el valor total del boleto sumando el valor inicial y el valor de todos los equipajes.
        """
        temp = 0
        for maleta in self.equipaje:
            temp += maleta.calcularPrecio()

        self.valorEquipaje = temp
        self.valor = self.valorInicial + temp

    def calcularReasignacion(self, boletoAnterior):
        """
        Calcula el valor total del boleto después de reasignar el asiento.

        Args:
            boletoAnterior (Boleto): Objeto de la clase Boleto que representa el boleto antes de la reasignación.
        """
        restante = self.valor - boletoAnterior.valor
        if restante >= 0:
            return round(self.valor * 1.10, 2)
        return restante + round(self.valor * 1.10, 2)

    def updateValorBase(self):
        """
        Actualiza el valor total del boleto sumando el valor inicial y el valor del equipaje.
        """
        self.valor = self.valorInicial + self.valorEquipaje

    def asignarAsiento(self, asiento):
        """
        Asigna un asiento al boleto.

        Args:
            asiento (Asiento): Objeto de la clase Asiento que se asignará al boleto.
        """
        asiento.asignarBoleto(self)

    def upgradeAsientoMillas(self, prevAsiento, newAsiento):
        """
        Actualiza el asiento del boleto a un asiento VIP y calcula el valor ahorrado.

        Args:
            prevAsiento (Asiento): Objeto de la clase Asiento que representa el asiento anterior.
            newAsiento (Asiento): Objeto de la clase Asiento que representa el nuevo asiento.
        """
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
            "Valor" : f"${self.valor}",
            "Tipo asiento" : self.tipo,
            "Numero de asiento" : self.asiento.n_silla,
            "Cantidad maletas" : len(self.equipaje),
            "Estado": self.status,
            "Servicios contratados": len(self.serviciosContratados)
        }
        
    def getStr(self): # devuelve el estado de los atributos principales del boleto para su visualizacion
        return f"Origen-Destino: {self.getOrigenDestino()}, Valor: {self.valor}, Tipo asiento: {self.tipo}, Cantidad maletas: {len(self.equipaje)}, Estado: {self.status}, Servicios: {len(self.serviciosContratados)}"