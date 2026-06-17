"""Modelo ProfissionalAutonomo."""

from models.usuario import Usuario


class ProfissionalAutonomo(Usuario):
    def __init__(self, nome, telefone, email, senha="", especialidades=None, portfolio=None, id=None):
        super().__init__(nome, telefone, email, senha, id)
        self.especialidades = especialidades or []
        self.portfolio = portfolio or []

    def adicionar_especialidade(self, especialidade):
        if especialidade not in self.especialidades:
            self.especialidades.append(especialidade)

    def remover_especialidade(self, especialidade):
        if especialidade in self.especialidades:
            self.especialidades.remove(especialidade)

    def adicionar_imagem(self, imagem):
        self.portfolio.append(imagem)

    def listar_portfolio(self):
        return self.portfolio

    def get_tipo(self):
        return "Profissional Autônomo"
