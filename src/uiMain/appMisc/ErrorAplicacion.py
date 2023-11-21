
class ErrorAplicacion(Exception):
    def __init__(self, mensajeEspecifico):
        self.mensajeBase = "Manejo de errores de la Aplicación"
        super().__init__(f"{self.mensajeBase}: {mensajeEspecifico}")


# Subclases de ErrorAplicacion
class ErrorTipoA(ErrorAplicacion):
    def __init__(self, mensaje="Error base de tipo A"):
        super().__init__(mensaje)

class ErrorTipoB(ErrorAplicacion):
    def __init__(self, mensaje="Error base de tipo B"):
        super().__init__(mensaje)


# Errores de tipo A -----------------
class ErrorDineroInsuficiente(ErrorTipoA):
    def __init__(self):
        super().__init__("Dinero insuficiente en la cuenta para realizar la transacción")

class ErrorMillasInsuficientes(ErrorTipoA):
    def __init__(self):
        super().__init__("El usuario no cuenta con las millas suficientes para canjear")

# Error sugerido
class ErrorSugeridoFieldFrame(ErrorTipoA):
    def __init__(self, campos):
        super().__init__(f"Campos sin rellenar ({', '.join(campos)})")


# Errores de tipo B -----------------
class ErrorSeleccionarDropdown(ErrorTipoB):
    def __init__(self):
        super().__init__("Campos sin seleccionar")

class ErrorDepositoInvalido(ErrorTipoB):
    def __init__(self):
        super().__init__("Valor a depositar en la cuenta es inválido")

# Error sugerido
