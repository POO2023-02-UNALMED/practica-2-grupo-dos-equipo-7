
class ErrorAplicacion(Exception):
    # Hereda de Exception, se dispara cuando se detecta un error en la aplicación
    def __init__(self, mensajeEspecifico):
        self.mensajeBase = "Manejo de errores de la Aplicación"
        # Mensaje de error que se mostrará al usuario, se concatena con el mensaje específico
        super().__init__(f"{self.mensajeBase}: {mensajeEspecifico}")


# Subclases de ErrorAplicacion (ErrorCuentaUsuario, ErrorAccionUsuario)

# Errores de tipo A (Cuenta del usuario)
class ErrorCuentaUsuario(ErrorAplicacion):
    def __init__(self, mensaje="Error al realizar una operación en la cuenta del usuario"):
        super().__init__(mensaje)
        
# Errores de tipo A -----------------
class ErrorDineroInsuficiente(ErrorCuentaUsuario):
    def __init__(self):
        super().__init__("Dinero insuficiente en la cuenta para realizar la transacción")

class ErrorMillasInsuficientes(ErrorCuentaUsuario):
    def __init__(self):
        super().__init__("El usuario no cuenta con las millas suficientes para canjear")

# Error sugerido 1 (Búsqueda sin resultados)
class ErrorBusquedaInvalida(ErrorCuentaUsuario):
    # Se dispara cuando el usuario realiza una búsqueda invalida y no se encuentran resultados
    def __init__(self):
        super().__init__("No se encontraron resultados para la búsqueda realizada")

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Errores de tipo B (Acciones del usuario)
class ErrorAccionUsuario(ErrorAplicacion):
    def __init__(self, mensaje="Error generado por una acción del usuario"):
        super().__init__(mensaje)


# Errores de tipo B (Acciones del usuario) -----------------
class ErrorSeleccionarDropdown(ErrorAccionUsuario):
    # Se dispara cuando el usuario no selecciona un elemento de un dropdown y desea continuar
    def __init__(self):
        super().__init__("Hay al menos un elemento del dropdown sin seleccionar")

class ErrorDepositoInvalido(ErrorAccionUsuario):
    # Se disparará cuando el usuario intente depositar un valor inválido (String o valor negativo)
    def __init__(self):
        super().__init__("Valor a depositar en la cuenta inválido, no se permiten letras ni valores negativos")

# Error sugerido 2 (Campos sin rellenar en FieldFrame)
class ErrorSugeridoFieldFrame(ErrorCuentaUsuario):
    # Se dispara cuando el usuario no rellena todos los campos de un FieldFrame y desea continuar
    def __init__(self, campos):
        super().__init__(f"Campos sin rellenar ({', '.join(campos)})")