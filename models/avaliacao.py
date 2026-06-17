"""Modelo Avaliacao."""


class Avaliacao:
    def __init__(self, nota, comentario, id=None):
        self.id = id
        self.nota = int(nota)
        self.comentario = comentario

    def validar_nota(self):
        return 1 <= self.nota <= 5
