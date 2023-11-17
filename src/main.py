from gestorAplicacion.Aerolinea.Maleta import Maleta
from gestorAplicacion.Aerolinea.ServiciosEspeciales import ServiciosEspeciales
from gestorAplicacion.Aerolinea.Vuelo import Vuelo

from gestorAplicacion.Descuentos.descuentoMaleta import descuentoMaleta
from gestorAplicacion.Descuentos.descuentoVuelo import descuentoVuelo
from gestorAplicacion.Descuentos.upgradeAsiento import upgradeAsiento

from gestorAplicacion.Mascotas.Perro import Perro
from gestorAplicacion.Mascotas.Gato import Gato
                

def checkin(user):
    historial = user.getHistorial()
    print(("Información de los vuelos:", "morado"))
    
    # Iterar a través del historial de boletos
    for i in range(len(historial)):
        boleto = historial[i]
        # Mostrar información de cada boleto en la lista
        print(f"{i} . {boleto.getInfo()}")

    
    print("Por favor, seleccione el número del vuelo deseado:")
    indexVuelo = inputI()
    # Obtener el boleto seleccionado por el usuario
    boleto = historial.get(indexVuelo)
    
    print(("Vuelo seleccionado, información detallada:", "morado"))
    
    print(boleto.getInfo())
    
    opcion
    
    # verifica si ya se realizo el checkin para el vuelo
    # en caso de que ya se realizo el check in no dejaria entrar a este menu
    if ((not boleto.getCheckInRealizado()) and boleto.getStatus() != "Cancelado"):

        while (opcion != 4 and (not boleto.getCheckInRealizado())):
            separadorGrande()
            # muestra el menu del check in
            print(print((
                "Bienvenido al sistema de check-in del vuelo", "morado")), 3)
            
            print("1. Realizar check-in")
            print("2. Mejorar asiento")
            print("3. Comprar servicios especiales")
            print("4. Volver al menú anterior")
            
            print("> Seleccione una opción (1-4): ")
            opcion = inputI()
            match (opcion):
                case 1:
                    # realizar el check in
                    
                    print(
                        "Confirma el check-in? (Escriba 1 para Confirmar, 0 para Cancelar):")
                    confirmacion = inputI()
                    
                    if (confirmacion == 1):
                        boleto.setStatus("Confirmado")
                        boleto.setCheckInRealizado(True)
                        print(("CheckIn Realizado con éxito.", "verde"))
                    else:
                        print(("Proceso cancelado.", "rojo"))


                case 2:
                    mejorarAsiento(boleto)

                case 3:
                    comprarServiciosEspeciales(boleto, user)

                case 4:
                    # Volver al menu (Listo)
                    
                    aviso("¡Volviendo al menu!")
                    

                case _:
                    pass
                    aviso(("Opción incorrecta", "rojo"))

    else:
        if (boleto.getStatus() == "Cancelado"):
            
            print((
                "No es posible realizar el checkIn ya que el vuelo fue cancelado", "rojo"))
        else:
            
            print(("Usted ya realizo el Check-in para este vuelo", "rojo"))

def mejorarAsiento(boleto):
    asiento = boleto.getAsiento()
    # se verifica que el asiento sea economico
    # si es vip ya no se puede mejorar
    if (asiento.getTipo() == "Economico"):
        
        print("Desea mejorar su asiento a VIP?, esto tiene un costo de $25 (1 Si, 0 No)")
        confirmacion = inputI()
        if (confirmacion == 1):
            # Mejorar asiento
            
            print(print(("Informacion de su asiento:", "morado")))
            
            print(asiento.getInfo())
            
            # Hacer asiento vip
            asientos = (boleto.getVuelo()).getAsientos()
            print(("Asientos disponibles", "morado"))
            
            for asientoTemp in asientos:
                if (asientoTemp.getTipo() == ("Vip")):
                    print(asientoTemp.getInfo(), 2)

            
            print("Por favor, seleccione el número del asiento deseado: ")
            indexAsiento = inputI()
            # ... Cambiar y reasignar todo
            newAsiento = asientos[indexAsiento - 1]
            user = boleto.getUser()
            if (user.getDinero() >= 25):
                boleto.upgradeAsiento(asiento, newAsiento)
                boleto.getUser().realizarPago(25)
                
                print((
                    "Mejora de asiento realizado con exitOpo", "verde"))
                
            else:
                print(("Dinero insuficiente, mejora cancelada", "rojo"))

    else:
        
        print(("Su asiento ya es VIP", "verde"))
        


