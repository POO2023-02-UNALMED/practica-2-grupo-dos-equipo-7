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

    
    prompt("Por favor, seleccione el número del vuelo deseado:")
    indexVuelo = inputI()
    # Obtener el boleto seleccionado por el usuario
    boleto = historial.get(indexVuelo)
    
    print(("Vuelo seleccionado, información detallada:", "morado"))
    
    print(boleto.getInfo())
    
    continuar()
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
            
            prompt("> Seleccione una opción (1-4): ")
            opcion = inputI()
            match (opcion):
                case 1:
                    # realizar el check in
                    
                    prompt(
                        "Confirma el check-in? (Escriba 1 para Confirmar, 0 para Cancelar):")
                    confirmacion = inputI()
                    
                    if (confirmacion == 1):
                        boleto.setStatus("Confirmado")
                        boleto.setCheckInRealizado(True)
                        print(("CheckIn Realizado con éxito.", "verde"))
                    else:
                        print(("Proceso cancelado.", "rojo"))

                    continuar()

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
            continuar()
        else:
            
            print(("Usted ya realizo el Check-in para este vuelo", "rojo"))
            continuar()

def mejorarAsiento(boleto):
    asiento = boleto.getAsiento()
    # se verifica que el asiento sea economico
    # si es vip ya no se puede mejorar
    if (asiento.getTipo() == "Economico"):
        
        prompt("Desea mejorar su asiento a VIP?, esto tiene un costo de $25 (1 Si, 0 No)")
        confirmacion = inputI()
        if (confirmacion == 1):
            # Mejorar asiento
            
            print(print(("Informacion de su asiento:", "morado")))
            
            print(asiento.getInfo())
            
            # Hacer asiento vip
            asientos = (boleto.getVuelo()).getAsientos()
            printNegrita(("Asientos disponibles", "morado"))
            
            for asientoTemp in asientos:
                if (asientoTemp.getTipo() == ("Vip")):
                    print(asientoTemp.getInfo(), 2)

            
            prompt("Por favor, seleccione el número del asiento deseado: ")
            indexAsiento = inputI()
            # ... Cambiar y reasignar todo
            newAsiento = asientos[indexAsiento - 1]
            user = boleto.getUser()
            if (user.getDinero() >= 25):
                boleto.upgradeAsiento(asiento, newAsiento)
                boleto.getUser().realizarPago(25)
                
                printNegrita((
                    "Mejora de asiento realizado con exitOpo", "verde"))
                
            else:
                print(("Dinero insuficiente, mejora cancelada", "rojo"))

            continuar()
    else:
        
        print(("Su asiento ya es VIP", "verde"))
        
        continuar()


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
        
        prompt("> Seleccione una opción (1-7): ")
        opcion = inputI()
        
        match (opcion):
            case 1:
                comprarComidaCarta(boleto, user)

            case 2:
                viajarConMascota(boleto, user)

            case 3:
                contratarAcompanante(boleto, user)

            case 4:
                prompt(
                    "Desea contratar un asistencia para pasajero con necesidades especiales?")
                prompt("Este servicio no tiene ningun costo (1/0)")
                respuesta = inputI()
                if (respuesta == 1):
                    boleto.anadirServiciosEspeciales(
                        ServiciosEspeciales.ASISTENCIA_NECESIDADES_ESPECIALES)
                    
                    printNegrita((
                        "Compra realizada con exitOpo!", "verde"))
                else:
                    prompt("Cancelado")

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
                continuar()


def comprarComidaCarta(boleto, user):
    prompt("Desea comprar el servicio de comida a la acarta durante el vuelo? Esto tiene un costo de $40")
    match (confirmarTransaccion(user, ServiciosEspeciales.COMIDA_A_LA_CARTA.getPrecio())):
        case 1:
            # anade a el servicio a la lista del boleto
            boleto.anadirServiciosEspeciales(
                ServiciosEspeciales.COMIDA_A_LA_CARTA)
            # realiza el pago del servicio
            boleto.getUser().realizarPago(ServiciosEspeciales.COMIDA_A_LA_CARTA.getPrecio())
            printNegrita(("Compra realizada con exitOpo!", "verde"))
            
            continuar()

        case -1:
            prompt("Dinero insuficiente, compra cancelada")
            continuar()

        case 0:
            prompt("Cancelado")
            continuar()

        case _:
            pass


