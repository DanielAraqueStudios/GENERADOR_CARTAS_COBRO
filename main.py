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
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        app.setApplicationName(config.APP_NAME)
        app.setApplicationVersion(config.APP_VERSION)
        
        # TODO: Importar y crear ventana principal
        # from gui.main_window import MainWindow
        # window = MainWindow()
        # window.show()
        
        # Placeholder mientras se implementa la GUI
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(config.APP_NAME)
        msg.setText(f"{config.APP_NAME} v{config.APP_VERSION}")
        msg.setInformativeText(
            "La interfaz gráfica está en desarrollo.\n\n"
            "Por ahora, usa la interfaz CLI:\n"
            "python cli.py --interactive"
        )
        msg.exec()
        
        logger.info(f"Aplicación iniciada: {config.APP_NAME} v{config.APP_VERSION}")
        
        # return app.exec()
        return 0
        
    except Exception as e:
        logger.error(f"Error al iniciar la aplicación: {str(e)}", exc_info=True)
        print(f"❌ Error: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
