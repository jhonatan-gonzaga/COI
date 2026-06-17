# Conecta Obras Itacoatiara Web

Sistema web em Python com Flask para conectar clientes e profissionais autônomos da construção civil em Itacoatiara.

## Tecnologias

- Python
- Flask
- PostgreSQL
- psycopg2
- HTML5, CSS3 e Jinja2
- Werkzeug `secure_filename` para upload seguro de imagens

## Organização

- `main.py`: inicializa a aplicação.
- `models/`: classes de domínio com POO.
- `repositories/`: acesso ao banco com SQL e `psycopg2`.
- `services/`: regras de negócio.
- `database/connection.py`: conexão PostgreSQL.
- `database/create_tables.py`: criação automática do banco e tabelas.
- `web/routes.py`: rotas públicas, do cliente e do profissional.
- `web/templates/`: telas HTML.
- `web/static/css/style.css`: CSS próprio.
- `web/static/uploads/`: imagens do portfólio.

## Banco PostgreSQL

Banco padrão:

```text
conecta_obras
```

Variáveis aceitas em `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=conecta_obras
DB_ADMIN_DB=postgres
DB_USER=postgres
DB_PASSWORD=postgres
```

## Instalação

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Criar tabelas

```bash
python database/create_tables.py
```

## Rodar

```bash
python main.py
```

Acesse:

```text
http://127.0.0.1:5000/login
```

## Fluxo de uso

Cliente:

```text
Login -> Home Cliente -> Buscar Profissionais -> Ver Perfil Público -> Solicitar Serviço -> Minhas Contratações -> Avaliar Serviço Concluído
```

Profissional:

```text
Login -> Home Profissional -> Aceitar/Recusar Pedido -> Concluir Serviço -> Portfólio -> Upload/Exclusão de Imagens -> Perfil e Especialidades
```

## Rotas principais

Públicas:

- `/login`
- `/logout`
- `/cadastro`
- `/cadastro/cliente`
- `/cadastro/profissional`

Cliente:

- `/cliente/home`
- `/cliente/profissionais`
- `/cliente/profissional/<id>`
- `/cliente/solicitar/<id>`
- `/cliente/minhas-contratacoes`
- `/cliente/avaliar/<id>`

Profissional:

- `/profissional/home`
- `/profissional/portfolio`
- `/profissional/portfolio/<id>/excluir`
- `/profissional/perfil`
- `/profissional/servico/<id>/aceitar`
- `/profissional/servico/<id>/recusar`
- `/profissional/servico/<id>/concluir`
