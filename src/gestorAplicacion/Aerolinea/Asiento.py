class Asiento:

    def __init__(self, tipo, n_silla,  valorBase):
        self.tipo = tipo
        self.n_silla = n_silla
        self.valorBase = valorBase
        self.disponible = True
        self.vip = True if tipo == "Vip" else False
        
        # Estado del asiento (ejemplo: "Disponible", "Asignado")
        self.status = "Disponible"
        self.boleto = None  # asociado al asiento

    def asignarBoleto(self, boleto):
        self.boleto = boleto
        self.disponible = False
        self.status = "Asignado"

    def desasignarBoleto(self):
        self.boleto = None
        self.disponible = True
        self.status = "Disponible"

    def getInfo(self):
        return f"{self.n_silla}. Tipo: {self.tipo}, Valor: ${self.valorBase}"
    
    def __str__(self):
        return self.getInfo()