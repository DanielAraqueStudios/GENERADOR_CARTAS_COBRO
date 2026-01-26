"""
Validadores de campos individuales.
"""
import re
from typing import Tuple, Optional
from decimal import Decimal
from datetime import date, datetime


class FieldValidator:
    """Validadores estáticos para campos individuales."""
    
    @staticmethod
    def validate_nit_colombiano(nit: str) -> Tuple[bool, Optional[str]]:
        """
        Valida que el NIT no esté vacío.
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not nit or not nit.strip():
            return False, "NIT no puede estar vacío"
        return True, None
    
    @staticmethod
    def validate_telefono_colombiano(telefono: str) -> Tuple[bool, Optional[str]]:
        """
        Valida que el teléfono no esté vacío.
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not telefono or not telefono.strip():
            return False, "Teléfono no puede estar vacío"
        return True, None
    
    @staticmethod
    def validate_numero_poliza(numero: str) -> Tuple[bool, Optional[str]]:
        """
        Valida que el número de póliza no esté vacío.
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not numero or not numero.strip():
            return False, "Número de póliza no puede estar vacío"
        return True, None
    
    @staticmethod
    def validate_plan_poliza(plan: str) -> Tuple[bool, Optional[str]]:
        """
        Valida que el plan de póliza no esté vacío.
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not plan or not plan.strip():
            return False, "Plan póliza no puede estar vacío"
        return True, None
    
    @staticmethod
    def validate_positive_amount(amount: float) -> Tuple[bool, Optional[str]]:
        """
        Valida que un monto sea un número válido.
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if amount is None:
            return False, "Monto no puede estar vacío"
        
        try:
            float(amount)
            return True, None
        except (ValueError, TypeError):
            return False, "Monto debe ser un número válido"
    
    @staticmethod
    def validate_text_not_empty(text: str) -> Tuple[bool, Optional[str]]:
        """
        Valida que un texto no esté vacío.
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not text or not text.strip():
            return False, "Este campo no puede estar vacío"
        return True, None
    
    @staticmethod
    def validate_valid_date(date_value) -> Tuple[bool, Optional[str]]:
        """
        Valida que una fecha sea válida.
        
        Args:
            date_value: Puede ser date, datetime, o str en formato ISO
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not date_value:
            return False, "Fecha no puede estar vacía"
        
        try:
            if isinstance(date_value, date):
                return True, None
            elif isinstance(date_value, str):
                # Intentar parsear formato ISO
                datetime.strptime(date_value, '%Y-%m-%d')
                return True, None
            else:
                return False, "Formato de fecha inválido"
        except (ValueError, TypeError) as e:
            return False, f"Fecha inválida: {str(e)}"
    
    @staticmethod
    def validate_numero_carta(numero: str) -> Tuple[bool, Optional[str]]:
        """
        Valida que el número de carta no esté vacío.
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not numero or not numero.strip():
            return False, "Número de carta no puede estar vacío"
        return True, None


class CurrencyFormatter:
    """Utilidades para formatear moneda colombiana."""
    
    @staticmethod
    def to_colombian_format(value: float) -> str:
        """
        Convierte un número a formato colombiano.
        
        Args:
            value: Número decimal
        
        Returns:
            str: Formato colombiano (ej: "1.372.412,00")
        """
        formatted = f"{value:,.2f}"
        # Intercambiar separadores: coma por punto y viceversa
        return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @staticmethod
    def from_colombian_format(text: str) -> float:
        """
        Convierte texto en formato colombiano a número.
        
        Args:
            text: Texto en formato colombiano (ej: "1.372.412,00")
        
        Returns:
            float: Valor numérico
        """
        # Remover puntos (miles) y reemplazar coma (decimal) por punto
        cleaned = text.replace('.', '').replace(',', '.')
        return float(cleaned)


class DateFormatter:
    """Utilidades para formatear fechas en español."""
    
    MESES_LARGO = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    
    MESES_CORTO_UPPER = {
        1: "ENE.", 2: "FEB.", 3: "MAR.", 4: "ABR.", 5: "MAY.", 6: "JUN.",
        7: "JUL.", 8: "AGO.", 9: "SEPT.", 10: "OCT.", 11: "NOV.", 12: "DIC."
    }
    
    MESES_CORTO_LOWER = {
        1: "ene.", 2: "feb.", 3: "mar.", 4: "abr.", 5: "may.", 6: "jun.",
        7: "jul.", 8: "ago.", 9: "sept.", 10: "oct.", 11: "nov.", 12: "dic."
    }
    
    @classmethod
    def to_long_spanish(cls, fecha: date) -> str:
        """18 de diciembre de 2025"""
        return f"{fecha.day} de {cls.MESES_LARGO[fecha.month - 1]} de {fecha.year}"
    
    @classmethod
    def to_short_upper(cls, fecha: date) -> str:
        """30-SEPT.-2025"""
        return f"{fecha.day}-{cls.MESES_CORTO_UPPER[fecha.month]}-{fecha.year}"
    
    @classmethod
    def to_short_lower(cls, fecha: date) -> str:
        """23-dic.-2025"""
        return f"{fecha.day}-{cls.MESES_CORTO_LOWER[fecha.month]}-{fecha.year}"
