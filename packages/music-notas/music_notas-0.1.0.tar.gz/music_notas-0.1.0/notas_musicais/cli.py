from rich import print
from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

from notas_musicais.acordes import acorde as _acorde
from notas_musicais.campo_harmonico import campo_harmonico as _campo_harmonico
from notas_musicais.escala import escala as _escala

console = Console()
app = Typer()


@app.command()
def escala(
    tonica: str = Argument('c', help='Tônica da escala'),
    tonalidade: str = Argument('maior', help='Tonalidade da escala'),
):
    table = Table()
    notas, graus = _escala(tonica, tonalidade).values()

    for grau in graus:
        table.add_column(grau)
    table.add_row(*notas)
    console.print(table)


@app.command()
def acorde(
    cifra: str = Argument('c', help='Cifra desejada'),
):
    table = Table()
    notas, graus = _acorde(cifra).values()

    for grau in graus:
        table.add_column(grau)
    table.add_row(*notas)
    console.print(table)


@app.command()
def campo_harmonico(
    tonica: str = Argument('c', help='Tônica do campo harmônico'),
    tonalidade: str = Argument('maior', help='Tonalidade do csmpo hsrmônico'),
):
    table = Table()
    acordes, graus = _campo_harmonico(tonica, tonalidade).values()

    for grau in graus:
        table.add_column(grau)
    table.add_row(*acordes)
    console.print(table)
