class Descuento:  # Abstracta

    def __init__(self):
        self.guardado = False  # Indica si el descuento ha sido guardado en la cuenta del usuario
        self.usado = False  # Indica si el descuento ha sido usado
        self.boleto = None  # El boleto al que se aplica el descuento
        self.user = None  # El usuario al que se asigna el descuento
        self.tipo = None  # El tipo de descuento
        self.estado = None  # El estado del descuento (Disponible o Usado)

    def usar(self):
        self.estado = "Usado"
        self.usado = True
        self.guardar()

    def isUsado(self):
        return self.usado

    def getTipo(self):
        return self.tipo

    def guardar(self):
        if (not self.guardado):
            self.user.addDescuento(self)
            self.guardado = True

    def init(self, user):
        self.user = user
        self.estado = "Disponible"

    def aplicarDescuento(self, boleto):
        pass

    def getInfo(self):
        return f"Tipo: {self.tipo}, Estado: {self.estado}"
