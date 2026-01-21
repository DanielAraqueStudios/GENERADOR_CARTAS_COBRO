"""
Clase base abstracta para generadores de PDF.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json


class BaseGenerator(ABC):
    """
    Clase base abstracta para todos los generadores de PDF.
    
    Define la interfaz común y métodos auxiliares compartidos.
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Inicializa el generador.
        
        Args:
            output_dir: Directorio donde se guardarán los PDFs generados
        """
        self.output_dir = output_dir or Path("output/cartas")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def generate(self, data: Dict[str, Any], output_filename: str) -> Path:
        """
        Genera el documento PDF.
        
        Args:
            data: Diccionario con los datos del documento
            output_filename: Nombre del archivo de salida (sin extensión)
        
        Returns:
            Path: Ruta completa al archivo PDF generado
        """
        pass
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Valida que los datos tengan todos los campos requeridos.
        
        Args:
            data: Diccionario con los datos a validar
        
        Returns:
            bool: True si los datos son válidos
        
        Raises:
            ValueError: Si los datos son inválidos
        """
        pass
    
    def _get_output_path(self, filename: str, is_draft: bool = False) -> Path:
        """
        Determina la ruta de salida según el estado del documento.
        
        Args:
            filename: Nombre base del archivo
            is_draft: Si es borrador, se guarda en carpeta diferente
        
        Returns:
            Path: Ruta completa al archivo
        """
        if is_draft:
            output_dir = self.output_dir.parent / "borradores"
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = self.output_dir
        
        # Asegurar extensión .pdf
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        return output_dir / filename
    
    def _generate_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Genera metadatos para el PDF.
        
        Args:
            data: Datos del documento
        
        Returns:
            Dict: Metadatos del PDF
        """
        return {
            "title": f"Carta de Cobro {data.get('numero_carta', 'N/A')}",
            "author": data.get('sender_company_name', 'SEGUROS UNIÓN'),
            "subject": f"Cobro Póliza {data.get('poliza_numero', 'N/A')}",
            "creator": "Generador de Cartas de Cobro v1.0",
            "creation_date": datetime.now()
        }
    
    def _log_generation(self, data: Dict[str, Any], output_path: Path, success: bool = True):
        """
        Registra la generación del documento en el log de auditoría.
        
        Args:
            data: Datos del documento generado
            output_path: Ruta del archivo generado
            success: Si la generación fue exitosa
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "document_type": self.__class__.__name__,
            "document_number": data.get('numero_carta', 'N/A'),
            "policy_number": data.get('poliza_numero', 'N/A'),
            "client_nit": data.get('cliente_nit', 'N/A'),
            "output_path": str(output_path),
            "status": "success" if success else "failed",
            "is_draft": data.get('es_borrador', False)
        }
        
        # Guardar en log de auditoría
        log_file = Path("logs") / "audit_trail.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