def viajarConMascota(boleto, user):
    mascota = None
    # Se pregunta si la mascota es perro o gato
    prompt("Desea viajar con un perro o un gato? ( 1. Perro 2. Gato)")
    op = inputI()
    
    # Se obtienen los datos de la mascota
    prompt("Por favor ingrese el nombre de la mascota")
    nombre = inputS()
    
    prompt("Por favor ingrese la raza de la mascota")
    raza = inputS()
    
    prompt("Por favor ingrese el tamano de la mascota")
    tamano = inputD()
    
    prompt("Por favor ingrese el peso de la mascota")
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
        prompt(
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
                        printNegrita((
                            "Compra realizada con exitOpo!", "verde"))
                        
                        continuar()

                    case 0:
                        prompt("Cancelado")
                        continuar()

                    case -1:
                        prompt("Dinero insuficiente, compra cancelada")
                        continuar()

                    case _:
                        pass

            elif (boleto.getMascotasEnBodega() < 2):
                # Si no puede viajar en cabina se indica que va a aviajar en bodega
                prompt(
                    "La mascota no cumple las restricciones de la aerolinea para viajar en cabina o ya se cumplio el limite permitido.")
                prompt(" Puede viajar en bodega. Esto tiene un costo de $30")
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
                        printNegrita((
                            "Compra realizada con exitOpo!", "verde"))
                        
                        continuar()

                    case 0:
                        prompt("Cancelado")
                        continuar()

                    case -1:
                        prompt("Dinero insuficiente, compra cancelada")
                        continuar()

                    case _:
                        pass

            else:
                aviso(("No es posible viajar con la mascota en bodega ya se alcanzo el limite permitido",
                                 "rojo"))
                continuar()

            # Si desea viajar en bodega
        elif (boleto.getMascotasEnBodega() < 2):
            prompt("El viaje en bodega tiene un costo de $30")
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
                    printNegrita((
                        "Compra realizada con exitOpo!", "verde"))
                    
                    continuar()

                case 0:
                    prompt("Cancelado")
                    continuar()

                case -1:
                    prompt("Dinero insuficiente, compra cancelada")
                    continuar()

                case _:
                    pass

        else:
            aviso(("No es posible viajar con la mascota en bodega ya se alcanzo el limite permitido",
                             "rojo"))
            continuar()

        # Si no se puede viajar de ninguna forma
    else:
        aviso((
            "La mascota no cumple con las restricciones de la aerolinea ", "rojo"))
        aviso((
            "o ya se cumplio el limite permitido por lo tanto no puede viajar", "rojo"))
        continuar()


def contratarAcompanante(boleto, user):
    prompt("Desea contratar un acompañante para el pasajero menor de edad? Esto tiene un costo de $15")
    match (confirmarTransaccion(user, ServiciosEspeciales.ACOMPANANTE_PARA_MENOR.getPrecio())):
        case 1:
            # anade a el servicio a la lista del boleto
            boleto.anadirServiciosEspeciales(
                ServiciosEspeciales.ACOMPANANTE_PARA_MENOR)
            # realiza el pago del servicio
            boleto.getUser().realizarPago(ServiciosEspeciales.ACOMPANANTE_PARA_MENOR.getPrecio())
            
            printNegrita(("Asignado con exitOpo ✔", "verde"))
            
            continuar()

        case -1:
            prompt("Dinero insuficiente, compra cancelada")
            continuar()

        case 0:
            prompt("Cancelado")
            continuar()

        case _:
            pass


def contratarTrasporteTerrestre(boleto, user):
    prompt("Desea contratar el servicio de transporte terrestre? Esto tiene un costo de $70")
    match (confirmarTransaccion(user, ServiciosEspeciales.TRANSPORTE_TERRESTRE.getPrecio())):
        case 1:
            # anade a el servicio a la lista del boleto
            boleto.anadirServiciosEspeciales(
                ServiciosEspeciales.TRANSPORTE_TERRESTRE)
            # realiza el pago del servicio
            boleto.getUser().realizarPago(ServiciosEspeciales.TRANSPORTE_TERRESTRE.getPrecio())
            
            printNegrita(("Compra realizada con exitOpo!", "verde"))
            
            continuar()

        case -1:
            prompt("Dinero insuficiente, compra cancelada")
            continuar()

        case 0:
            prompt("Cancelado")
            continuar()

        case _:
            pass


def verServiciosContratados(boleto):
    if (len(boleto.getServiciosContratados()) != 0):
        print((("Usted tiene los siguientes servicios contratados"), "morado"))
        
        index = 0
        for servicio in boleto.getServiciosContratados():
            print(
                f"Servicio: {servicio.getServicio()} por un valor de: ${servicio.getPrecio()}")
            if (servicio == ServiciosEspeciales.MASCOTA_EN_CABINA or servicio == ServiciosEspeciales.MASCOTA_EN_BODEGA):
                print("	-" + boleto.getMascotas()[index])
                index += 1
        continuar()

    else:
        print(("No tiene servicios contratados", "morado"))
        continuar()


def confirmarTransaccion(user, valor):
    prompt("Confirmar Transaccion (Escriba 1 para Confirmar, 0 para Cancelar)")
    confirmacion = inputI()
    
    if (confirmacion == 1):
        if (user.getDinero() >= valor):
            return 1
        else:
            return -1
    else:
        return 0


def canjearMillas(user):
    seleccionado("Canjear millas")
    separadorGrande()
    print(f"Hola {user.getNombre()}", 3)
    
    opcion = None

    while (opcion != 6):
        print(f"En este momento usted posee {user.getMillas()} millas")
        
        prompt("Escoja en que desea canjear sus millas")
        
        # print("Menu")
        print("1. Mejora de silla" +
                   " (" + upgradeAsiento.costoMillas + ")")
        print("2. Descuento vuelo" +
                   " (" + descuentoVuelo.costoMillas + ")")
        print("3. Descuento maleta" +
                   " (" + descuentoMaleta.costoMillas + ")")
        print("4. Aplicar descuentos")
        print("5. Ver descuentos del usuario")
        print("6. Volver al menú anterior")
        
        prompt("> Seleccione una opción (1-6): ")
        opcion = inputI()
        
        # Imprimir las opciones
        match (opcion):
            case 1:
                match 
            
                        printNegrita(
                            
                        
                        prompt(
                            "Desea aplicar el descuendo de una vez? (1 si / 0 no)")
                        aplicar = inputI()
                        if (aplicar == 1):
                        else:
                            descuento = upgradeAsiento(user)
                            descuento.guardar()
                            
                            printNegrita((
                                "Se guardo el descuento en su cuenta, puedes aplicarlo cuando desees",
                                "verde"))
                            
                            continuar()
                            
                    case -1:
                        prompt("Millas insuficientes!")

                    case 0:
                        prompt("Operacion cancelada")

                    case _:
                        pass

            case 2:
                match (verificarMillas(user, descuentoVuelo.costoMillas)):
                    case 1:
                        user.descontarMillas(descuentoVuelo.costoMillas)
                        printNegrita(
                            f"Canjeado con éxito, millas restantes: {user.getMillas()}")
                        
                        prompt(
                            "Desea aplicar el descuendo de una vez? (1 si / 0 no)")
                        aplicar = inputI()
                        if (aplicar == 1):
                            descuento = descuentoVuelo(user)
                            millasVuelo(user, descuento)
                        else:
                            descuento = descuentoVuelo(user)
                            descuento.guardar()
                            
                            printNegrita((
                                "Se guardo el descuento en su cuenta, puedes aplicarlo cuando desees",
                                "verde"))
                            
                            continuar()
                            
                    case -1:
                        prompt("Millas insuficientes!")

                    case 0:
                        prompt("Operacion cancelada")

                    case _:
                        pass

            case 3:
                match (verificarMillas(user, descuentoMaleta.costoMillas)):
                    case 1:
                        user.descontarMillas(descuentoMaleta.costoMillas)
                        printNegrita(
                            f"Canjeado con éxito, millas restantes: {user.getMillas()}")
                        
                        prompt(
                            "Desea aplicar el descuendo de una vez? (1 si / 0 no)")
                        aplicar = inputI()
                        if (aplicar == 1):
                            descuento = descuentoMaleta(user)
                            millasMaleta(user, descuento)
                        else:
                            descuento = descuentoMaleta(user)
                            descuento.guardar()
                            
                            printNegrita((
                                "Se guardo el descuento en su cuenta, puedes aplicarlo cuando desees",
                                "verde"))
                            
                            continuar()
                            
                    case -1:
                        prompt("Millas insuficientes!")

                    case 0:
                        prompt("Operacion cancelada")

                    case _:
                        pass

            case 4:
                # Aplicar descuento
                descuentos = verDescuentos(user, 1)
                
                # Solicitar al usuario que seleccione un vuelo y se selecciona.
                prompt("Por favor, seleccione el número del descuento deseado: ")
                index = inputI()
                descuento = descuentos.get(index)
                match (descuento.getTipo()):
                    case "Mejora de asiento":
                        millasAsiento(user, descuento)

                    case "Descuento Vuelo":
                        millasVuelo(user, descuento)

                    case "Descuento de maleta":
                        millasMaleta(user, descuento)

                    case _:
                        pass

            case 5:
                # Ver descuento
                prompt(
                    "Desea ver solo los descuentos disponibles/canjeados o los aplicados tambien (1 / 0)")
                op = inputI()
                verDescuentos(user, op)
                
                continuar()

            case 6:
                aviso(("Volviendo al menu", "rojo"))
                

            case _:
                pass
                aviso(("Opción incorrecta", "rojo"))
        separadorGrande()


def millasAsiento(user, descuento):
    boleto = selecBoleto(user)
    asiento = boleto.getAsiento()
    # se verifica que el asiento sea economico
    # si es vip ya no se puede mejorar

    if (asiento.getTipo() == "Economico"):
        # Hacer asiento vip
        asientos = (boleto.getVuelo()).getAsientos()
        printNegrita(("Asientos disponibles", "morado"))
        
        for asientoTemp in asientos:
            if (asientoTemp.getTipo() == ("Vip")):
                print(asientoTemp.getInfo(), 2)

        
        prompt("Por favor, seleccione el número del asiento deseado: ")
        indexAsiento = inputI()
        # ... Cambiar y reasignar todo
        newAsiento = asientos[indexAsiento - 1]
        boleto.upgradeAsientoMillas(asiento, newAsiento)
        descuento.aplicarDescuento(boleto)
        
        printNegrita((
            "Mejora de asiento realizado con exitOpo", "verde"))
        
        printNegrita(("Detalles del nuevo asiento:", "morado"))
        
        print((boleto.getAsiento()).getInfo())
        
        continuar()
    else:
        descuento.guardar()
        
        printNegrita((
            "Su asiento ya es VIP, se guardo el descuento en su cuenta", "verde"))
        
        continuar()
        


def millasVuelo(user, descuento):
    boleto = selecBoleto(user)
    descuento.aplicarDescuento(boleto)
    # Listo, su costo de maleta ha sdo reducido en un % y se ha regresado el dinero
    printNegrita(
        f"Se ha aplicado un {descuentoVuelo.descuento} % de descuento en el valor de su vuelo, ahorro de: $ {boleto.getValorInicial() * (0.2)}")
    
    continuar()


def verDescuentos(user, op):
    
    descuentos = user.getDescuentos()
    print(print(("Descuentos disponibles:", "morado")), 4)
    
    if (op == 1):
        # Iterar a través del historial de boletos
        for i in range(len(descuentos)):
            descuento = descuentos.get(i)
            if (descuento.isUsado() == False):
                # Mostrar información de cada boleto en la lista
                print(i + ". " + descuento.getInfo())
    else:
        # Iterar a través del historial de boletos
        for i in range(len(descuentos)):
            descuento = descuentos.get(i)
            # Mostrar información de cada boleto en la lista
            print(i + ". " + descuento.getInfo())
    return descuentos


def selecBoleto(user):
    # Obtener el historial de boletos del usuario
    historial = user.getHistorial()
    
    printNegrita(("Información de los vuelos:", "morado"))
    
    # Iterar a través del historial de boletos
    for i in range(len(historial)):
        boleto = historial[i]
        # Mostrar información de cada boleto en la lista
        print(f"{i} . {boleto.getInfo()}")

    
    prompt("Por favor, seleccione el número del vuelo deseado:")
    indexVuelo = inputI()
    # Obtener el boleto seleccionado por el usuario
    boleto = historial.get(indexVuelo)
    
    print(("Vuelo seleccionado, información detallada:", "morado"))
    
    print(boleto.getInfo())
    
    continuar()
    
    return boleto


def verificarMillas(user, valor):
    prompt("Confirmar canjeo de millas (1 si / 0 no)")
    confirmacion = inputI()
    
    if (confirmacion == 1):
        if (user.getMillas() >= valor):
            return 1
        else:
            return -1

    else:
        return 0


def millasMaleta(user, descuento):
    boleto = selecBoleto(user)
    descuento.aplicarDescuento(boleto)
    # Listo, su costo de maleta ha sdo reducido en un % y se ha regresado el dinero
    printNegrita(
        f"Se ha aplicado un {descuentoMaleta.descuento}% de descuento en el costo de su equipaje, ahorro de: ${boleto.getValorInicial() * 0.2}")
    
    continuar()


main()
