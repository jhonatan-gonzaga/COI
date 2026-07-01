"""Demonstracao do fluxo Cliente-Profissional salvando no banco de dados."""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parent
REPOSITORIES_DIR = ROOT_DIR / "repositories"
sys.path.insert(0, str(REPOSITORIES_DIR))

from database.connection import get_connection
from database.create_tables import create_tables
from models.servico import Servico
from services.avaliacao_service import AvaliacaoService
from services.cliente_service import ClienteService
from services.profissional_service import ProfissionalService
from services.servico_service import ServicoService


EMAIL_CLIENTE_DEMO = "maria.demo@conectaobras.com"
EMAIL_PROFISSIONAL_DEMO = "joao.demo@conectaobras.com"


def mostrar_titulo(texto):
    print(f"\n{texto}")
    print("-" * 60)


def limpar_dados_demo():
    """Remove somente os dados desta demonstracao para ela poder rodar de novo."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            DELETE FROM usuarios
            WHERE email IN (%s, %s)
            """,
            (EMAIL_CLIENTE_DEMO, EMAIL_PROFISSIONAL_DEMO),
        )
        cur.execute(
            """
            DELETE FROM enderecos e
            WHERE NOT EXISTS (
                SELECT 1
                FROM servicos s
                WHERE s.endereco_id = e.id
            )
            """
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def buscar_usuario(usuario_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, nome, telefone, email, tipo
        FROM usuarios
        WHERE id = %s
        """,
        (usuario_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "nome": row[1],
        "telefone": row[2],
        "email": row[3],
        "tipo": row[4],
    }


def main():
    create_tables(ensure_database=True)
    limpar_dados_demo()

    cliente_service = ClienteService()
    profissional_service = ProfissionalService()
    servico_service = ServicoService()
    avaliacao_service = AvaliacaoService()

    mostrar_titulo("1. Cliente e profissional sao cadastrados")
    cliente_id = cliente_service.criar_cliente(
        nome="Maria Oliveira",
        telefone="(92) 99999-1111",
        email=EMAIL_CLIENTE_DEMO,
        senha="123456",
    )
    profissional_id = profissional_service.criar_profissional(
        nome="Joao Santos",
        telefone="(92) 98888-2222",
        email=EMAIL_PROFISSIONAL_DEMO,
        senha="abcdef",
        especialidades=["Pedreiro"],
    )

    cliente = buscar_usuario(cliente_id)
    profissional = profissional_service.buscar_profissional(profissional_id)

    print(f"Cliente salvo com id {cliente_id}: {cliente['nome']} ({cliente['email']})")
    print(f"Profissional salvo com id {profissional_id}: {profissional.nome} ({profissional.email})")
    print(f"Especialidades: {', '.join(profissional.especialidades)}")

    mostrar_titulo("2. Cliente solicita/contrata o servico")
    servico_id = servico_service.criar_servico(
        {
            "descricao": "Construir uma parede divisoria e fazer o acabamento.",
            "data_prevista": "2026-07-05",
            "valor": 850.00,
            "status": Servico.STATUS_AGUARDANDO,
            "cliente_id": cliente_id,
            "profissional_id": profissional_id,
            "rua": "Rua das Palmeiras",
            "numero": "120",
            "bairro": "Centro",
        }
    )
    servico = servico_service.buscar_servico(servico_id)

    print(f"Servico salvo com id {servico_id}")
    print(f"Descricao: {servico['descricao']}")
    print(f"Profissional contratado: {servico['profissional']}")
    print(f"Endereco: {servico['rua']}, {servico['numero']} - {servico['bairro']}")
    print(f"Data prevista: {servico['data_prevista']}")
    print(f"Valor combinado: R$ {servico['valor']:.2f}")
    print(f"Status do servico: {servico['status']}")

    mostrar_titulo("3. Profissional aceita o pedido")
    servico_service.alterar_status(servico_id, Servico.STATUS_EM_ANDAMENTO)
    servico = servico_service.buscar_servico(servico_id)

    print(f"{profissional.nome} aceitou o servico de {cliente['nome']}.")
    print(f"Status salvo no banco: {servico['status']}")

    mostrar_titulo("4. Servico e executado e concluido")
    servico_service.alterar_status(servico_id, Servico.STATUS_CONCLUIDO)
    servico = servico_service.buscar_servico(servico_id)

    print(f"Servico finalizado: {servico['descricao']}")
    print(f"Valor final: R$ {servico['valor']:.2f}")
    print(f"Status salvo no banco: {servico['status']}")

    mostrar_titulo("5. Cliente avalia o profissional")
    avaliacao_id = avaliacao_service.criar_avaliacao(
        {
            "nota": 5,
            "comentario": "Servico bem feito, dentro do prazo e com otimo acabamento.",
            "servico_id": servico_id,
            "cliente_id": cliente_id,
            "profissional_id": profissional_id,
        }
    )

    avaliacoes = avaliacao_service.listar_por_profissional(profissional_id)
    avaliacao = next(item for item in avaliacoes if item["id"] == avaliacao_id)

    print(f"Avaliacao salva com id {avaliacao_id}")
    print(f"Nota registrada: {avaliacao['nota']}/5")
    print(f"Comentario: {avaliacao['comentario']}")
    print(f"Cliente avaliador: {avaliacao['cliente']}")

    mostrar_titulo("6. Resumo salvo no banco")
    servico = servico_service.buscar_servico(servico_id)
    profissional_publico = profissional_service.buscar_perfil_publico(profissional_id)

    print(f"Cliente: {servico['cliente']}")
    print(f"Profissional: {servico['profissional']}")
    print(f"Servico: {servico['descricao']}")
    print(f"Status final: {servico['status']}")
    print(f"Avaliado: {'Sim' if servico['avaliado'] else 'Nao'}")
    print(f"Nota media do profissional: {profissional_publico['nota_media']}")


if __name__ == "__main__":
    main()
