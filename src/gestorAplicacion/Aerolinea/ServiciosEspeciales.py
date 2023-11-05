class ServiciosEspeciales: #(enum)
    
	#COMIDA_A_LA_CARTA("Comida a la carta", 40),
	#MASCOTA_EN_CABINA("Mascota en cabina", 40),
	#MASCOTA_EN_BODEGA("Mascota en bodega", 30),
	#ACOMPANANTE_PARA_MENOR("Acompañante para menor", 15),
	#ASISTENCIA_NECESIDADES_ESPECIALES("Asistencia para pasajero con necesidades especiales", 0),
	#TRANSPORTE_TERRESTRE("Transporte terrestre", 70)

	def __init__(self, servicio, precio):
		self.servicio = servicio
		self.precio = precio

	def getServicio(self):
		return self.servicio

	def getPrecio(self):
		return self.precio