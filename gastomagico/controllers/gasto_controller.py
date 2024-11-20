# controllers/gasto_controller.py

from use_cases.gasto_use_case import GastoUseCase
from use_cases.tabla_use_case import TablaUseCase
from utils.console import console
from rich.table import Table


class GastoController:
    @staticmethod
    def agregar_gasto_interactivo() -> None:
        descripcion = input("Descripción del gasto: ")
        monto_str = input("Monto: ")
        try:
            monto = float(monto_str)
        except ValueError:
            console.print("[red]Monto inválido[/red]")
            return

        # Seleccionar categoría
        categorias = TablaUseCase.listar_categorias()
        if not categorias:
            console.print("[yellow]No hay categorías disponibles. Por favor, agregue una primero.[/yellow]")
            return
        table = Table(title="Seleccione una Categoría")
        table.add_column("ID", justify="right")
        table.add_column("Nombre")
        for categoria in categorias:
            table.add_row(str(categoria.id), categoria.nombre)
        console.print(table)
        categoria_id = input("Ingrese el ID de la categoría: ")
        try:
            categoria_id = int(categoria_id)
        except ValueError:
            console.print("[red]ID inválido[/red]")
            return

        # Seleccionar método de pago
        metodos_pago = TablaUseCase.listar_metodos_pago()
        if not metodos_pago:
            console.print("[yellow]No hay métodos de pago disponibles. Por favor, agregue uno primero.[/yellow]")
            return
        table = Table(title="Seleccione un Método de Pago")
        table.add_column("ID", justify="right")
        table.add_column("Nombre")
        for metodo in metodos_pago:
            table.add_row(str(metodo.id), metodo.nombre)
        console.print(table)
        metodo_pago_id = input("Ingrese el ID del método de pago: ")
        try:
            metodo_pago_id = int(metodo_pago_id)
        except ValueError:
            console.print("[red]ID inválido[/red]")
            return

        try:
            GastoUseCase.agregar_gasto(descripcion, monto, categoria_id, metodo_pago_id)
            console.print(":money_with_wings: [green]Gasto agregado correctamente[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    @staticmethod
    def listar_gastos_interactivo() -> None:
        gastos = GastoUseCase.listar_gastos()
        if not gastos:
            console.print("[yellow]No hay gastos registrados.[/yellow]")
            return

        table = Table(title="Listado de Gastos")
        table.add_column("ID", justify="right")
        table.add_column("Descripción")
        table.add_column("Monto", justify="right")
        table.add_column("Categoría")
        table.add_column("Método de Pago")
        table.add_column("Fecha de Creación")

        for gasto in gastos:
            table.add_row(
                str(gasto.id),
                gasto.descripcion,
                f"${gasto.monto:.2f}",
                gasto.categoria.nombre if gasto.categoria else "N/A",
                gasto.metodo_pago.nombre if gasto.metodo_pago else "N/A",
                gasto.created_at.strftime("%Y-%m-%d %H:%M:%S") if gasto.created_at else "N/A"
            )
        console.print(table)

    @staticmethod
    def eliminar_gasto_interactivo() -> None:
        GastoController.listar_gastos_interactivo()
        id_gasto = input("Ingrese el ID del gasto a eliminar: ")
        try:
            id_gasto = int(id_gasto)
            GastoUseCase.eliminar_gasto(id_gasto)
            console.print("[green]Gasto eliminado correctamente.[/green]")
        except ValueError:
            console.print("[red]ID inválido o Gasto no encontrado.[/red]")
