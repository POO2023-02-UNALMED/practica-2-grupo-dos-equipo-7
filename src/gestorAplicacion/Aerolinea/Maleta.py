from .RestriccionesMaleta import RestriccionesMaleta
class Maleta(RestriccionesMaleta):

    precioMaleta = 10.0
    excedente = 0  

    def __init__(self, id, peso, boleto):# se asignan los valores iniciales de la clase
        self.id = id
        self.peso = peso
        self.boleto = boleto
        self.destino_origen = boleto.getOrigenDestino()
        self.boleto.addEquipaje(self)
        
    def calcularPrecio(self):# se calcula el valor de la maleta segun su peso
        # Valor fijo de $5
        return round((((self.peso * 0.5)) + 3), 2)  # Convertimos el resultado final a int