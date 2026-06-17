"""Modelo Endereco."""


class Endereco:
    def __init__(self, rua, numero, bairro):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro

    def formatar(self):
        return f"{self.rua}, {self.numero} - {self.bairro}"
