# main.py

import sys
import click
from controllers.gasto_controller import GastoController
from controllers.tabla_controller import TablaController
from controllers.reporte_controller import ReporteController
from utils.console import console, mostrar_frase_motivacional
from utils.database import init_db

@click.group()
def cli():
    """GastoMágico: Una herramienta de gestión de gastos."""
    init_db()
    console.print("[bold cyan]¡Bienvenido a GastoMágico![/bold cyan]")
    mostrar_frase_motivacional()

@cli.group()
def gastos():
    """Gestión de gastos."""
    pass

@gastos.command()
def agregar():
    """Agregar un nuevo gasto."""
    GastoController.agregar_gasto_interactivo()

@gastos.command()
def listar():
    """Listar todos los gastos."""
    GastoController.listar_gastos_interactivo()

@gastos.command()
@click.argument('id_gasto', type=int)
def eliminar(id_gasto):
    """Eliminar un gasto por ID."""
    try:
        GastoUseCase = __import__('use_cases.gasto_use_case', fromlist=['GastoUseCase']).GastoUseCase
        GastoUseCase.eliminar_gasto(id_gasto)
        console.print("[green]Gasto eliminado correctamente.[/green]")
    except ValueError as e:
        console.print(f"[red]{e}[/red]")

@cli.group()
def tablas():
    """Gestión de tablas (categorías, métodos de pago, frases)."""
    pass

@tablas.command()
def agregar_categoria():
    """Agregar una nueva categoría."""
    TablaController.agregar_categoria_interactivo()

@tablas.command()
def listar_categorias():
    """Listar todas las categorías."""
    TablaController.listar_categorias_interactivo()

@tablas.command()
@click.argument('id_categoria', type=int)
def eliminar_categoria(id_categoria):
    """Eliminar una categoría por ID."""
    try:
        TablaUseCase = __import__('use_cases.tabla_use_case', fromlist=['TablaUseCase']).TablaUseCase
        TablaUseCase.eliminar_categoria(id_categoria)
        console.print("[green]Categoría eliminada correctamente.[/green]")
    except ValueError as e:
        console.print(f"[red]{e}[/red]")

@tablas.command()
def agregar_metodo_pago():
    """Agregar un nuevo método de pago."""
    TablaController.agregar_metodo_pago_interactivo()

@tablas.command()
def listar_metodos_pago():
    """Listar todos los métodos de pago."""
    TablaController.listar_metodos_pago_interactivo()

@tablas.command()
@click.argument('id_metodo', type=int)
def eliminar_metodo_pago(id_metodo):
    """Eliminar un método de pago por ID."""
    try:
        TablaUseCase = __import__('use_cases.tabla_use_case', fromlist=['TablaUseCase']).TablaUseCase
        TablaUseCase.eliminar_metodo_pago(id_metodo)
        console.print("[green]Método de pago eliminado correctamente.[/green]")
    except ValueError as e:
        console.print(f"[red]{e}[/red]")

@tablas.command()
def agregar_frase():
    """Agregar una nueva frase motivacional."""
    TablaController.agregar_frase_interactivo()

@tablas.command()
def listar_frases():
    """Listar todas las frases motivacionales."""
    TablaController.listar_frases_interactivo()

@cli.group()
def reportes():
    """Generación y gestión de reportes."""
    pass

@reportes.command()
def exportar():
    """Exportar reporte a Excel."""
    ReporteController.exportar_reporte_excel_interactivo()

@reportes.command()
def importar():
    """Importar reporte desde Excel."""
    ReporteController.importar_reporte_excel_interactivo()

@reportes.command()
def personalizados():
    """Generar reportes financieros personalizados."""
    ReporteController.menu_reportes_personalizados_interactivo()

@cli.command()
def menu():
    """Iniciar el menú interactivo."""
    menu_interactivo()

def menu_interactivo():
    while True:
        console.print("\n[bold cyan]Menú Principal[/bold cyan]")
        console.print("1. Gestión de Gastos")
        console.print("2. Gestión de Tablas")
        console.print("3. Generación de Reportes")
        console.print("4. Salir")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            menu_gestion_gastos()
        elif opcion == '2':
            menu_gestion_tablas()
        elif opcion == '3':
            ReporteController.menu_reportes_interactivo()
        elif opcion == '4':
            console.print("[bold green]¡Hasta luego![/bold green]")
            break
        else:
            console.print("[red]Opción inválida[/red]")

def menu_gestion_gastos():
    while True:
        console.print("\n[bold cyan]Gestión de Gastos[/bold cyan]")
        console.print("1. Agregar Gasto")
        console.print("2. Listar Gastos")
        console.print("3. Eliminar Gasto")
        console.print("4. Regresar al Menú Principal")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            GastoController.agregar_gasto_interactivo()
        elif opcion == '2':
            GastoController.listar_gastos_interactivo()
        elif opcion == '3':
            id_gasto = input("Ingrese el ID del gasto a eliminar: ")
            try:
                id_gasto = int(id_gasto)
                from use_cases.gasto_use_case import GastoUseCase
                GastoUseCase.eliminar_gasto(id_gasto)
                console.print("[green]Gasto eliminado correctamente.[/green]")
            except ValueError:
                console.print("[red]ID inválido o Gasto no encontrado.[/red]")
        elif opcion == '4':
            break
        else:
            console.print("[red]Opción inválida[/red]")

def menu_gestion_tablas():
    while True:
        console.print("\n[bold cyan]Gestión de Tablas[/bold cyan]")
        console.print("1. Agregar Categoría")
        console.print("2. Listar Categorías")
        console.print("3. Eliminar Categoría")
        console.print("4. Agregar Método de Pago")
        console.print("5. Listar Métodos de Pago")
        console.print("6. Eliminar Método de Pago")
        console.print("7. Agregar Frase Motivacional")
        console.print("8. Listar Frases Motivacionales")
        console.print("9. Regresar al Menú Principal")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            TablaController.agregar_categoria_interactivo()
        elif opcion == '2':
            TablaController.listar_categorias_interactivo()
        elif opcion == '3':
            TablaController.eliminar_categoria_interactivo()
        elif opcion == '4':
            TablaController.agregar_metodo_pago_interactivo()
        elif opcion == '5':
            TablaController.listar_metodos_pago_interactivo()
        elif opcion == '6':
            TablaController.eliminar_metodo_pago_interactivo()
        elif opcion == '7':
            TablaController.agregar_frase_interactivo()
        elif opcion == '8':
            TablaController.listar_frases_interactivo()
        elif opcion == '9':
            break
        else:
            console.print("[red]Opción inválida[/red]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli()
    else:
        init_db()
        menu_interactivo()
