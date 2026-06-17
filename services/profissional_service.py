"""Serviço de ProfissionalAutonomo."""

from models.profissional_autonomo import ProfissionalAutonomo
from repositories.profissional_repository import ProfissionalRepository


class ProfissionalService:
    def __init__(self):
        self.repository = ProfissionalRepository()

    def criar_profissional(self, nome, telefone, email, senha="", especialidades=None, portfolio=""):
        if isinstance(especialidades, str):
            lista_especialidades = [e.strip() for e in especialidades.split(",") if e.strip()]
        else:
            lista_especialidades = especialidades or []
        profissional = ProfissionalAutonomo(
            nome=nome,
            telefone=telefone,
            email=email,
            senha=senha,
            especialidades=lista_especialidades,
            portfolio=[portfolio] if portfolio else [],
        )
        return self.repository.criar(profissional)

    def listar_profissionais(self):
        return self.repository.listar()

    def listar_profissionais_com_metricas(self, termo=""):
        return self.repository.listar_com_metricas(termo)

    def buscar_profissional(self, profissional_id):
        return self.repository.buscar_por_id(profissional_id)

    def buscar_perfil_publico(self, profissional_id):
        return self.repository.buscar_perfil_publico(profissional_id)

    def buscar_detalhes(self, profissional_id):
        return self.repository.buscar_detalhes(profissional_id)

    def atualizar_profissional(self, profissional_id, nome, telefone, email, especialidades, portfolio, senha=""):
        profissional = ProfissionalAutonomo(
            id=profissional_id,
            nome=nome,
            telefone=telefone,
            email=email,
            senha=senha,
            especialidades=[e.strip() for e in especialidades.split(",") if e.strip()],
            portfolio=[portfolio] if portfolio else [],
        )
        self.repository.atualizar(profissional)

    def listar_especialidades(self, profissional_id=None):
        if profissional_id is not None:
            return self.repository.listar_especialidades_do_profissional(profissional_id)
        return self.repository.listar_especialidades()

    def atualizar_especialidades(self, profissional_id, especialidades):
        self.repository.atualizar_especialidades(profissional_id, especialidades)

    def adicionar_imagem_portfolio(self, profissional_id, caminho_pasta, descricao):
        self.repository.adicionar_imagem_portfolio(profissional_id, caminho_pasta, descricao)

    def atualizar_perfil_e_especialidades(self, profissional_id, telefone, email, especialidades):
        self.repository.atualizar_perfil_e_especialidades(profissional_id, telefone, email, especialidades)

    def excluir_profissional(self, profissional_id):
        self.repository.excluir(profissional_id)
