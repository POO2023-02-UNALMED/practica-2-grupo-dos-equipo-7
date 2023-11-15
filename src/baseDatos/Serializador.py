from pickle import dump

# Imports correctos
from gestorAplicacion.Aerolinea.Asiento import Asiento
from gestorAplicacion.Aerolinea.Boleto import Boleto
from gestorAplicacion.Aerolinea.Maleta import Maleta
from gestorAplicacion.Aerolinea.RestriccionesMaleta import RestriccionesMaleta
from gestorAplicacion.Aerolinea.ServiciosEspeciales import ServiciosEspeciales
from gestorAplicacion.Aerolinea.Vuelo import Vuelo

from gestorAplicacion.Cuenta.Usuario import Usuario

from gestorAplicacion.Descuentos.Descuento import Descuento
from gestorAplicacion.Descuentos.descuentoMaleta import descuentoMaleta
from gestorAplicacion.Descuentos.descuentoVuelo import descuentoVuelo
from gestorAplicacion.Descuentos.upgradeAsiento import upgradeAsiento

from gestorAplicacion.Mascotas.Animal import Animal
from gestorAplicacion.Mascotas.Perro import Perro
from gestorAplicacion.Mascotas.Gato import Gato

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
        with open("baseDatos/temp/mainUser.txt","wb") as file:
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
