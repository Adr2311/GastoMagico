# controllers/tabla_controller.py

from use_cases.tabla_use_case import TablaUseCase
from utils.console import console
from rich.table import Table


class TablaController:
    @staticmethod
    def agregar_categoria_interactivo() -> None:
        nombre = input("Nombre de la categoría: ")
        try:
            TablaUseCase.agregar_categoria(nombre)
            console.print("[green]Categoría agregada correctamente.[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    @staticmethod
    def listar_categorias_interactivo() -> None:
        categorias = TablaUseCase.listar_categorias()
        if not categorias:
            console.print("[yellow]No hay categorías registradas.[/yellow]")
            return

        table = Table(title="Listado de Categorías")
        table.add_column("ID", justify="right")
        table.add_column("Nombre")

        for categoria in categorias:
            table.add_row(str(categoria.id), categoria.nombre)

        console.print(table)

    @staticmethod
    def eliminar_categoria_interactivo() -> None:
        TablaController.listar_categorias_interactivo()
        id_categoria = input("Ingrese el ID de la categoría a eliminar: ")
        try:
            id_categoria = int(id_categoria)
            TablaUseCase.eliminar_categoria(id_categoria)
            console.print("[green]Categoría eliminada correctamente.[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    @staticmethod
    def agregar_metodo_pago_interactivo() -> None:
        nombre = input("Nombre del método de pago: ")
        try:
            TablaUseCase.agregar_metodo_pago(nombre)
            console.print("[green]Método de pago agregado correctamente.[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    @staticmethod
    def listar_metodos_pago_interactivo() -> None:
        metodos = TablaUseCase.listar_metodos_pago()
        if not metodos:
            console.print("[yellow]No hay métodos de pago registrados.[/yellow]")
            return

        table = Table(title="Listado de Métodos de Pago")
        table.add_column("ID", justify="right")
        table.add_column("Nombre")

        for metodo in metodos:
            table.add_row(str(metodo.id), metodo.nombre)

        console.print(table)

    @staticmethod
    def eliminar_metodo_pago_interactivo() -> None:
        TablaController.listar_metodos_pago_interactivo()
        id_metodo = input("Ingrese el ID del método de pago a eliminar: ")
        try:
            id_metodo = int(id_metodo)
            TablaUseCase.eliminar_metodo_pago(id_metodo)
            console.print("[green]Método de pago eliminado correctamente.[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    @staticmethod
    def agregar_frase_interactivo() -> None:
        texto = input("Texto de la frase: ")
        try:
            TablaUseCase.agregar_frase(texto)
            console.print("[green]Frase motivacional agregada correctamente.[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    @staticmethod
    def listar_frases_interactivo() -> None:
        frases = TablaUseCase.listar_frases()
        if not frases:
            console.print("[yellow]No hay frases motivacionales registradas.[/yellow]")
            return

        table = Table(title="Listado de Frases Motivacionales")
        table.add_column("ID", justify="right")
        table.add_column("Texto")

        for frase in frases:
            table.add_row(str(frase.id), frase.texto)

        console.print(table)
