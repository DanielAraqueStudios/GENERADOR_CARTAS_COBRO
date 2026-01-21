"""
Punto de entrada principal para la aplicación GUI.

Ejecuta la interfaz gráfica PyQt6 del generador de cartas de cobro.
"""
import sys
from PyQt6.QtWidgets import QApplication
from utils.config import config
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Función principal de la aplicación GUI."""
    try:
        # Importar y ejecutar la GUI simple
        from gui_simple import GeneradorCartasGUI
        
        app = QApplication(sys.argv)
        app.setApplicationName(config.APP_NAME)
        app.setApplicationVersion(config.APP_VERSION)
        app.setStyle("Fusion")
        
        window = GeneradorCartasGUI()
        window.show()
        
        logger.info(f"Aplicación iniciada: {config.APP_NAME} v{config.APP_VERSION}")
        
        # Iniciar bucle de eventos
        return app.exec()
        
    except Exception as e:
        logger.error(f"Error al iniciar la aplicación: {str(e)}", exc_info=True)
        print(f"❌ Error: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
