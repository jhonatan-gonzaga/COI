"""Serviço de autenticação."""

from repositories.usuario_repository import UsuarioRepository


class AuthService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def autenticar(self, email, senha):
        return self.repository.autenticar(email, senha)
