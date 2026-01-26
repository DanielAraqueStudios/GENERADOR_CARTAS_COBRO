"""
Gestor de descripciones de pólizas.

Permite guardar y recuperar descripciones frecuentemente usadas.
"""
import json
from pathlib import Path
from typing import List
from threading import Lock


class DescripcionManager:
    """
    Gestor de descripciones de pólizas.
    
    Mantiene un registro de descripciones utilizadas para autocompletado
    y selección rápida.
    """
    
    def __init__(self, storage_file: Path = None):
        """
        Inicializa el gestor de descripciones.
        
        Args:
            storage_file: Archivo donde se guardan las descripciones
        """
        self.storage_file = storage_file or Path('logs/descripciones.json')
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._load_descripciones()
    
    def _load_descripciones(self):
        """Carga las descripciones desde el archivo."""
        if self.storage_file.exists():
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        self.descripciones = data.get('descripciones', [])
                    else:
                        self._create_default_descripciones()
            except (json.JSONDecodeError, KeyError):
                self._create_default_descripciones()
        else:
            self._create_default_descripciones()
    
    def _create_default_descripciones(self):
        """Crea descripciones predeterminadas."""
        self.descripciones = [
            "Plan Empresarial Plus",
            "Cobertura Total",
            "Plan Básico",
            "Plan Premium",
            "Cobertura Familiar"
        ]
        self._save()
    
    def _save(self):
        """Guarda las descripciones en el archivo."""
        with self._lock:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump({'descripciones': self.descripciones}, f, ensure_ascii=False, indent=2)
    
    def add_descripcion(self, descripcion: str):
        """
        Agrega una nueva descripción si no existe.
        
        Args:
            descripcion: Descripción a agregar
        """
        descripcion = descripcion.strip()
        if descripcion and descripcion not in self.descripciones:
            self.descripciones.append(descripcion)
            # Ordenar alfabéticamente
            self.descripciones.sort()
            self._save()
    
    def get_all(self) -> List[str]:
        """
        Obtiene todas las descripciones.
        
        Returns:
            Lista de descripciones
        """
        return sorted(self.descripciones)
    
    def remove_descripcion(self, descripcion: str):
        """
        Elimina una descripción.
        
        Args:
            descripcion: Descripción a eliminar
        """
        if descripcion in self.descripciones:
            self.descripciones.remove(descripcion)
            self._save()


# Instancia global
descripcion_manager = DescripcionManager()
