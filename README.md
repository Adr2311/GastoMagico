
# GastoMágico 💰

GastoMágico es una aplicación web diseñada para el control personal de gastos. Utiliza Streamlit para la interfaz de usuario y SQLAlchemy para la gestión de la base de datos.

## Características

- **Registro de Gastos**: Añade, edita y elimina tus gastos diarios.
- **Categorías Personalizadas**: Organiza tus gastos por categorías como Alimentación, Transporte, Entretenimiento, Salud, y Educación.
- **Métodos de Pago**: Gestiona diferentes métodos de pago como Efectivo, Tarjeta de Crédito, Débito y Transferencias Bancarias.
- **Reportes y Análisis**: Genera reportes en Excel y visualizaciones gráficas de tus gastos mensuales y diarios.
- **Frases Motivacionales**: Recibe una frase motivacional aleatoria para mantenerte inspirado.
- **Configuración de Límites**: Establece límites de gasto para mantener tus finanzas bajo control.

## Instalación

### Prerrequisitos

- Python 3.7 o superior
- Pip

### Pasos

1. **Clonar el repositorio**
    ```bash
    git clone https://github.com/tu-usuario/GastoMagico.git
    cd GastoMagico
    ```

2. **Crear un entorno virtual**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. **Instalar las dependencias**
    ```bash
    pip install -r requirements.txt
    ```

4. **Inicializar la base de datos**
    ```bash
    python main.py
    ```

## Uso

Inicia la aplicación Streamlit ejecutando el siguiente comando en la raíz del proyecto:

```bash
streamlit run main.py
```

La aplicación estará disponible en `http://localhost:8501`. Desde allí, podrás:

- **Agregar Gastos**: Registra tus gastos con detalles como monto, descripción, categoría y método de pago.
- **Gestionar Categorías y Métodos de Pago**: Añade o elimina categorías y métodos de pago según tus necesidades.
- **Generar Reportes**: Exporta tus gastos a un archivo Excel o visualiza reportes gráficos directamente en la aplicación.
- **Establecer Límites de Gasto**: Configura un límite de gasto mensual para mantener tus finanzas bajo control.

## Contribuciones

¡Las contribuciones son bienvenidas! Sigue estos pasos para contribuir:

1. **Fork** el repositorio.
2. **Crea una rama** para tu característica (`git checkout -b feature/tu-caracteristica`).
3. **Commit** tus cambios (`git commit -m 'Añadir nueva característica'`).
4. **Push** a la rama (`git push origin feature/tu-caracteristica`).
5. **Abre un Pull Request**.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
