class Animal:
    """
    Clase que representa a un animal.
    Se usa como una "Interfaz" para las subclases.
    Atributos:
        nombre (str): Nombre del animal.
        raza (str): Raza del animal.
    """

    def __init__(self, nombre, raza):
        """
        Inicializa un objeto de la clase Animal.
        """
        self.nombre = nombre
        self.raza = raza

    def puedeViajarEnCabina(self):
        """
        Método para determinar si el animal puede viajar en la cabina.
        Este método es implementado en las subclases.
        """
        pass

    def puedeViajarEnBodega(self):
        """
        Método para determinar si el animal puede viajar en la bodega.
        Este método es implementado en las subclases.
        """
        pass