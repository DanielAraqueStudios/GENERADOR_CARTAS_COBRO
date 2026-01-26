"""
Gestor de ramos de pólizas.

Permite guardar y recuperar ramos frecuentemente usados.
"""
import json
from pathlib import Path
from typing import List
from threading import Lock


class RamoManager:
    """
    Gestor de ramos de pólizas.
    
    Mantiene un registro de ramos utilizados para autocompletado
    y selección rápida.
    """
    
    def __init__(self, storage_file: Path = None):
        """
        Inicializa el gestor de ramos.
        
        Args:
            storage_file: Archivo donde se guardan los ramos
        """
        self.storage_file = storage_file or Path('logs/ramos.json')
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._load_ramos()
    
    def _load_ramos(self):
        """Carga los ramos desde el archivo."""
        if self.storage_file.exists():
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        self.ramos = data.get('ramos', [])
                    else:
                        self._create_default_ramos()
            except (json.JSONDecodeError, KeyError):
                self._create_default_ramos()
        else:
            self._create_default_ramos()
    
    def _create_default_ramos(self):
        """Crea ramos predeterminados."""
        self.ramos = [
            "AUTOS INDIVIDUAL",
            "HOGAR",
            "MULTIRRIESGO EMPRESARIAL",
            "RC DERIVADA DE CUMPLIMIENTO",
            "RC PREDIOS LABORES Y OPERACIONES",
            "TRANSPORTES DE MERCANCIAS",
            "TODO RIESGO DAÑOS MATERIALES",
            "MANEJO ENTIDADES FINANCIERAS",
            "COPROPIEDADES",
            "VIDA ACTUAL",
            "VIDA GRUPO CONTRIBUTIVA",
            "VIDA GRUPO CONTRIBUTIVO",
            "ACCIDENTES PERSONALES",
            "SALUD CLASICO",
            "SALUD COLECTIVA CLASICO",
            "PLAN COMPLEMENTARIO",
            "SEGUROS EXEQUIALES",
            "MEDICINA PREPAGADA COLECTIV",
            "CEM",
            "EMERGENCIAS MÉDICAS",
            "ASSIST CARD",
            "SOAT",
            "CUMPLIMIENTO",
            "MI PYME",
            "RC CLINICAS Y HOSPITALES",
            "TRANSPORTE DE VALORES",
            "MAQUINARIA Y EQUIPO",
            "ARRENDAMIENTO",
            "PROTECCION DIGITAL",
            "AERONAVES CASCO",
            "ACCIDENTES JUVENILES",
            "ACCIDENTES ESCOLARES",
            "SALUD PARA TODOS",
            "PLAN COMPLEMENTARIO COLECTIVO",
            "ARL",
            "RENTA EDUCATIVA",
            "MAS VIDA",
            "MEDICINA PREPAGADA FAMILIAR"
        ]
        self._save()
    
    def _save(self):
        """Guarda los ramos en el archivo."""
        with self._lock:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump({'ramos': self.ramos}, f, ensure_ascii=False, indent=2)
    
    def add_ramo(self, ramo: str):
        """
        Agrega un nuevo ramo si no existe.
        
        Args:
            ramo: Ramo a agregar
        """
        ramo = ramo.strip().upper()
        if ramo and ramo not in self.ramos:
            self.ramos.append(ramo)
            # Ordenar alfabéticamente
            self.ramos.sort()
            self._save()
    
    def get_all(self) -> List[str]:
        """
        Obtiene todos los ramos.
        
        Returns:
            Lista de ramos
        """
        return sorted(self.ramos)
    
    def remove_ramo(self, ramo: str):
        """
        Elimina un ramo.
        
        Args:
            ramo: Ramo a eliminar
        """
        if ramo in self.ramos:
            self.ramos.remove(ramo)
            self._save()


# Instancia global
ramo_manager = RamoManager()
