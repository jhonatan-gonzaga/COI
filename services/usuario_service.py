"""Serviço de autenticação de usuários."""

from repositories.usuario_repository import UsuarioRepository


class UsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def autenticar(self, email, senha):
        return self.repository.autenticar(email, senha)
