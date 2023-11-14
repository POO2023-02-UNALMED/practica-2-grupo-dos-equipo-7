from pickle import dump

from Boleto import Boleto


class Serializador:
    def __init__(self) :
        return

    

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


    def serializarUsuario(self,usuario : Usuario ):
        with open("mainUser.txt","wb") as file:
            serializacion = pickle.dump(usuario, file)
        serializarDescuento(usuario.getDescuentos())
        serializarBoleto(Usuario.getHistorial())
        return


    def serializarBoleto(self, boletos : Boleto[]):
        count = 1
        for boleto in boletos :

            with open(f"boleto{count}.txt","wb") as file:
                serializacion = pickle.dump(boleto,file)

            serializarVuelo(boleto.getVuelo())
            serializarMascota(boleto.getMascotas())
            serializarDescuento(boleto.getDescuentos())
            serializarServicio(boleto.getServiciosContratados())
            
        


        pass

    def serializarEquipaje(self,Equipaje: Maleta[]):
        for maleta in Equipaje:
            with open("Equipaje.txt","wb") as file:
                serializacion = pickle.dump(maleta,file)
        
        pass

    def SerializarVuelo(self,vuelo : Vuelo):

        return

    def serializarAsiento(self,Asientos : Asiento[]):
        pass

    def serializarMaletas(self, Maletas : Maleta[]):
        pass

    def serializarPasajero(self,pasajero : Pasajero):
        pass

    def serializarMascota(self, Mascotas : Animal[]):
        pass


    def serializarDescuento(self,descuentos : Descuento[]):
        pass
