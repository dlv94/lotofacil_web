from io import BytesIO
import json
import os
from pathlib import Path
from tempfile import mkstemp
from typing import Any

from flask import Flask, flash, redirect, render_template, request, send_file, url_for

from excel_exporter import ExcelExporter
from game_config import GameConfig
from game_generator import GameGenerator
from generated_game import GeneratedGame
from quadrant_set import QuadrantSet
from validator import GameValidator


app = Flask(__name__)
app.config["SECRET_KEY"] = "troque-esta-chave-no-pythonanywhere"

validator = GameValidator()
generator = GameGenerator()
exporter = ExcelExporter()


def parse_fixed_numbers(value: str) -> list[int]:
    """Converte números separados por vírgula ou ponto e vírgula."""
    if not value.strip():
        return []

    numbers: list[int] = []
    for item in value.replace(";", ",").split(","):
        item = item.strip()
        if not item:
            continue
        try:
            numbers.append(int(item))
        except ValueError as error:
            raise ValueError(f"'{item}' não é um número válido.") from error
    return numbers


def parse_configuration() -> GameConfig:
    """Lê os campos do formulário e cria o objeto de configuração."""
    fixed_numbers = parse_fixed_numbers(request.form.get("fixed_numbers", ""))
    raw_set_ids = request.form.getlist("set_id")
    if not raw_set_ids:
        raise ValueError("Adicione pelo menos um conjunto de quadrantes.")

    quadrant_sets: list[QuadrantSet] = []
    for index, raw_set_id in enumerate(raw_set_ids):
        try:
            set_id = int(raw_set_id)
            number_of_games = int(request.form.get(f"number_of_games_{index}", ""))
            distribution = {
                quadrant: int(request.form.get(f"q{quadrant}_{index}", ""))
                for quadrant in range(1, 6)
            }
        except ValueError as error:
            raise ValueError(
                f"Preencha apenas números inteiros no conjunto {index + 1}."
            ) from error

        quadrant_sets.append(
            QuadrantSet(
                set_id=set_id,
                number_of_games=number_of_games,
                quadrant_distribution=distribution,
            )
        )

    return GameConfig(fixed_numbers=fixed_numbers, quadrant_sets=quadrant_sets)


def games_as_dict(games: list[Any]) -> list[dict[str, Any]]:
    return [
        {
            "identifier": exporter._get_game_identifier(game),
            "set_id": game.set_id,
            "game_number": game.game_number,
            "quadrant_distribution": game.quadrant_distribution,
            "numbers": game.numbers,
        }
        for game in games
    ]


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/validate")
def validate_configuration():
    try:
        config = parse_configuration()
        validator.validate(config)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("index"))

    flash("Configuração válida. Você já pode gerar os jogos.", "success")
    return redirect(url_for("index"))


@app.post("/generate")
def generate_games():
    try:
        config = parse_configuration()
        validator.validate(config)
        games = generator.generate(config)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("index"))
    except Exception:
        app.logger.exception("Erro inesperado ao gerar jogos")
        flash("Não foi possível gerar os jogos. Tente novamente.", "error")
        return redirect(url_for("index"))

    return render_template(
        "results.html",
        games=games_as_dict(games),
        total=len(games),
        config=config,
    )


def parse_presented_games() -> list[GeneratedGame]:
    """Reconstrói os jogos exibidos para exportá-los sem regenerar."""
    raw_games = request.form.get("games_json", "")
    if not raw_games:
        raise ValueError("Os jogos apresentados não foram encontrados.")

    try:
        data = json.loads(raw_games)
    except json.JSONDecodeError as error:
        raise ValueError("Não foi possível ler os jogos apresentados.") from error

    if not isinstance(data, list) or not data:
        raise ValueError("Não existem jogos apresentados para exportar.")

    games: list[GeneratedGame] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Formato inválido dos jogos apresentados.")
        try:
            game = GeneratedGame(
                set_id=int(item["set_id"]),
                game_number=int(item["game_number"]),
                quadrant_distribution=[
                    int(quantity) for quantity in item["quadrant_distribution"]
                ],
                numbers=[int(number) for number in item["numbers"]],
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Formato inválido dos jogos apresentados.") from error

        if len(game.numbers) != 15 or len(set(game.numbers)) != 15:
            raise ValueError("Um dos jogos apresentados não possui 15 números únicos.")
        if any(number < 1 or number > 25 for number in game.numbers):
            raise ValueError("Um dos jogos apresentados possui números inválidos.")
        games.append(game)

    return games


@app.post("/download")
def download_games():
    temporary_path = None
    try:
        # O download utiliza exatamente os jogos enviados pela tela de resultados.
        games = parse_presented_games()
        output = BytesIO()
        file_descriptor, temporary_path = mkstemp(suffix=".xlsx")
        # No Windows, o descritor precisa ser fechado antes que o openpyxl
        # tente reabrir o mesmo caminho para gravar o arquivo ZIP do XLSX.
        os.close(file_descriptor)
        Path(temporary_path).unlink(missing_ok=True)
        exporter.export(games, temporary_path)
        with open(temporary_path, "rb") as file:
            output.write(file.read())
        output.seek(0)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("index"))
    except Exception:
        app.logger.exception("Erro inesperado ao exportar jogos")
        flash("Não foi possível gerar a planilha. Tente novamente.", "error")
        return redirect(url_for("index"))
    finally:
        if temporary_path:
            Path(temporary_path).unlink(missing_ok=True)

    return send_file(
        output,
        as_attachment=True,
        download_name="jogos_lotofacil.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    app.run(debug=True)


# O PythonAnywhere procura por este nome no arquivo WSGI.
application = app
