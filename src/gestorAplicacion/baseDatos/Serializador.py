from pickle import dump

from Boleto import Boleto


class Serializador:
    def __init__(self) :
        pass

    # antes de cada parte tengo que revisar primero que los atributos con objetos esten asignados
    # segundo  cada open debe estar dentro de un try and catch y un with
    # 1. dump(usuario)
    # 2.for Boleto in Boleto: serializar Boleto() , necesito enumerar los archivos de los
    # boletos para poner uno en cada archivo para que al cargarlo to/do pueda crear un for donde asignar cada
    #  archivo a su respectivo boleto
    #        2.1 serializarVuelo()
    #               2.1.1 for asiento in asientos: SerializarAsiento(=)
    #               2.1.2 for maleta in Maletas: SerializarMaleta(=)
    #        2.2 serializarPasajero(=)
    #        2.3 for mascota in mascotas: serializarMascota(=)
    #        2.4 for maleta in equipaje: SeriañizarMaleta(=)
    # 3. for descuento in descuentos:Serializardescuento(=) ,enummerar y meter cada descuento en un archivo
    # , para reasignarle su boleto luego

    def serializarBoleto(self):
        pass

    def SerializarVuelo(self,boleto : Boleto):
        return

    def serializarAsiento(self):
        pass

    def serializarMaleta(self):
        pass

    def serializarPasajero(self):
        pass

    def serializarMascota(self):
        pass


    def serializarDescuento(self):
        pass

