"""Modelo Servico."""


class Servico:
    def __init__(
        self,
        descricao,
        data_prevista,
        valor,
        status,
        cliente,
        profissional,
        endereco,
        id=None,
    ):
        self.id = id
        self.descricao = descricao
        self.data_prevista = data_prevista
        self.valor = float(valor)
        self.status = status
        self.cliente = cliente
        self.profissional = profissional
        self.endereco = endereco

    def concluir(self):
        self.status = "Concluído"

    def cancelar(self):
        self.status = "Cancelado"

    def alterar_status(self, novo_status):
        self.status = novo_status

    def calcular_valor_final(self):
        return self.valor