def comprarServiciosEspeciales(boleto, user):
    opcion = None

    while (opcion != 7):
        
        print(print(("Servicios disponibles", "morado")), 4)
        
        print("1. Comida a la carta")
        print("2. Viaje con mascota")
        print("3. Acompañante para menor de edad")
        print("4. Asistencia para pasajero con necesidades especiales")
        print("5. Transporte terrestre")
        print("6. Ver servicios contratados")
        print("7. Volver al menú anterior")
        
        print("> Seleccione una opción (1-7): ")
        opcion = inputI()
        
        match (opcion):
            case 1:
                comprarComidaCarta(boleto, user)

            case 2:
                viajarConMascota(boleto, user)

            case 3:
                contratarAcompanante(boleto, user)

            case 4:
                print(
                    "Desea contratar un asistencia para pasajero con necesidades especiales?")
                print("Este servicio no tiene ningun costo (1/0)")
                respuesta = inputI()
                if (respuesta == 1):
                    boleto.anadirServiciosEspeciales(
                        ServiciosEspeciales.ASISTENCIA_NECESIDADES_ESPECIALES)
                    
                    print((
                        "Compra realizada con exitOpo!", "verde"))
                else:
                    print("Cancelado")

            case 5:
                contratarTrasporteTerrestre(boleto, user)

            case 6:
                verServiciosContratados(boleto)

            case 7:
                # Volver al menu (Listo)
                
                aviso("¡Volviendo al menu!")
                

            case _:
                pass
                aviso(("Opción incorrecta", "rojo"))


def comprarComidaCarta(boleto, user):
    print("Desea comprar el servicio de comida a la acarta durante el vuelo? Esto tiene un costo de $40")
    match (confirmarTransaccion(user, ServiciosEspeciales.COMIDA_A_LA_CARTA.getPrecio())):
        case 1:
            # anade a el servicio a la lista del boleto
            boleto.anadirServiciosEspeciales(
                ServiciosEspeciales.COMIDA_A_LA_CARTA)
            # realiza el pago del servicio
            boleto.getUser().realizarPago(ServiciosEspeciales.COMIDA_A_LA_CARTA.getPrecio())
            print(("Compra realizada con exitOpo!", "verde"))
            

        case -1:
            print("Dinero insuficiente, compra cancelada")

        case 0:
            print("Cancelado")

        case _:
            pass


