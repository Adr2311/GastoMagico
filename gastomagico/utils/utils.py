from rich.console import Console
import random
from sqlalchemy.orm import Session

console = Console()

def mostrar_frase_motivacional(session: Session) -> None:
    """
    Muestra una frase motivacional aleatoria de la base de datos.

    Args:
        session (Session): Sesión de base de datos.
    """
    from gastomagico.utils.models import Frase
    frases = session.query(Frase).all()
    if frases:
        frase = random.choice(frases)
        console.print(f":sparkles: [bold magenta]{frase.texto}[/bold magenta] :sparkles:")
