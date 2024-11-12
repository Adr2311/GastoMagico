from database import session
from models import Gasto, Categoria, MetodoPago, Frase
from utils import console, mostrar_frase_motivacional
from rich.table import Table
from typing import List, Optional

def menu_gestion_gastos() -> None:
    """
    Menú para la gestión de gastos.
    """
    while True:
        console.print("\n[bold cyan]Gestión de Gastos[/bold cyan]")
        console.print("1. Agregar Gasto")
        console.print("2. Listar Gastos")
        console.print("3. Regresar al Menú Principal")
        opcion: str = input("Selecciona una opción: ")
        if opcion == '1':
            agregar_gasto()
        elif opcion == '2':
            listar_gastos()
        elif opcion == '3':
            break
        else:
            console.print("[red]Opción inválida[/red]")

def menu_gestion_tablas() -> None:
    """
    Menú para la gestión de tablas (categorías, métodos de pago y frases).
    """
    while True:
        console.print("\n[bold cyan]Gestión de Tablas[/bold cyan]")
        console.print("1. Agregar Categoría")
        console.print("2. Agregar Método de Pago")
        console.print("3. Agregar Frase Motivacional")
        console.print("4. Listar Categorías")
        console.print("5. Listar Métodos de Pago")
        console.print("6. Listar Frases Motivacionales")
        console.print("7. Regresar al Menú Principal")
        opcion: str = input("Selecciona una opción: ")
        if opcion == '1':
            agregar_categoria()
        elif opcion == '2':
            agregar_metodo_pago()
        elif opcion == '3':
            agregar_frase()
        elif opcion == '4':
            listar_categorias()
        elif opcion == '5':
            listar_metodos_pago()
        elif opcion == '6':
            listar_frases()
        elif opcion == '7':
            break
        else:
            console.print("[red]Opción inválida[/red]")

def agregar_gasto() -> None:
    """
    Función para agregar un nuevo gasto a la base de datos.
    """
    descripcion: str = input("Descripción del gasto: ")
    monto_str: str = input("Monto: ")
    try:
        monto: float = float(monto_str)
    except ValueError:
        console.print("[red]Monto inválido[/red]")
        return

    # Listar categorías y seleccionar una
    categoria = seleccionar_categoria()
    if not categoria:
        return

    # Listar métodos de pago y seleccionar uno
    metodo_pago = seleccionar_metodo_pago()
    if not metodo_pago:
        return

    # Crear el gasto
    gasto = Gasto(
        descripcion=descripcion,
        monto=monto,
        categoria_id=categoria.id,
        metodo_pago_id=metodo_pago.id
    )

    session.add(gasto)
    session.commit()
    console.print(":money_with_wings: [green]Gasto agregado correctamente[/green]")
    mostrar_frase_motivacional(session)

def seleccionar_categoria() -> Optional[Categoria]:
    """
    Función para listar categorías y permitir al usuario seleccionar una.
    """
    categorias: List[Categoria] = session.query(Categoria).all()
    if not categorias:
        console.print("[yellow]No hay categorías disponibles. Por favor, agregue una en la Gestión de Tablas.[/yellow]")
        return None

    table = Table(title="Seleccione una Categoría")
    table.add_column("ID", justify="right")
    table.add_column("Nombre")

    for categoria in categorias:
        table.add_row(str(categoria.id), categoria.nombre)

    console.print(table)
    id_categoria = input("Ingrese el ID de la categoría: ")

    try:
        id_categoria = int(id_categoria)
    except ValueError:
        console.print("[red]ID inválido[/red]")
        return None

    categoria = session.query(Categoria).filter_by(id=id_categoria).first()
    if not categoria:
        console.print("[red]Categoría no encontrada[/red]")
        return None

    return categoria

def seleccionar_metodo_pago() -> Optional[MetodoPago]:
    """
    Función para listar métodos de pago y permitir al usuario seleccionar uno.
    """
    metodos: List[MetodoPago] = session.query(MetodoPago).all()
    if not metodos:
        console.print("[yellow]No hay métodos de pago disponibles. Por favor, agregue uno en la Gestión de Tablas.[/yellow]")
        return None

    table = Table(title="Seleccione un Método de Pago")
    table.add_column("ID", justify="right")
    table.add_column("Nombre")

    for metodo in metodos:
        table.add_row(str(metodo.id), metodo.nombre)

    console.print(table)
    id_metodo = input("Ingrese el ID del método de pago: ")

    try:
        id_metodo = int(id_metodo)
    except ValueError:
        console.print("[red]ID inválido[/red]")
        return None

    metodo_pago = session.query(MetodoPago).filter_by(id=id_metodo).first()
    if not metodo_pago:
        console.print("[red]Método de pago no encontrado[/red]")
        return None

    return metodo_pago

