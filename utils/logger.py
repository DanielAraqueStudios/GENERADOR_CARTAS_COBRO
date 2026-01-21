"""
Sistema de logging centralizado.
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class Logger:
    """
    Sistema de logging centralizado para el proyecto.
    """
    
    _instance: Optional['Logger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.loggers = {}
        self._setup_base_logger()
    
    def _setup_base_logger(self):
        """Configura el logger base."""
        log_dir = Path('logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo de log con fecha
        log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para archivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Logger raíz
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Obtiene un logger con el nombre especificado.
        
        Args:
            name: Nombre del logger (usualmente __name__)
        
        Returns:
            logging.Logger: Logger configurado
        """
        if name not in self.loggers:
            logger = logging.getLogger(name)
            self.loggers[name] = logger
        
        return self.loggers[name]


# Instancia global
logger_manager = Logger()


def get_logger(name: str) -> logging.Logger:
    """
    Función de conveniencia para obtener un logger.
    
    Args:
        name: Nombre del logger (usar __name__)
    
    Returns:
        logging.Logger: Logger configurado
    
    Example:
        >>> from utils.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Mensaje informativo")
    """
    return logger_manager.get_logger(name)
