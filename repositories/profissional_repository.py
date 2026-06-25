"""Repositório de ProfissionalAutonomo."""

from database.connection import get_connection
from models.profissional_autonomo import ProfissionalAutonomo


class ProfissionalRepository:

    #cria o profissional colocando todas as suas informações na tabela 'usuarios'
    def criar(self, profissional):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (nome, telefone, email, senha, tipo) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (profissional.nome, profissional.telefone, profissional.email, profissional.senha, "profissional"),
        )
        usuario_id = cur.fetchone()[0]
        cur.execute("INSERT INTO profissionais (id) VALUES (%s)", (usuario_id,))
        for especialidade in profissional.especialidades:
            cur.execute(
                """
                INSERT INTO especialidades (nome, descricao)
                VALUES (%s, %s)
                ON CONFLICT (nome) DO UPDATE SET descricao = EXCLUDED.descricao
                RETURNING id
                """,
                (especialidade, ""),
            )
            especialidade_id = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO profissional_especialidade (profissional_id, especialidade_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (usuario_id, especialidade_id),
            )
        conn.commit()
        cur.close()
        conn.close()
        return usuario_id

    #lista todos os profissionais cadastrados,calculando a nota média da tabela avaliacoes
    def listar(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT u.id, u.nome, u.telefone, u.email, u.senha,
                   COALESCE(string_agg(DISTINCT e.nome, ', ' ORDER BY e.nome), ''),
                   COALESCE(ROUND(AVG(a.nota)::numeric, 1), 0) AS nota_media
            FROM usuarios u
            JOIN profissionais p ON p.id = u.id
            LEFT JOIN profissional_especialidade pe ON pe.profissional_id = p.id
            LEFT JOIN especialidades e ON e.id = pe.especialidade_id
            LEFT JOIN avaliacoes a ON a.profissional_id = p.id
            GROUP BY u.id, u.nome, u.telefone, u.email, u.senha
            ORDER BY u.nome
            """
        )
        profissionais = []
        for row in cur.fetchall():
            especialidades = [item.strip() for item in row[5].split(",") if item.strip()]
            profissional = ProfissionalAutonomo(
                id=row[0],
                nome=row[1],
                telefone=row[2],
                email=row[3],
                senha=row[4],
                portfolio=[],
                especialidades=especialidades,
            )
            profissional.nota_media = float(row[6])
            profissionais.append(profissional)
        cur.close()
        conn.close()
        return profissionais

    # lista todos os profissionais permitindo buscar por nome ou especialidade, trazendo a nota média da tabela avaliacoes
    def listar_com_metricas(self, termo=""):
        conn = get_connection()
        cur = conn.cursor()
        busca = f"%{termo}%"
        cur.execute(
            """
            SELECT u.id, u.nome, u.telefone, u.email,
                   COALESCE(string_agg(DISTINCT e.nome, ', ' ORDER BY e.nome), '') AS especialidades,
                   COALESCE(ROUND(AVG(a.nota)::numeric, 1), 0) AS nota_media,
                   COUNT(a.id) AS total_avaliacoes
            FROM usuarios u
            JOIN profissionais p ON p.id = u.id
            LEFT JOIN profissional_especialidade pe ON pe.profissional_id = p.id
            LEFT JOIN especialidades e ON e.id = pe.especialidade_id
            LEFT JOIN avaliacoes a ON a.profissional_id = p.id
            WHERE (%s = '' OR u.nome ILIKE %s OR e.nome ILIKE %s)
            GROUP BY u.id, u.nome, u.telefone, u.email
            ORDER BY nota_media DESC, total_avaliacoes DESC, u.nome
            """,
            (termo, busca, busca),
        )
        colunas = [desc[0] for desc in cur.description]
        profissionais = [dict(zip(colunas, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return profissionais
    
    # busca os profissionais por id
    def buscar_por_id(self, profissional_id):
        profissionais = [p for p in self.listar() if p.id == int(profissional_id)]
        return profissionais[0] if profissionais else None
    
    #Busca as informações básicas do profissional na tabela usuarios e calcula sua nota média na tabela avaliacoes para exibição pública
    def buscar_perfil_publico(self, profissional_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT u.id, u.nome, u.telefone, u.email,
                   COALESCE(ROUND(AVG(a.nota)::numeric, 1), 0) AS nota_media
            FROM usuarios u
            JOIN profissionais p ON p.id = u.id
            LEFT JOIN avaliacoes a ON a.profissional_id = p.id
            WHERE u.id = %s
            GROUP BY u.id, u.nome, u.telefone, u.email
            """,
            (profissional_id,),
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
            "nota_media": float(row[4]),
        }

    # busca o perfil do profissional trazendo seus dados gerais, a lista de fotos da tabela imagens e os comentários com os nomes dos clientes vindos da tabela avaliacoes
    def buscar_detalhes(self, profissional_id):
        profissionais = self.listar_com_metricas()
        profissional = next((p for p in profissionais if p["id"] == int(profissional_id)), None)
        if not profissional:
            return None
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT i.id,
                   regexp_replace(i.caminho_pasta, '^uploads/', '') AS caminho_pasta,
                   i.descricao, a.nota, a.comentario
            FROM imagens i
            LEFT JOIN avaliacoes a ON a.id = i.avaliacao_id
            WHERE i.profissional_id = %s
            ORDER BY i.id DESC
            """,
            (profissional_id,),
        )
        profissional["portfolio"] = [
            {
                "id": row[0],
                "caminho_pasta": row[1],
                "descricao": row[2],
                "nota": row[3],
                "comentario": row[4],
            }
            for row in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT a.id, a.nota, a.comentario, uc.nome AS cliente
            FROM avaliacoes a
            JOIN usuarios uc ON uc.id = a.cliente_id
            WHERE a.profissional_id = %s
            ORDER BY a.id DESC
            """,
            (profissional_id,),
        )
        profissional["avaliacoes"] = [
            {"id": row[0], "nota": row[1], "comentario": row[2], "cliente": row[3]}
            for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return profissional
    
    # insere uma imagem na tabela imagens com o id do profissional relacionado
    def adicionar_imagem_portfolio(self, profissional_id, caminho_pasta, descricao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO imagens (caminho_pasta, descricao, profissional_id)
            VALUES (%s, %s, %s)
            """,
            (caminho_pasta, descricao, profissional_id),
        )
        conn.commit()
        cur.close()
        conn.close()

    # atualiza o telefone, especialidade e email do profissional
    def atualizar_perfil_e_especialidades(self, profissional_id, telefone, email, especialidades):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET telefone = %s, email = %s WHERE id = %s",
            (telefone, email, profissional_id),
        )
        cur.execute("DELETE FROM profissional_especialidade WHERE profissional_id = %s", (profissional_id,))
        for especialidade in especialidades:
            cur.execute(
                """
                INSERT INTO especialidades (nome, descricao)
                VALUES (%s, %s)
                ON CONFLICT (nome) DO UPDATE SET descricao = EXCLUDED.descricao
                RETURNING id
                """,
                (especialidade, ""),
            )
            especialidade_id = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO profissional_especialidade (profissional_id, especialidade_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (profissional_id, especialidade_id),
            )
        conn.commit()
        cur.close()
        conn.close()

    #Atualiza os dados do usuário com um id específico na tabela usuarios
    def atualizar(self, profissional):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET nome = %s, telefone = %s, email = %s, senha = COALESCE(NULLIF(%s, ''), senha) WHERE id = %s",
            (profissional.nome, profissional.telefone, profissional.email, profissional.senha, profissional.id),
        )
        cur.execute("DELETE FROM profissional_especialidade WHERE profissional_id = %s", (profissional.id,))
        for especialidade in profissional.especialidades:
            cur.execute(
                """
                INSERT INTO especialidades (nome, descricao)
                VALUES (%s, %s)
                ON CONFLICT (nome) DO UPDATE SET descricao = EXCLUDED.descricao
                RETURNING id
                """,
                (especialidade, ""),
            )
            especialidade_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO profissional_especialidade VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (profissional.id, especialidade_id),
            )
        conn.commit()
        cur.close()
        conn.close()

    #lista as especialidades da tabela especialidades, ordenadas por nome
    def listar_especialidades(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, descricao FROM especialidades ORDER BY nome")
        especialidades = [{"id": row[0], "nome": row[1], "descricao": row[2]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return especialidades
    
    #lista as especialidades da tabela profissional_especialidades linkadas com o profissional
    def listar_especialidades_do_profissional(self, profissional_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT e.id, e.nome, e.descricao
            FROM especialidades e
            JOIN profissional_especialidade pe ON pe.especialidade_id = e.id
            WHERE pe.profissional_id = %s
            ORDER BY e.nome
            """,
            (profissional_id,),
        )
        especialidades = [
            {"id": row[0], "nome": row[1], "descricao": row[2]}
            for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return especialidades
    
    #deleta a especialidade do profissional linkado na tabela de profissional_especialidade e cria uma nova especialidade na mesma tabela linkada a ele.
    def atualizar_especialidades(self, profissional_id, especialidades):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM profissional_especialidade WHERE profissional_id = %s", (profissional_id,))
        for especialidade in especialidades:
            cur.execute(
                """
                INSERT INTO especialidades (nome, descricao)
                VALUES (%s, %s)
                ON CONFLICT (nome) DO UPDATE SET descricao = EXCLUDED.descricao
                RETURNING id
                """,
                (especialidade, ""),
            )
            especialidade_id = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO profissional_especialidade (profissional_id, especialidade_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (profissional_id, especialidade_id),
            )
        conn.commit()
        cur.close()
        conn.close()

    #deleta o profissional da tablea de usuarios
    def excluir(self, profissional_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id = %s", (profissional_id,))
        conn.commit()
        cur.close()
        conn.close()
