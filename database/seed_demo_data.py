"""Limpa o banco e cadastra dados ficticios para demonstracao."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.create_tables import create_tables
from database.connection import get_connection


ESPECIALIDADES = [
    ("Pedreiro", "Servicos de alvenaria, reformas e construcao."),
    ("Eletricista", "Instalacoes, manutencao e reparos eletricos."),
    ("Pintor", "Pintura residencial, comercial e acabamento."),
    ("Encanador", "Instalacoes hidraulicas, vazamentos e tubulacoes."),
    ("Carpinteiro", "Estruturas, moveis e servicos em madeira."),
    ("Mestre de obras", "Coordenacao e acompanhamento de obras."),
]

CLIENTES = [
    ("Ana Paula Nogueira", "(92) 99123-1100", "ana.cliente@demo.com", "123456"),
    ("Carlos Henrique Lima", "(92) 98444-2211", "carlos.cliente@demo.com", "123456"),
    ("Marina Souza Costa", "(92) 99222-3344", "marina.cliente@demo.com", "123456"),
]

PROFISSIONAIS = [
    {
        "nome": "Joao Batista Almeida",
        "telefone": "(92) 98111-1001",
        "email": "joao.pedreiro@demo.com",
        "senha": "123456",
        "especialidades": ["Pedreiro", "Mestre de obras"],
        "portfolio": [
            ("portfolio_alvenaria.svg", "Assentamento de parede e acabamento em residencia."),
            ("portfolio_contrapiso.svg", "Nivelamento de contrapiso para area gourmet."),
        ],
    },
    {
        "nome": "Rafaela Martins Silva",
        "telefone": "(92) 98222-1002",
        "email": "rafaela.eletrica@demo.com",
        "senha": "123456",
        "especialidades": ["Eletricista"],
        "portfolio": [
            ("portfolio_eletrica.svg", "Quadro de distribuicao organizado e identificado."),
            ("portfolio_luminaria.svg", "Instalacao de luminarias e tomadas novas."),
        ],
    },
    {
        "nome": "Bruno Carvalho Reis",
        "telefone": "(92) 98333-1003",
        "email": "bruno.pintor@demo.com",
        "senha": "123456",
        "especialidades": ["Pintor"],
        "portfolio": [
            ("portfolio_pintura.svg", "Pintura interna com acabamento acetinado."),
            ("portfolio_fachada.svg", "Revitalizacao de fachada residencial."),
        ],
    },
    {
        "nome": "Patricia Gomes Araujo",
        "telefone": "(92) 98444-1004",
        "email": "patricia.hidraulica@demo.com",
        "senha": "123456",
        "especialidades": ["Encanador"],
        "portfolio": [
            ("portfolio_hidraulica.svg", "Troca de tubulacao e pontos de agua."),
            ("portfolio_banheiro.svg", "Reparo hidraulico em banheiro social."),
        ],
    },
    {
        "nome": "Lucas Ferreira Mendes",
        "telefone": "(92) 98555-1005",
        "email": "lucas.carpinteiro@demo.com",
        "senha": "123456",
        "especialidades": ["Carpinteiro"],
        "portfolio": [
            ("portfolio_marcenaria.svg", "Bancada de madeira sob medida."),
            ("portfolio_telheiro.svg", "Estrutura de cobertura em madeira tratada."),
        ],
    },
]

SERVICOS = [
    {
        "cliente": "Ana Paula Nogueira",
        "profissional": "Joao Batista Almeida",
        "descricao": "Reforma de muro lateral com reboco e acabamento.",
        "data_prevista": "2026-06-10",
        "valor": "1850.00",
        "status": "CONCLUIDO",
        "endereco": ("Rua Borba", "120", "Centro"),
        "avaliacao": (5, "Servico muito bem feito, terminou antes do prazo."),
    },
    {
        "cliente": "Carlos Henrique Lima",
        "profissional": "Rafaela Martins Silva",
        "descricao": "Revisao eletrica completa da cozinha.",
        "data_prevista": "2026-06-14",
        "valor": "620.00",
        "status": "CONCLUIDO",
        "endereco": ("Avenida Parque", "45", "Santo Antonio"),
        "avaliacao": (5, "Profissional organizada e explicou tudo com clareza."),
    },
    {
        "cliente": "Marina Souza Costa",
        "profissional": "Bruno Carvalho Reis",
        "descricao": "Pintura de sala e dois quartos.",
        "data_prevista": "2026-06-18",
        "valor": "1450.00",
        "status": "CONCLUIDO",
        "endereco": ("Rua Acari", "77", "Pedreiras"),
        "avaliacao": (4, "Boa pintura e cuidado com a limpeza do ambiente."),
    },
    {
        "cliente": "Ana Paula Nogueira",
        "profissional": "Patricia Gomes Araujo",
        "descricao": "Conserto de vazamento na area de servico.",
        "data_prevista": "2026-06-21",
        "valor": "380.00",
        "status": "CONCLUIDO",
        "endereco": ("Rua Borba", "120", "Centro"),
        "avaliacao": (5, "Resolveu o vazamento no mesmo dia."),
    },
    {
        "cliente": "Carlos Henrique Lima",
        "profissional": "Lucas Ferreira Mendes",
        "descricao": "Instalacao de prateleiras e ajuste de porta.",
        "data_prevista": "2026-06-23",
        "valor": "540.00",
        "status": "CONCLUIDO",
        "endereco": ("Travessa Sao Jose", "19", "Jauary"),
        "avaliacao": (4, "Trabalho caprichado e material bem aproveitado."),
    },
    {
        "cliente": "Marina Souza Costa",
        "profissional": "Joao Batista Almeida",
        "descricao": "Orcamento para ampliar varanda dos fundos.",
        "data_prevista": "2026-07-02",
        "valor": "3200.00",
        "status": "EM_ANDAMENTO",
        "endereco": ("Rua Manaus", "300", "Sao Francisco"),
    },
    {
        "cliente": "Ana Paula Nogueira",
        "profissional": "Rafaela Martins Silva",
        "descricao": "Instalacao de tomada 220V para ar-condicionado.",
        "data_prevista": "2026-07-05",
        "valor": "450.00",
        "status": "AGUARDANDO",
        "endereco": ("Rua Borba", "120", "Centro"),
    },
    {
        "cliente": "Carlos Henrique Lima",
        "profissional": "Patricia Gomes Araujo",
        "descricao": "Troca de torneira e sifao da pia.",
        "data_prevista": "2026-07-08",
        "valor": "250.00",
        "status": "CANCELADO",
        "endereco": ("Avenida Parque", "45", "Santo Antonio"),
    },
]


def insert_usuario(cur, nome, telefone, email, senha, tipo):
    cur.execute(
        """
        INSERT INTO usuarios (nome, telefone, email, senha, tipo)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (nome, telefone, email, senha, tipo),
    )
    return cur.fetchone()[0]


