"""Modelo Cliente."""

from models.usuario import Usuario


class Cliente(Usuario):
    def solicitar_servico(self, descricao):
        return f"Solicitação criada: {descricao}"

    def avaliar_servico(self, nota, comentario):
        return {"nota": nota, "comentario": comentario}

    def get_tipo(self):
        return "Cliente"
