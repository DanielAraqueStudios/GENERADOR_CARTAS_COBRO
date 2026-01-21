"""
Configuración global del sistema.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """
    Configuración centralizada del sistema.
    
    Carga variables de entorno desde .env y proporciona valores por defecto.
    """
    
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()
        
        # Rutas base
        self.BASE_DIR = Path(__file__).parent.parent
        self.TEMPLATES_DIR = self.BASE_DIR / os.getenv('TEMPLATES_DIR', 'templates')
        self.OUTPUT_DIR = self.BASE_DIR / os.getenv('OUTPUT_DIR', 'output')
        self.LOGS_DIR = self.BASE_DIR / os.getenv('LOGS_DIR', 'logs')
        
        # Información de la aplicación
        self.APP_NAME = os.getenv('APP_NAME', 'Generador de Cartas de Cobro')
        self.APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
        
        # Información de las compañías
        self.SENDER_COMPANY_NAME = os.getenv('SENDER_COMPANY_NAME', 'SEGUROS UNIÓN')
        self.SENDER_ADDRESS = os.getenv(
            'SENDER_ADDRESS',
            'Carrera 77 A # 49 - 37 .Sector Estadio - Medellin'
        )
        self.SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'gerencia@segurosunion.com')
        
        self.PAYEE_COMPANY_NAME = os.getenv(
            'PAYEE_COMPANY_NAME',
            'SEGUROS DE VIDA SURAMERICANA S.A.'
        )
        self.PAYEE_NIT = os.getenv('PAYEE_NIT', '890903790-5')
        
        # Configuración PDF
        self.PDF_PAGE_SIZE = os.getenv('PDF_PAGE_SIZE', 'LETTER')
        self.PDF_MARGIN_TOP = float(os.getenv('PDF_MARGIN_TOP', '2.5'))
        self.PDF_MARGIN_BOTTOM = float(os.getenv('PDF_MARGIN_BOTTOM', '2.0'))
        self.PDF_MARGIN_LEFT = float(os.getenv('PDF_MARGIN_LEFT', '2.5'))
        self.PDF_MARGIN_RIGHT = float(os.getenv('PDF_MARGIN_RIGHT', '2.5'))
        
        # Logging
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FORMAT = os.getenv(
            'LOG_FORMAT',
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Crear directorios si no existen
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Crea directorios necesarios si no existen."""
        self.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        (self.OUTPUT_DIR / 'cartas').mkdir(parents=True, exist_ok=True)
        (self.OUTPUT_DIR / 'borradores').mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    def get_template_path(self, template_id: str) -> Path:
        """
        Obtiene la ruta completa a un archivo de plantilla.
        
        Args:
            template_id: ID de la plantilla (ej: 'carta_cobro_seguros_union')
        
        Returns:
            Path: Ruta completa al archivo JSON de la plantilla
        """
        return self.TEMPLATES_DIR / f"{template_id}.json"
    
    def to_dict(self) -> dict:
        """Retorna la configuración como diccionario."""
        return {
            'app_name': self.APP_NAME,
            'app_version': self.APP_VERSION,
            'sender_company_name': self.SENDER_COMPANY_NAME,
            'sender_address': self.SENDER_ADDRESS,
            'sender_email': self.SENDER_EMAIL,
            'payee_company_name': self.PAYEE_COMPANY_NAME,
            'payee_nit': self.PAYEE_NIT
        }


# Instancia global de configuración
config = Config()
