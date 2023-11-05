from .Usuario import Usuario

class GestionUsuario:

    def __init__(self):
        self.usuarios = []
        self.inventarioMaletas = []
        self.user = Usuario("Jaime A. Guzman", "usuario@gmail.com", "123", 0)
        self.user.setDinero(2000)
        self.user.setMillas(150)
        self.usuarios.append(self.user)

    # end def
    def iniciarSesion(self, mail, contrasena):
        for usuario in self.usuarios:
            if ((usuario.getMail() == mail) and usuario.verificarContrasena(contrasena)):
                self.user = usuario
                return usuario
        return None

    def cambiarContrasena(self, usuario, contrasena, nuevaContrasena):
        if (usuario.verificarContrasena(contrasena)):
            usuario.setContrasena(nuevaContrasena)
            return usuario
        else:
            return None

    def getUser(self):
        return self.user

    def cerrarSesion(self, user):
        self.user = None
        return None
