"""Repositório de Avaliação."""

from database.connection import get_connection


class AvaliacaoRepository:

    #cria uma avaliação na tabela 'avaliacoes' com seus atributos, retornando o seu id gerado
    def criar(self, dados):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO avaliacoes (nota, comentario, servico_id, cliente_id, profissional_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                dados["nota"],
                dados["comentario"],
                dados["servico_id"],
                dados["cliente_id"],
                dados.get("profissional_id") or None,
            ),
        )
        avaliacao_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return avaliacao_id

    #lista todas as avaliações cadastradas no sistema, com o nome e o serviço
    def listar(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT a.id, a.nota, a.comentario, s.descricao, uc.nome, up.nome
            FROM avaliacoes a
            JOIN servicos s ON s.id = a.servico_id
            JOIN usuarios uc ON uc.id = a.cliente_id
            LEFT JOIN usuarios up ON up.id = a.profissional_id
            ORDER BY a.id DESC
            """
        )
        avaliacoes = cur.fetchall()
        cur.close()
        conn.close()
        return avaliacoes
    
    # lista todas as avaliações de um profissional específico, incluindo as fotos anexadas.
    def listar_por_profissional(self, profissional_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT a.id, a.nota, a.comentario, s.descricao, uc.nome AS cliente,
                   regexp_replace(i.caminho_pasta, '^uploads/', '') AS caminho_pasta
            FROM avaliacoes a
            JOIN servicos s ON s.id = a.servico_id
            JOIN usuarios uc ON uc.id = a.cliente_id
            LEFT JOIN imagens i ON i.avaliacao_id = a.id
            WHERE a.profissional_id = %s
            ORDER BY a.id DESC
            """,
            (profissional_id,),
        )
        colunas = [desc[0] for desc in cur.description]
        avaliacoes = [dict(zip(colunas, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return avaliacoes
    
    #Verifica se um serviço específico já recebeu alguma avaliação, pegando somente a primeira avaliação, se existir
    def existe_por_servico(self, servico_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM avaliacoes WHERE servico_id = %s", (servico_id,))
        existe = cur.fetchone() is not None
        cur.close()
        conn.close()
        return existe