def viajarConMascota(boleto, user):
    mascota = None
    # Se pregunta si la mascota es perro o gato
    print("Desea viajar con un perro o un gato? ( 1. Perro 2. Gato)")
    op = inputI()
    
    # Se obtienen los datos de la mascota
    print("Por favor ingrese el nombre de la mascota")
    nombre = inputS()
    
    print("Por favor ingrese la raza de la mascota")
    raza = inputS()
    
    print("Por favor ingrese el tamano de la mascota")
    tamano = inputD()
    
    print("Por favor ingrese el peso de la mascota")
    peso = inputD()
    
    if (op == 1):
        # Se crea una instancia de perro
        mascota = Perro(nombre, raza, tamano, peso)
    else:
        # Se crea una instancia de gato
        mascota = Gato(nombre, raza, tamano, peso)

    # Verifica que la mascota si pueda viajar en cabina o bodega y que no sobrepase
    # el limite de 1 en cabina y 2 en bodega
    if ((mascota.puedeViajarEnCabina() and boleto.getMascotasEnCabina() < 1) or (mascota.puedeViajarEnBodega() and boleto.getMascotasEnBodega() < 2)):
        # Pregunta si desea llevarla en cabina
        print(
            "Desea llevar la mascota en cabina? (1 Si, 0 No) Esto tiene un costo de $40")
        opcion = inputI()
        
        # Si desea viajar en cabina
        if (opcion == 1):
            # Verifica que si sea posible viajar en cabina
            if (mascota.puedeViajarEnCabina() and boleto.getMascotasEnCabina() < 1):
                # Confirma la transaccion
                match (confirmarTransaccion(user, ServiciosEspeciales.MASCOTA_EN_CABINA.getPrecio())):
                    case 1:
                        # anade a el servicio a la lista del boleto
                        boleto.anadirServiciosEspeciales(
                            ServiciosEspeciales.MASCOTA_EN_CABINA)
                        # Anade la mascota a la lista del boleto
                        boleto.anadirServiciosMascota(mascota)
                        # realiza el pago del servicio
                        boleto.getUser().realizarPago(ServiciosEspeciales.MASCOTA_EN_CABINA.getPrecio())
                        print((
                            "Compra realizada con exitOpo!", "verde"))
                        

                    case 0:
                        print("Cancelado")

                    case -1:
                        print("Dinero insuficiente, compra cancelada")

                    case _:
                        pass

            elif (boleto.getMascotasEnBodega() < 2):
                # Si no puede viajar en cabina se indica que va a aviajar en bodega
                print(
                    "La mascota no cumple las restricciones de la aerolinea para viajar en cabina o ya se cumplio el limite permitido.")
                print(" Puede viajar en bodega. Esto tiene un costo de $30")
                # Se confirma la transaccion
                match (confirmarTransaccion(user, ServiciosEspeciales.MASCOTA_EN_BODEGA.getPrecio())):
                    case 1:
                        # anade a el servicio a la lista del boleto
                        boleto.anadirServiciosEspeciales(
                            ServiciosEspeciales.MASCOTA_EN_BODEGA)
                        # Anade la mascota a la lista del boleto
                        boleto.anadirServiciosMascota(mascota)
                        # realiza el pago del servicio
                        boleto.getUser().realizarPago(ServiciosEspeciales.MASCOTA_EN_BODEGA.getPrecio())
                        print((
                            "Compra realizada con exitOpo!", "verde"))
                        

                    case 0:
                        print("Cancelado")

                    case -1:
                        print("Dinero insuficiente, compra cancelada")

                    case _:
                        pass

            else:
                aviso(("No es posible viajar con la mascota en bodega ya se alcanzo el limite permitido",
                                 "rojo"))

            # Si desea viajar en bodega
        elif (boleto.getMascotasEnBodega() < 2):
            print("El viaje en bodega tiene un costo de $30")
            # Se confirma la transaccion
            match (confirmarTransaccion(user, ServiciosEspeciales.MASCOTA_EN_BODEGA.getPrecio())):
                case 1:
                    # anade a el servicio a la lista del boleto
                    boleto.anadirServiciosEspeciales(
                        ServiciosEspeciales.MASCOTA_EN_BODEGA)
                    # Anade la mascota a la lista del boleto
                    boleto.anadirServiciosMascota(mascota)
                    # realiza el pago del servicio
                    boleto.getUser().realizarPago(ServiciosEspeciales.MASCOTA_EN_BODEGA.getPrecio())
                    print((
                        "Compra realizada con exitOpo!", "verde"))
                    

                case 0:
                    print("Cancelado")

                case -1:
                    print("Dinero insuficiente, compra cancelada")

                case _:
                    pass

        else:
            aviso(("No es posible viajar con la mascota en bodega ya se alcanzo el limite permitido",
                             "rojo"))

        # Si no se puede viajar de ninguna forma
    else:
        aviso((
            "La mascota no cumple con las restricciones de la aerolinea ", "rojo"))
        aviso((
            "o ya se cumplio el limite permitido por lo tanto no puede viajar", "rojo"))


def contratarAcompanante(boleto, user):
    print("Desea contratar un acompañante para el pasajero menor de edad? Esto tiene un costo de $15")
    match (confirmarTransaccion(user, ServiciosEspeciales.ACOMPANANTE_PARA_MENOR.getPrecio())):
        case 1:
            # anade a el servicio a la lista del boleto
            boleto.anadirServiciosEspeciales(
                ServiciosEspeciales.ACOMPANANTE_PARA_MENOR)
            # realiza el pago del servicio
            boleto.getUser().realizarPago(ServiciosEspeciales.ACOMPANANTE_PARA_MENOR.getPrecio())
            
            print(("Asignado con exitOpo ✔", "verde"))
            

        case -1:
            print("Dinero insuficiente, compra cancelada")

        case 0:
            print("Cancelado")

        case _:
            pass


def contratarTrasporteTerrestre(boleto, user):
    print("Desea contratar el servicio de transporte terrestre? Esto tiene un costo de $70")
    match (confirmarTransaccion(user, ServiciosEspeciales.TRANSPORTE_TERRESTRE.getPrecio())):
        case 1:
            # anade a el servicio a la lista del boleto
            boleto.anadirServiciosEspeciales(
                ServiciosEspeciales.TRANSPORTE_TERRESTRE)
            # realiza el pago del servicio
            boleto.getUser().realizarPago(ServiciosEspeciales.TRANSPORTE_TERRESTRE.getPrecio())
            
            print(("Compra realizada con exitOpo!", "verde"))
            

        case -1:
            print("Dinero insuficiente, compra cancelada")

        case 0:
            print("Cancelado")

        case _:
            pass