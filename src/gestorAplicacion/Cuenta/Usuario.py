class Usuario:
    """
    Clase que representa a un usuario.

    Atributos:
        nombre (str): Nombre del usuario.
        mail (str): Correo electrónico del usuario.
        dinero (float): Dinero disponible del usuario.
        millas (int): Millas acumuladas por el usuario.
        historial (list): Lista de boletos comprados por el usuario.
        descuentos (list): Lista de descuentos disponibles para el usuario.
    """

    def __init__(self, nombre, mail, dinero):
        """
        Inicializa un objeto de la clase Usuario.
        """
        self.nombre = nombre
        self.mail = mail
        self.dinero = dinero
        self.millas = 100
        self.historial = []
        self.descuentos = []
        
    def comprarBoleto(self, boleto):
        """
        Permite al usuario comprar un boleto.
        """
        self.dinero -= boleto.valor
        self.millas += int(boleto.valor * 0.1)
        self.historial.append(boleto)
        boleto.status = "Comprado"
        boleto.asignarAsiento(boleto.asiento)

    def reasignarBoleto(self, newBoleto, indexBoleto):
        """
        Permite al usuario reasignar un boleto.
        """
        costo = newBoleto.calcularReasignacion(self.historial[indexBoleto])
        self.dinero -= costo
        self.millas -= int(self.historial[indexBoleto].valor * 0.1)
        newBoleto.status = "Reasignado"
        self.historial[indexBoleto] = newBoleto

    def verificarMillas(self, valor):
        """
        Verifica si el usuario tiene suficientes millas.
        """
        return True if self.millas >= valor else False
    
    def canjearMillas(self, boleto, descuento):
        """
        Permite al usuario canjear millas por un descuento.
        """
        descuento.generar(self, boleto)
        self.descontarMillas(descuento.getCostoMillas())
        ahorrado = descuento.aplicarDescuento()
        return ahorrado
    
    def comprarBoletoReasig(self, boleto):
        """
        Permite al usuario comprar un boleto reasignado.
        """
        self.dinero -= boleto.valor
        self.millas += int(boleto.valor * 0.1)
        boleto.status = "Comprado"

    def cancelarBoleto(self, boleto):
        """
        Permite al usuario cancelar un boleto.
        """
        self.dinero += int(boleto.valor * 0.5)
        self.millas -= int(boleto.valor * 0.1)
        boleto.status = "Cancelado"
        boleto.asiento.desasignarBoleto()
        return int(boleto.valor * 0.5)

    def getInfo(self):
        """
        Obtiene la información del usuario.
        """
        return {
            "Usuario": self.nombre,
            "Balance": f"${round(self.dinero,2)}",
            "Millas": self.millas,
            "Vuelos comprados": len(self.historial),
            "Descuentos canjeados": len(self.descuentos)
        }
        
    def depositarDinero(self, valor):
        """
        Permite al usuario depositar dinero.
        """
        self.dinero += valor

    def realizarPago(self, valor):
        """
        Permite al usuario realizar un pago.
        """
        self.dinero -= valor

    def addDescuento(self, descuento):
        """
        Permite al usuario agregar un descuento.
        """
        self.descuentos.add(descuento)

    def descontarMillas(self, valor):
        """
        Permite al usuario descontar millas.
        """
        self.millas -= valor

    def getHistorial(self):
        """
        Obtiene el historial de boletos comprados por el usuario.
        """
        return self.historial