def seed():
    create_tables(ensure_database=True)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            TRUNCATE TABLE
                imagens,
                avaliacoes,
                servicos,
                enderecos,
                profissional_especialidade,
                clientes,
                profissionais,
                usuarios,
                especialidades
            RESTART IDENTITY CASCADE
            """
        )

        especialidade_ids = {}
        for nome, descricao in ESPECIALIDADES:
            cur.execute(
                """
                INSERT INTO especialidades (nome, descricao)
                VALUES (%s, %s)
                RETURNING id
                """,
                (nome, descricao),
            )
            especialidade_ids[nome] = cur.fetchone()[0]

        cliente_ids = {}
        for nome, telefone, email, senha in CLIENTES:
            usuario_id = insert_usuario(cur, nome, telefone, email, senha, "cliente")
            cur.execute("INSERT INTO clientes (id) VALUES (%s)", (usuario_id,))
            cliente_ids[nome] = usuario_id

        profissional_ids = {}
        for profissional in PROFISSIONAIS:
            usuario_id = insert_usuario(
                cur,
                profissional["nome"],
                profissional["telefone"],
                profissional["email"],
                profissional["senha"],
                "profissional",
            )
            cur.execute("INSERT INTO profissionais (id) VALUES (%s)", (usuario_id,))
            profissional_ids[profissional["nome"]] = usuario_id

            for especialidade in profissional["especialidades"]:
                cur.execute(
                    """
                    INSERT INTO profissional_especialidade (profissional_id, especialidade_id)
                    VALUES (%s, %s)
                    """,
                    (usuario_id, especialidade_ids[especialidade]),
                )

            for arquivo, descricao in profissional["portfolio"]:
                cur.execute(
                    """
                    INSERT INTO imagens (caminho_pasta, descricao, profissional_id)
                    VALUES (%s, %s, %s)
                    """,
                    (f"uploads/{arquivo}", descricao, usuario_id),
                )

        for servico in SERVICOS:
            cur.execute(
                """
                INSERT INTO enderecos (rua, numero, bairro)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                servico["endereco"],
            )
            endereco_id = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO servicos
                    (descricao, data_prevista, valor, status, cliente_id, profissional_id, endereco_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    servico["descricao"],
                    servico["data_prevista"],
                    servico["valor"],
                    servico["status"],
                    cliente_ids[servico["cliente"]],
                    profissional_ids[servico["profissional"]],
                    endereco_id,
                ),
            )
            servico_id = cur.fetchone()[0]

            if "avaliacao" in servico:
                nota, comentario = servico["avaliacao"]
                cur.execute(
                    """
                    INSERT INTO avaliacoes (nota, comentario, servico_id, cliente_id, profissional_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        nota,
                        comentario,
                        servico_id,
                        cliente_ids[servico["cliente"]],
                        profissional_ids[servico["profissional"]],
                    ),
                )

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    seed()
    print("Dados ficticios recriados com sucesso.")
