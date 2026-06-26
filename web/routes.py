"""Rotas Flask do Conecta Obras Itacoatiara Web."""

import os
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from database.create_tables import create_tables
from services.auth_service import AuthService
from services.avaliacao_service import AvaliacaoService
from services.cliente_service import ClienteService
from services.portfolio_service import PortfolioService
from services.profissional_service import ProfissionalService
from services.servico_service import ServicoService


STATUS_LABELS = {
    "AGUARDANDO": "Aguardando",
    "EM_ANDAMENTO": "Em andamento",
    "CONCLUIDO": "Concluído",
    "CANCELADO": "Cancelado",
}

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Faça login para continuar.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapper


def cliente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))

        if session.get("tipo") != "cliente":
            if session.get("tipo") == "profissional":
                return redirect(url_for("profissional_home"))
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function


def profissional_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        tipo = str(session.get("tipo", "")).strip().lower()
        if tipo != "profissional":
            flash("Você foi redirecionado para sua área correta.")
            return redirect(url_for("cliente_home"))
        return f(*args, **kwargs)

    return wrapper


def create_app():
    app = Flask(__name__, template_folder="static/templates", static_folder="static")
    app.secret_key = os.getenv("SECRET_KEY", "conecta-obras-dev")
    app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder, "uploads")

    auth_service = AuthService()
    cliente_service = ClienteService()
    profissional_service = ProfissionalService()
    servico_service = ServicoService()
    avaliacao_service = AvaliacaoService()
    portfolio_service = PortfolioService()

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    @app.before_request
    def preparar_banco():
        if not getattr(app, "_db_ready", False):
            create_tables()
            app._db_ready = True

    @app.context_processor
    def contexto_global():
        return {"status_labels": STATUS_LABELS}

    def home_por_tipo():
        tipo = str(session.get("tipo", "")).strip().lower()
        if tipo == "cliente":
            return redirect(url_for("cliente_home"))
        if tipo == "profissional":
            return redirect(url_for("profissional_home"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            usuario = auth_service.autenticar(request.form["email"], request.form["senha"])
            if not usuario:
                flash("E-mail ou senha inválidos.")
                return redirect(url_for("login"))
            tipo = str(usuario["tipo"]).strip().lower()
            session.clear()
            session["usuario_id"] = usuario["id"]
            if tipo == "cliente":
                session["tipo"] = "cliente"
            elif tipo == "profissional":
                session["tipo"] = "profissional"
            else:
                flash("Tipo de usuário inválido.")
                return redirect(url_for("login"))
            session["nome"] = usuario["nome"]
            session["email"] = usuario["email"]
            return home_por_tipo()
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Você saiu do sistema.")
        return redirect(url_for("login"))

    @app.route("/cadastro")
    def escolha_perfil():
        return render_template("selecionar_tipo_conta.html")

    @app.route("/cadastro/cliente", methods=["GET", "POST"])
    def cadastro_cliente():
        if request.method == "POST":
            if request.form["senha"] != request.form["confirmar_senha"]:
                flash("As senhas não conferem.")
                return redirect(url_for("cadastro_cliente"))
            try:
                cliente_service.criar_cliente(
                    request.form["nome"],
                    request.form["telefone"],
                    request.form["email"],
                    request.form["senha"],
                )
                flash("Cadastro concluído. Faça login para entrar.")
                return redirect(url_for("login"))
            except Exception:
                flash("Não foi possível cadastrar. Verifique se o e-mail já existe.")
        return render_template("cadastro_cliente.html")

    @app.route("/cadastro/profissional", methods=["GET", "POST"])
    def cadastro_profissional():
        especialidades = profissional_service.listar_especialidades()
        if request.method == "POST":
            if request.form["senha"] != request.form["confirmar_senha"]:
                flash("As senhas não conferem.")
                return redirect(url_for("cadastro_profissional"))
            try:
                profissional_service.criar_profissional(
                    request.form["nome"],
                    request.form["telefone"],
                    request.form["email"],
                    request.form["senha"],
                    request.form.getlist("especialidades"),
                    "",
                )
                flash("Cadastro concluído. Faça login para entrar.")
                return redirect(url_for("login"))
            except Exception:
                flash("Não foi possível cadastrar. Verifique se o e-mail já existe.")
        return render_template("cadastro_profissional.html", especialidades=especialidades)

    @app.route("/cliente/home")
    @cliente_required
    def cliente_home():
        termo = request.args.get("busca", "").strip()
        profissionais = profissional_service.listar_profissionais_com_metricas(termo)
        especialidades = profissional_service.listar_especialidades()
        return render_template(
            "cliente_home.html",
            profissionais=profissionais,
            especialidades=especialidades,
            termo=termo,
        )

    @app.route("/cliente/profissionais")
    @cliente_required
    def cliente_profissionais():
        termo = request.args.get("busca", "").strip()
        profissionais = profissional_service.listar_profissionais_com_metricas(termo)
        return render_template("cliente_profissionais.html", profissionais=profissionais, termo=termo)

    @app.route("/cliente/profissional/<int:profissional_id>")
    @cliente_required
    def cliente_perfil_profissional(profissional_id):
        profissional = profissional_service.buscar_perfil_publico(profissional_id)
        if not profissional:
            flash("Profissional não encontrado.")
            return redirect(url_for("cliente_profissionais"))
        imagens = portfolio_service.listar_imagens_profissional(profissional_id)
        avaliacoes = avaliacao_service.listar_por_profissional(profissional_id)
        especialidades = profissional_service.listar_especialidades(profissional_id)
        return render_template(
            "cliente_perfil_profissional.html",
            profissional=profissional,
            imagens=imagens,
            avaliacoes=avaliacoes,
            especialidades=especialidades,
        )

    @app.route("/cliente/solicitar/<int:profissional_id>", methods=["GET", "POST"])
    @cliente_required
    def cliente_solicitar_servico(profissional_id):
        profissional = profissional_service.buscar_detalhes(profissional_id)
        if not profissional:
            flash("Profissional não encontrado.")
            return redirect(url_for("cliente_profissionais"))
        if request.method == "POST":
            servico_service.criar_servico(
                {
                    "cliente_id": session["usuario_id"],
                    "profissional_id": profissional_id,
                    "descricao": request.form["descricao"],
                    "data_prevista": request.form["data_prevista"],
                    "valor": request.form["valor"],
                    "rua": request.form["rua"],
                    "numero": request.form["numero"],
                    "bairro": request.form["bairro"],
                    "status": "AGUARDANDO",
                }
            )
            flash("Solicitação de serviço enviada.")
            return redirect(url_for("cliente_minhas_contratacoes"))
        return render_template("cliente_solicitar_servico.html", profissional=profissional)

    @app.route("/cliente/minhas-contratacoes")
    @cliente_required
    def cliente_minhas_contratacoes():
        cliente_id = session["usuario_id"]
        servicos = servico_service.listar_por_cliente(cliente_id)
        por_status = {status: [] for status in STATUS_LABELS}
        for servico in servicos:
            por_status.setdefault(servico["status"], []).append(servico)
        return render_template(
            "cliente_minhas_contratacoes.html",
            servicos=servicos,
            por_status=por_status,
        )

    @app.route("/cliente/avaliar/<int:servico_id>", methods=["GET", "POST"])
    @cliente_required
    def cliente_avaliar_servico(servico_id):
        servico = servico_service.buscar_servico(servico_id)
        if not servico or not servico_service.servico_pertence_ao_cliente(servico_id, session["usuario_id"]):
            flash("Serviço não encontrado.")
            return redirect(url_for("cliente_minhas_contratacoes"))
        if servico["status"] != "CONCLUIDO":
            flash("Somente serviços concluídos podem ser avaliados.")
            return redirect(url_for("cliente_minhas_contratacoes"))
        if avaliacao_service.existe_por_servico(servico_id):
            flash("Este serviço já foi avaliado.")
            return redirect(url_for("cliente_minhas_contratacoes"))
        if request.method == "POST":
            try:
                avaliacao_service.criar_avaliacao(
                    {
                        "nota": request.form["nota"],
                        "comentario": request.form["comentario"],
                        "servico_id": servico_id,
                        "cliente_id": session["usuario_id"],
                        "profissional_id": servico["profissional_id"],
                    }
                )
                flash("Avaliação publicada com sucesso.")
                return redirect(url_for("cliente_minhas_contratacoes"))
            except ValueError as erro:
                flash(str(erro))
        return render_template("cliente_avaliar_servico.html", servico=servico)

    @app.route("/profissional/home")
    @profissional_required
    def profissional_home():
        profissional = profissional_service.buscar_detalhes(session["usuario_id"])
        servicos = servico_service.listar_por_profissional(session["usuario_id"])
        pedidos = [servico for servico in servicos if servico["status"] == "AGUARDANDO"]
        ativos = [servico for servico in servicos if servico["status"] == "EM_ANDAMENTO"]
        return render_template(
            "profissional_home.html",
            profissional=profissional,
            pedidos=pedidos,
            ativos=ativos,
        )

    def alterar_status_do_profissional(servico_id, status_atual, novo_status):
        servico = servico_service.buscar_servico(servico_id)
        if not servico or servico["profissional_id"] != session["usuario_id"]:
            flash("Serviço não encontrado para este profissional.")
            return redirect(url_for("profissional_home"))
        if servico["status"] != status_atual:
            flash("Este serviço não está em um status válido para esta ação.")
            return redirect(url_for("profissional_home"))
        servico_service.alterar_status(servico_id, novo_status)
        flash("Status do serviço atualizado.")
        return redirect(url_for("profissional_home"))

    @app.route("/profissional/servico/<int:servico_id>/aceitar", methods=["POST"])
    @profissional_required
    def profissional_aceitar_servico(servico_id):
        return alterar_status_do_profissional(servico_id, "AGUARDANDO", "EM_ANDAMENTO")

    @app.route("/profissional/servico/<int:servico_id>/recusar", methods=["POST"])
    @profissional_required
    def profissional_recusar_servico(servico_id):
        return alterar_status_do_profissional(servico_id, "AGUARDANDO", "CANCELADO")

    @app.route("/profissional/servico/<int:servico_id>/concluir", methods=["POST"])
    @profissional_required
    def profissional_concluir_servico(servico_id):
        return alterar_status_do_profissional(servico_id, "EM_ANDAMENTO", "CONCLUIDO")

    @app.route("/profissional/portfolio", methods=["GET", "POST"])
    @profissional_required
    def profissional_portfolio():
        print("SESSION:", dict(session))
        print("ACESSANDO PORTFOLIO PROFISSIONAL")
        profissional_id = session["usuario_id"]
        if request.method == "POST":
            imagem = request.files.get("imagem")
            descricao = request.form.get("descricao", "").strip()
            if not imagem or not imagem.filename:
                flash("Envie uma imagem para adicionar ao portfólio.")
                return redirect(url_for("profissional_portfolio"))
            if not allowed_file(imagem.filename):
                flash("Envie uma imagem PNG, JPG, JPEG ou WEBP.")
                return redirect(url_for("profissional_portfolio"))
            nome_seguro = secure_filename(imagem.filename)
            nome_arquivo = f"profissional_{profissional_id}_{nome_seguro}"
            imagem.save(os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo))
            portfolio_service.adicionar_imagem(profissional_id, nome_arquivo, descricao)
            flash("Imagem adicionada ao portfólio.")
            return redirect(url_for("profissional_portfolio"))

        profissional = profissional_service.buscar_detalhes(profissional_id)
        imagens = portfolio_service.listar_imagens(profissional_id)
        avaliacoes = avaliacao_service.listar_por_profissional(profissional_id)
        return render_template(
            "profissional_portfolio.html",
            profissional=profissional,
            imagens=imagens,
            avaliacoes=avaliacoes,
        )

    @app.route("/profissional/portfolio/<int:imagem_id>/excluir", methods=["POST"])
    @profissional_required
    def profissional_excluir_imagem_portfolio(imagem_id):
        imagem = portfolio_service.buscar_imagem_do_profissional(imagem_id, session["usuario_id"])
        if not imagem:
            flash("Imagem não encontrada.")
            return redirect(url_for("profissional_portfolio"))
        portfolio_service.excluir_imagem(imagem_id, session["usuario_id"])
        caminho = os.path.join(app.config["UPLOAD_FOLDER"], imagem["caminho_pasta"])
        if os.path.exists(caminho):
            os.remove(caminho)
        flash("Imagem removida do portfólio.")
        return redirect(url_for("profissional_portfolio"))

    @app.route("/profissional/perfil", methods=["GET", "POST"])
    @profissional_required
    def profissional_perfil():
        profissional = profissional_service.buscar_profissional(session["usuario_id"])
        especialidades = profissional_service.listar_especialidades()
        if request.method == "POST":
            try:
                profissional_service.atualizar_perfil_e_especialidades(
                    session["usuario_id"],
                    request.form["telefone"],
                    request.form["email"],
                    request.form.getlist("especialidades"),
                )
                session["email"] = request.form["email"]
                flash("Perfil e especialidades atualizados.")
                return redirect(url_for("profissional_perfil"))
            except Exception:
                flash("Não foi possível salvar. Verifique se o e-mail já está em uso.")
        return render_template(
            "profissional_perfil_especialidades.html",
            profissional=profissional,
            especialidades=especialidades,
        )

    return app
