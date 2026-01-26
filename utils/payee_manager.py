"""
Gestor de aseguradoras beneficiarias (payees).

Permite guardar y recuperar nombres de aseguradoras frecuentemente usadas.
"""
import json
from pathlib import Path
from typing import List, Optional, Dict
from threading import Lock


class PayeeManager:
    """
    Gestor de aseguradoras beneficiarias.
    
    Mantiene un registro de aseguradoras utilizadas para autocompletado
    y selección rápida.
    """
    
    def __init__(self, storage_file: Optional[Path] = None):
        """
        Inicializa el gestor de aseguradoras.
        
        Args:
            storage_file: Archivo donde se guardan las aseguradoras
        """
        self.storage_file = storage_file or Path('logs/payees.json')
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._load_payees()
    
    def _load_payees(self):
        """Carga las aseguradoras desde el archivo."""
        if self.storage_file.exists():
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        self.payees = data.get('payees', [])
                    else:
                        # Archivo vacío, crear default
                        self._create_default_payees()
            except (json.JSONDecodeError, KeyError):
                # Archivo corrupto, recrear
                self._create_default_payees()
        else:
            # Archivo no existe
            self._create_default_payees()
    
    def _create_default_payees(self):
        """Crea las aseguradoras por defecto."""
        self.payees = [
            {
                "name": "SEGUROS GENERALES SURAMERICANA S.A",
                "nit": "890903407-5",
                "link_pago": "WWW.SURA.COM",
                "usage_count": 0
            },
            {
                "name": "SEGUROS DE VIDA SURAMERICANA S.A",
                "nit": "890903790-5",
                "link_pago": "WWW.SURA.COM",
                "usage_count": 0
            },
            {
                "name": "ALLIANZ SEGUROS S.A",
                "nit": "860001220-8",
                "link_pago": "WWW.ALLIANZ.CO",
                "usage_count": 0
            },
            {
                "name": "ALLIANZ SEGUROS DE VIDA S.A",
                "nit": "890982420-0",
                "link_pago": "WWW.ALLIANZ.CO",
                "usage_count": 0
            },
            {
                "name": "HDI SEGUROS",
                "nit": "860035827-0",
                "link_pago": "WWW.HDI.COM.CO",
                "usage_count": 0
            },
            {
                "name": "SEGUROS DEL ESTADO S.A",
                "nit": "860009578-0",
                "link_pago": "WWW.SEGUROSDELESTADO.COM",
                "usage_count": 0
            },
            {
                "name": "SEGUROS DE VIDA DEL ESTADO",
                "nit": "830003564-5",
                "link_pago": "WWW.SEGUROSDELESTADO.COM",
                "usage_count": 0
            },
            {
                "name": "COMPANIA DE SEGUROS BOLIVAR S.A",
                "nit": "860002400-4",
                "link_pago": "WWW.SEGUROSBOLIVAR.COM",
                "usage_count": 0
            },
            {
                "name": "CHUBB SEGUROS COLOMBIA S.A.",
                "nit": "860002183-5",
                "link_pago": "WWW.CHUBB.COM/CO",
                "usage_count": 0
            },
            {
                "name": "SEGUROS MUNDIAL",
                "nit": "860045179-2",
                "link_pago": "WWW.SEGUROSMUNDIAL.COM.CO",
                "usage_count": 0
            },
            {
                "name": "MAPFRE SEGUROS GENERALES",
                "nit": "860002180-0",
                "link_pago": "WWW.MAPFRE.COM.CO",
                "usage_count": 0
            },
            {
                "name": "LA PREVISORA S A COMPANIA DE SEGUROS",
                "nit": "890982420-0",
                "link_pago": "WWW.LAPREVISORA.COM.CO",
                "usage_count": 0
            },
            {
                "name": "AXA COLPATRIA SEGUROS S.A",
                "nit": "860002184-3",
                "link_pago": "WWW.COLPATRIA.COM",
                "usage_count": 0
            },
            {
                "name": "AXA COLPATRIA SEGUROS DE VIDA S.A",
                "nit": "860069988-6",
                "link_pago": "WWW.COLPATRIA.COM",
                "usage_count": 0
            },
            {
                "name": "EMERMEDICA S.A SERVICIOS DE AMBULANCIA PREPAGADOS",
                "nit": "900000000-0",
                "link_pago": "WWW.EMERMEDICA.COM.CO",
                "usage_count": 0
            },
            {
                "name": "COMPANIA DE MEDICINA PREPAGADA COLSANITAS S.A.",
                "nit": "860000000-0",
                "link_pago": "WWW.COLSANITAS.COM",
                "usage_count": 0
            },
            {
                "name": "MEDISANITAS S.A.S COMPANIA DE MEDICINA PREPAGADA",
                "nit": "900000001-0",
                "link_pago": "WWW.MEDISANITAS.COM.CO",
                "usage_count": 0
            },
            {
                "name": "LA EQUIDAD SEGUROS GENERALES",
                "nit": "860026819-1",
                "link_pago": "WWW.LAEQUIDADSEGUROS.COOP",
                "usage_count": 0
            },
            {
                "name": "ASSIST CARD DE COLOMBIA SAS",
                "nit": "900000002-0",
                "link_pago": "WWW.ASSISTCARD.COM",
                "usage_count": 0
            },
            {
                "name": "COOMEVA MEDICINA PREPAGADA S.A.",
                "nit": "805000427-1",
                "link_pago": "WWW.COOMEVA.COM.CO",
                "usage_count": 0
            },
            {
                "name": "COLMENA SEGUROS",
                "nit": "860066740-7",
                "link_pago": "WWW.COLMENASEGUROS.COM",
                "usage_count": 0
            },
            {
                "name": "FUNERARIA SAN VICENTE S.A.",
                "nit": "890900000-0",
                "link_pago": "WWW.SANVICENTE.COM.CO",
                "usage_count": 0
            },
            {
                "name": "MAGENTA ASISTANCE S.A.S.",
                "nit": "900000003-0",
                "link_pago": "WWW.MAGENTA.COM.CO",
                "usage_count": 0
            },
            {
                "name": "COOMEVA EXPERIENCIA MEDICA SAS",
                "nit": "900000004-0",
                "link_pago": "WWW.COOMEVA.COM.CO",
                "usage_count": 0
            },
            {
                "name": "GRANCOLOMBIANA DE FIANZAS S.A.S",
                "nit": "860000001-0",
                "link_pago": "WWW.GRANFIANZAS.COM.CO",
                "usage_count": 0
            },
            {
                "name": "ASEGURADORA SOLIDARIA DE COLOMBIA",
                "nit": "860524654-8",
                "link_pago": "WWW.ASEGURADORASOLIDARIA.COM",
                "usage_count": 0
            },
            {
                "name": "POSITIVA COMPANIA DE SEGUROS S.A",
                "nit": "800251440-2",
                "link_pago": "WWW.POSITIVA.GOV.CO",
                "usage_count": 0
            },
            {
                "name": "SBS SEGUROS COLOMBIA S.A",
                "nit": "860069988-6",
                "link_pago": "WWW.SBS.COM.CO",
                "usage_count": 0
            },
            {
                "name": "ZURICH COLOMBIA SEGUROS S.A",
                "nit": "860009834-7",
                "link_pago": "WWW.ZURICH.CO",
                "usage_count": 0
            }
        ]
        self._save_payees()
    
    def _save_payees(self):
        """Guarda las aseguradoras en el archivo."""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump({
                'payees': self.payees,
                'last_updated': str(Path(__file__).parent)
            }, f, indent=2, ensure_ascii=False)
    
    def add_payee(self, name: str, nit: str, link_pago: str = "") -> Dict:
        """
        Agrega una nueva aseguradora o actualiza existente.
        
        Args:
            name: Nombre de la aseguradora
            nit: NIT de la aseguradora
            link_pago: Link de pago de la aseguradora
        
        Returns:
            Dict: Aseguradora agregada/actualizada
        """
        with self._lock:
            # Buscar si ya existe
            for payee in self.payees:
                if payee['name'].upper() == name.upper():
                    payee['nit'] = nit
                    payee['link_pago'] = link_pago.strip()
                    payee['usage_count'] += 1
                    self._save_payees()
                    return payee
            
            # Agregar nueva
            new_payee = {
                "name": name.upper().strip(),
                "nit": nit.strip(),
                "link_pago": link_pago.strip(),
                "usage_count": 1
            }
            self.payees.append(new_payee)
            self._save_payees()
            return new_payee
    
    def get_all_payees(self) -> List[Dict]:
        """
        Obtiene todas las aseguradoras ordenadas por uso.
        
        Returns:
            List[Dict]: Lista de aseguradoras
        """
        return sorted(self.payees, key=lambda x: x['usage_count'], reverse=True)
    
    def get_payee_by_name(self, name: str) -> Optional[Dict]:
        """
        Busca una aseguradora por nombre.
        
        Args:
            name: Nombre de la aseguradora
        
        Returns:
            Optional[Dict]: Aseguradora encontrada o None
        """
        name_upper = name.upper().strip()
        for payee in self.payees:
            if payee['name'].upper() == name_upper:
                return payee
        return None
    
    def increment_usage(self, name: str):
        """
        Incrementa el contador de uso de una aseguradora.
        
        Args:
            name: Nombre de la aseguradora
        """
        with self._lock:
            for payee in self.payees:
                if payee['name'].upper() == name.upper():
                    payee['usage_count'] += 1
                    self._save_payees()
                    break
    
    def get_payee_names(self) -> List[str]:
        """
        Obtiene lista de nombres de aseguradoras.
        
        Returns:
            List[str]: Nombres de aseguradoras
        """
        return [payee['name'] for payee in self.get_all_payees()]
    
    def delete_payee(self, name: str) -> bool:
        """
        Elimina una aseguradora por nombre.
        
        Args:
            name: Nombre de la aseguradora a eliminar
        
        Returns:
            bool: True si se eliminó, False si no se encontró
        """
        with self._lock:
            name_upper = name.upper().strip()
            for idx, payee in enumerate(self.payees):
                if payee['name'].upper() == name_upper:
                    self.payees.pop(idx)
                    self._save_payees()
                    return True
            return False
    
    def update_payee(self, old_name: str, new_name: str, new_nit: str, new_link_pago: str = "") -> Optional[Dict]:
        """
        Actualiza el nombre y/o NIT de una aseguradora existente.
        
        Args:
            old_name: Nombre actual de la aseguradora
            new_name: Nuevo nombre de la aseguradora
            new_nit: Nuevo NIT de la aseguradora
            new_link_pago: Nuevo link de pago de la aseguradora
        
        Returns:
            Optional[Dict]: Aseguradora actualizada o None si no se encontró
        """
        with self._lock:
            old_name_upper = old_name.upper().strip()
            for payee in self.payees:
                if payee['name'].upper() == old_name_upper:
                    payee['name'] = new_name.upper().strip()
                    payee['nit'] = new_nit.strip()
                    payee['link_pago'] = new_link_pago.strip()
                    self._save_payees()
                    return payee
            return None


# Instancia global
payee_manager = PayeeManager()
