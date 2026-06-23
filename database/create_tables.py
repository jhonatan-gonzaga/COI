"""Cria as tabelas usadas pela aplicacao."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.connection import get_connection


load_dotenv()


def create_database_if_not_exists():
    db_name = os.getenv("DB_NAME", "conecta_obras")
    conn = get_connection(os.getenv("DB_ADMIN_DB", "postgres"))
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    exists = cur.fetchone()
    if not exists:
        cur.execute(f'CREATE DATABASE "{db_name}"')
    cur.close()
    conn.close()


def create_tables(ensure_database=False):
    if ensure_database:
        create_database_if_not_exists()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(120) NOT NULL,
            telefone VARCHAR(30) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL DEFAULT '',
            tipo VARCHAR(30) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS profissionais (
            id INTEGER PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS especialidades (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) UNIQUE NOT NULL,
            descricao TEXT
        );

        CREATE TABLE IF NOT EXISTS profissional_especialidade (
            profissional_id INTEGER REFERENCES profissionais(id) ON DELETE CASCADE,
            especialidade_id INTEGER REFERENCES especialidades(id) ON DELETE CASCADE,
            PRIMARY KEY (profissional_id, especialidade_id)
        );

        CREATE TABLE IF NOT EXISTS enderecos (
            id SERIAL PRIMARY KEY,
            rua VARCHAR(120) NOT NULL,
            numero VARCHAR(20) NOT NULL,
            bairro VARCHAR(80) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS servicos (
            id SERIAL PRIMARY KEY,
            descricao TEXT NOT NULL,
            data_prevista DATE NOT NULL,
            valor NUMERIC(10, 2) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'AGUARDANDO',
            cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
            profissional_id INTEGER REFERENCES profissionais(id) ON DELETE SET NULL,
            endereco_id INTEGER NOT NULL REFERENCES enderecos(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS avaliacoes (
            id SERIAL PRIMARY KEY,
            nota INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
            comentario TEXT,
            servico_id INTEGER UNIQUE NOT NULL REFERENCES servicos(id) ON DELETE CASCADE,
            cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
            profissional_id INTEGER REFERENCES profissionais(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS imagens (
            id SERIAL PRIMARY KEY,
            caminho_pasta VARCHAR(255) NOT NULL,
            descricao TEXT,
            avaliacao_id INTEGER REFERENCES avaliacoes(id) ON DELETE CASCADE,
            profissional_id INTEGER REFERENCES profissionais(id) ON DELETE CASCADE
        );

        ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS senha VARCHAR(255) NOT NULL DEFAULT '';
        ALTER TABLE imagens ADD COLUMN IF NOT EXISTS avaliacao_id INTEGER REFERENCES avaliacoes(id) ON DELETE CASCADE;
        ALTER TABLE servicos ALTER COLUMN status SET DEFAULT 'AGUARDANDO';

        DELETE FROM avaliacoes a
        USING avaliacoes b
        WHERE a.servico_id = b.servico_id AND a.id < b.id;

        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'avaliacoes_servico_id_unique'
            ) THEN
                ALTER TABLE avaliacoes
                ADD CONSTRAINT avaliacoes_servico_id_unique UNIQUE (servico_id);
            END IF;
        END $$;

        UPDATE servicos SET status = 'AGUARDANDO' WHERE status = 'Solicitado';
        UPDATE servicos SET status = 'EM_ANDAMENTO' WHERE status = 'Em andamento';
        UPDATE servicos SET status = 'CONCLUIDO' WHERE status = 'Concluído';
        UPDATE servicos SET status = 'CANCELADO' WHERE status = 'Cancelado';

        INSERT INTO especialidades (nome, descricao) VALUES
            ('Pedreiro', 'Serviços de alvenaria, reformas e construção.'),
            ('Eletricista', 'Instalações, manutenção e reparos elétricos.'),
            ('Pintor', 'Pintura residencial, comercial e acabamento.'),
            ('Encanador', 'Instalações hidráulicas, vazamentos e tubulações.'),
            ('Carpinteiro', 'Estruturas, móveis e serviços em madeira.'),
            ('Mestre de obras', 'Coordenação e acompanhamento de obras.')
        ON CONFLICT (nome) DO NOTHING;
        """
    )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    create_tables(ensure_database=True)
    print("Banco e tabelas criados com sucesso.")
