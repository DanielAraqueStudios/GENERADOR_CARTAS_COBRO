"""
Control de versiones y consecutivos de documentos.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
from threading import Lock


class VersionManager:
    """
    Gestor de versiones y consecutivos de documentos.
    
    Mantiene un registro de consecutivos por año para números de carta.
    """
    
    def __init__(self, storage_file: Optional[Path] = None):
        """
        Inicializa el gestor de versiones.
        
        Args:
            storage_file: Archivo donde se guardan los consecutivos
        """
        self.storage_file = storage_file or Path('logs/consecutivos.json')
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._load_consecutivos()
    
    def _load_consecutivos(self):
        """Carga los consecutivos desde el archivo."""
        if self.storage_file.exists():
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                self.consecutivos = json.load(f)
        else:
            self.consecutivos = {}
    
    def _save_consecutivos(self):
        """Guarda los consecutivos en el archivo."""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.consecutivos, f, indent=2, ensure_ascii=False)
    
    def get_next_numero_carta(self, year: Optional[int] = None) -> str:
        """
        Genera el siguiente número de carta para el año especificado.
        
        Args:
            year: Año para el consecutivo (None = año actual)
        
        Returns:
            str: Número de carta en formato "15434 - 2025"
        """
        with self._lock:
            year = year or datetime.now().year
            year_key = str(year)
            
            # Obtener consecutivo actual del año
            if year_key not in self.consecutivos:
                self.consecutivos[year_key] = {
                    'last_consecutivo': 0,
                    'year': year
                }
            
            # Incrementar consecutivo
            self.consecutivos[year_key]['last_consecutivo'] += 1
            consecutivo = self.consecutivos[year_key]['last_consecutivo']
            
            # Guardar
            self._save_consecutivos()
            
            return f"{consecutivo} - {year}"
    
    def get_current_consecutivo(self, year: Optional[int] = None) -> int:
        """
        Obtiene el consecutivo actual sin incrementar.
        
        Args:
            year: Año del consecutivo
        
        Returns:
            int: Consecutivo actual
        """
        year = year or datetime.now().year
        year_key = str(year)
        
        if year_key not in self.consecutivos:
            return 0
        
        return self.consecutivos[year_key]['last_consecutivo']
    
    def set_consecutivo(self, consecutivo: int, year: Optional[int] = None):
        """
        Establece manualmente el consecutivo para un año.
        
        Args:
            consecutivo: Número de consecutivo
            year: Año (None = año actual)
        """
        with self._lock:
            year = year or datetime.now().year
            year_key = str(year)
            
            self.consecutivos[year_key] = {
                'last_consecutivo': consecutivo,
                'year': year
            }
            
            self._save_consecutivos()
    
    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas de documentos generados.
        
        Returns:
            Dict: Estadísticas por año
        """
        return {
            year_key: {
                'year': data['year'],
                'total_documents': data['last_consecutivo']
            }
            for year_key, data in self.consecutivos.items()
        }


# Instancia global
version_manager = VersionManager()