def listar_gastos() -> None:
    """
    Función para listar todos los gastos registrados.
    """
    gastos: List[Gasto] = session.query(Gasto).all()
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
            f"\${gasto.monto:.2f}",
            gasto.categoria.nombre if gasto.categoria else "N/A",
            gasto.metodo_pago.nombre if gasto.metodo_pago else "N/A",
            gasto.created_at.strftime("%Y-%m-%d %H:%M:%S") if gasto.created_at else "N/A"
        )

    console.print(table)

def agregar_categoria() -> None:
    """
    Función para agregar una nueva categoría.
    """
    nombre: str = input("Nombre de la categoría: ")
    if session.query(Categoria).filter_by(nombre=nombre).first():
        console.print("[red]La categoría ya existe.[/red]")
    else:
        categoria = Categoria(nombre=nombre)
        session.add(categoria)
        session.commit()
        console.print("[green]Categoría agregada correctamente.[/green]")
        mostrar_frase_motivacional(session)

def listar_categorias() -> None:
    """
    Función para listar todas las categorías.
    """
    categorias: List[Categoria] = session.query(Categoria).all()
    if not categorias:
        console.print("[yellow]No hay categorías registradas.[/yellow]")
        return

    table = Table(title="Listado de Categorías")
    table.add_column("ID", justify="right")
    table.add_column("Nombre")

    for categoria in categorias:
        table.add_row(str(categoria.id), categoria.nombre)

    console.print(table)

def agregar_metodo_pago() -> None:
    """
    Función para agregar un nuevo método de pago.
    """
    nombre: str = input("Nombre del método de pago: ")
    if session.query(MetodoPago).filter_by(nombre=nombre).first():
        console.print("[red]El método de pago ya existe.[/red]")
    else:
        metodo_pago = MetodoPago(nombre=nombre)
        session.add(metodo_pago)
        session.commit()
        console.print("[green]Método de pago agregado correctamente.[/green]")
        mostrar_frase_motivacional(session)

def listar_metodos_pago() -> None:
    """
    Función para listar todos los métodos de pago.
    """
    metodos: List[MetodoPago] = session.query(MetodoPago).all()
    if not metodos:
        console.print("[yellow]No hay métodos de pago registrados.[/yellow]")
        return

    table = Table(title="Listado de Métodos de Pago")
    table.add_column("ID", justify="right")
    table.add_column("Nombre")

    for metodo in metodos:
        table.add_row(str(metodo.id), metodo.nombre)

    console.print(table)

def agregar_frase() -> None:
    """
    Función para agregar una nueva frase motivacional.
    """
    texto: str = input("Texto de la frase: ")
    frase = Frase(texto=texto)
    session.add(frase)
    session.commit()
    console.print("[green]Frase motivacional agregada correctamente.[/green]")

def listar_frases() -> None:
    """
    Función para listar todas las frases motivacionales.
    """
    frases: List[Frase] = session.query(Frase).all()
    if not frases:
        console.print("[yellow]No hay frases motivacionales registradas.[/yellow]")
        return

    table = Table(title="Listado de Frases Motivacionales")
    table.add_column("ID", justify="right")
    table.add_column("Texto")

    for frase in frases:
        table.add_row(str(frase.id), frase.texto)

    console.print(table)

def main() -> None:
    """
    Función principal que maneja el menú de la aplicación.
    """
    console.print("[bold cyan]¡Bienvenido a GastoMágico![/bold cyan]")
    mostrar_frase_motivacional(session)
    while True:
        console.print("\n[bold cyan]Menú Principal[/bold cyan]")
        console.print("1. Gestión de Gastos")
        console.print("2. Gestión de Tablas")
        console.print("3. Salir")
        opcion: str = input("Selecciona una opción: ")
        if opcion == '1':
            menu_gestion_gastos()
        elif opcion == '2':
            menu_gestion_tablas()
        elif opcion == '3':
            console.print("[bold green]¡Hasta luego![/bold green]")
            break
        else:
            console.print("[red]Opción inválida[/red]")

if __name__ == "__main__":
    main()
