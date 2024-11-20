from gastomagico.utils.database import session
from models import Frase

def agregar_frases() -> None:
    """
    Agrega frases motivacionales a la base de datos.
    """
    frases = [
        Frase(texto="¡Sigue ahorrando, cada centavo cuenta!"),
        Frase(texto="La constancia es la clave del éxito financiero."),
        Frase(texto="¡Estás más cerca de tus metas!"),
        Frase(texto="El éxito es la suma de pequeños esfuerzos repetidos día tras día."),
        Frase(texto="Ahorra hoy para disfrutar mañana."),
    ]
    session.add_all(frases)
    session.commit()
    print("Frases motivacionales agregadas correctamente.")

if __name__ == "__main__":
    agregar_frases()
