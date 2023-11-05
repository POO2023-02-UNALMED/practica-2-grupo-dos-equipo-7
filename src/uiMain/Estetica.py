def colorTexto(text, color):
    return text


def negrita(text):
    return text


def printNegrita(text):
    print(negrita(text))


def saltoO():
    print()


def salto(n):
    for x in range(n):
        print()


def aviso(text):
    print(negrita(("> > > " + text + " < < <")))


def identacionO(text, n):
    cadena = ""
    for i in range(n):
        cadena += "    "
    print(cadena + text)


def identacion(text):
    print("    " + text)


def titulo(text):
    print(negrita("# = = = " + text + " = = = #"))
# Prompts


def prompt(text):
    print("> " + text)


def inputS():
    return input("> ")


def inputI():
    return int(input("> "))


def inputD():
    return float(input("> "))


def continuar():
    prompt("Presione enter para continuar")
    input("  >_")


def separador():
    saltoO()
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    saltoO()


def separadorGrande():
    saltoO()
    print("+ = = = = = = = = = = = = = = = = = = = = = = = +")
    saltoO()


def seleccionado(text):
    print(" - - - > Seleccion: " + text + " < - - -")
