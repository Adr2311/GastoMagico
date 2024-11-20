# utils/console.py

from rich.console import Console
from utils.database import session
from utils.models import Frase
import random

console = Console()

def mostrar_frase_motivacional():
    frases = session.query(Frase).all()
    if frases:
        frase = random.choice(frases)
        console.print(f"\n[italic blue]{frase.texto}[/italic blue]\n")
