"""Ponto de entrada da aplicação Flask Conecta Obras Itacoatiara Web."""

from database.create_tables import create_tables
from web.routes import create_app


app = create_app()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
