# controllers/reporte_controller.py

from use_cases.reporte_use_case import ReporteUseCase
from utils.console import console
from rich.table import Table


class ReporteController:
    @staticmethod
    def exportar_reporte_excel_interactivo() -> None:
        filepath = input("Ingrese la ruta para guardar el reporte Excel (ejemplo: reporte.xlsx): ")
        try:
            ReporteUseCase.generar_reporte_excel(filepath)
            console.print(f"[green]Reporte exportado exitosamente a {filepath}.[/green]")
        except Exception as e:
            console.print(f"[red]Error al exportar el reporte: {e}[/red]")

    @staticmethod
    def importar_reporte_excel_interactivo() -> None:
        filepath = input("Ingrese la ruta del archivo Excel a importar (ejemplo: reporte.xlsx): ")
        try:
            ReporteUseCase.importar_reporte_excel(filepath)
            console.print(f"[green]Reporte importado exitosamente desde {filepath}.[/green]")
        except Exception as e:
            console.print(f"[red]Error al importar el reporte: {e}[/red]")

    @staticmethod
    def mostrar_gastos_mensuales_interactivo() -> None:
        resumen = ReporteUseCase.gastos_mensuales()
        if not resumen:
            console.print("[yellow]No hay gastos registrados para mostrar.[/yellow]")
            return
        table = Table(title="Gastos Mensuales")
        table.add_column("Mes")
        table.add_column("Monto Total", justify="right")
        for mes, monto in sorted(resumen.items()):
            table.add_row(mes, f"${monto:.2f}")
        console.print(table)

    @staticmethod
    def mostrar_dia_menor_gasto_interactivo() -> None:
        dia = ReporteUseCase.dia_menor_gasto()
        if not dia:
            console.print("[yellow]No hay datos suficientes para determinar el día con menor gasto.[/yellow]")
            return
        console.print(f"[green]El día con menor gasto es: {dia}[/green]")

    @staticmethod
    def establecer_limite_gasto_interactivo() -> None:
        limite_str = input("Ingrese el límite de gasto: ")
        try:
            limite = float(limite_str)
            ReporteUseCase.establecer_limite_gasto(limite)
            console.print("[green]Límite de gasto establecido correctamente.[/green]")
        except ValueError:
            console.print("[red]Valor inválido para el límite de gasto.[/red]")

    @staticmethod
    def menu_reportes_personalizados_interactivo() -> None:
        while True:
            console.print("\n[bold cyan]Reportes Financieros Personalizados[/bold cyan]")
            console.print("1. Gastos Mensuales")
            console.print("2. Día con Menor Gasto")
            console.print("3. Establecer Límite de Gastos")
            console.print("4. Regresar al Menú de Reportes")
            opcion = input("Selecciona una opción: ")
            if opcion == '1':
                ReporteController.mostrar_gastos_mensuales_interactivo()
            elif opcion == '2':
                ReporteController.mostrar_dia_menor_gasto_interactivo()
            elif opcion == '3':
                ReporteController.establecer_limite_gasto_interactivo()
            elif opcion == '4':
                break
            else:
                console.print("[red]Opción inválida[/red]")

    @staticmethod
    def menu_reportes_interactivo() -> None:
        while True:
            console.print("\n[bold cyan]Generación de Reportes[/bold cyan]")
            console.print("1. Exportar Reporte a Excel")
            console.print("2. Importar Reporte desde Excel")
            console.print("3. Reportes Financieros Personalizados")
            console.print("4. Regresar al Menú Principal")
            opcion = input("Selecciona una opción: ")
            if opcion == '1':
                ReporteController.exportar_reporte_excel_interactivo()
            elif opcion == '2':
                ReporteController.importar_reporte_excel_interactivo()
            elif opcion == '3':
                ReporteController.menu_reportes_personalizados_interactivo()
            elif opcion == '4':
                break
            else:
                console.print("[red]Opción inválida[/red]")
