"""Classes de usuários do Conecta Obras."""

from abc import ABC, abstractmethod


class Usuario(ABC):
    def __init__(self, nome, telefone, email, senha="", id=None):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.senha = senha

    def atualizar_dados(self, nome=None, telefone=None, email=None, senha=None):
        if nome:
            self.nome = nome
        if telefone:
            self.telefone = telefone
        if email:
            self.email = email
        if senha:
            self.senha = senha

    @abstractmethod
    def get_tipo(self):
        pass

    def __str__(self):
        return f"{self.get_tipo()}: {self.nome} ({self.email})"
