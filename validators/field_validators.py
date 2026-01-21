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
        Valida formato y dígito de verificación de NIT colombiano.
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not nit:
            return False, "NIT no puede estar vacío"
        
        # Normalizar: remover espacios
        nit = nit.strip().replace(' ', '')
        
        # Validar formato
        if not re.match(r'^\d{9}-\d$', nit):
            return False, "Formato de NIT inválido. Use: 123456789-0"
        
        # Extraer dígitos
        digits = nit.replace('-', '')
        base = digits[:9]
        check_digit = int(digits[9])
        
        # Calcular dígito de verificación según DIAN
        primes = [3, 7, 13, 17, 19, 23, 29, 37, 41]
        try:
            total = sum(int(base[i]) * primes[i] for i in range(9))
            calculated_check = (11 - (total % 11)) % 11
            
            if calculated_check != check_digit:
                return False, f"Dígito de verificación incorrecto. Debería ser: {calculated_check}"
            
            return True, None
        except (ValueError, IndexError) as e:
            return False, f"Error al validar NIT: {str(e)}"
    
    @staticmethod
    def validate_telefono_colombiano(telefono: str) -> Tuple[bool, Optional[str]]:
        """
        Valida teléfono colombiano (fijo o móvil).
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not telefono:
            return False, "Teléfono no puede estar vacío"
        
        # Remover espacios y guiones
        telefono = telefono.strip().replace(' ', '').replace('-', '')
        
        # Validar solo dígitos
        if not telefono.isdigit():
            return False, "Teléfono solo debe contener dígitos"
        
        # Validar longitud (7-10 dígitos)
        if not (7 <= len(telefono) <= 10):
            return False, "Teléfono debe tener entre 7 y 10 dígitos"
        
        return True, None
    
    @staticmethod
    def validate_numero_poliza(numero: str) -> Tuple[bool, Optional[str]]:
        """
        Valida número de póliza (7 dígitos).
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not numero:
            return False, "Número de póliza no puede estar vacío"
        
        numero = numero.strip()
        
        if not numero.isdigit():
            return False, "Número de póliza solo debe contener dígitos"
        
        if len(numero) != 7:
            return False, "Número de póliza debe tener exactamente 7 dígitos"
        
        return True, None
    
    @staticmethod
    def validate_plan_poliza(plan: str) -> Tuple[bool, Optional[str]]:
        """
        Valida formato de plan póliza (ej: "06  3144016" - dos espacios).
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not plan:
            return False, "Plan póliza no puede estar vacío"
        
        # Debe tener exactamente dos espacios consecutivos
        if '  ' not in plan:
            return False, "Plan póliza debe tener formato: 06  3144016 (dos espacios)"
        
        parts = plan.split('  ')
        if len(parts) != 2:
            return False, "Plan póliza debe tener formato: código  número"
        
        codigo, numero = parts
        
        if not codigo.isdigit() or len(codigo) != 2:
            return False, "Código de plan debe ser 2 dígitos"
        
        if not numero.isdigit() or len(numero) != 7:
            return False, "Número de póliza debe ser 7 dígitos"
        
        return True, None
    
    @staticmethod
    def validate_positive_amount(amount: float) -> Tuple[bool, Optional[str]]:
        """
        Valida que un monto sea positivo o cero.
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if amount is None:
            return False, "Monto no puede estar vacío"
        
        try:
            value = float(amount)
            if value < 0:
                return False, "Monto no puede ser negativo"
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
        Valida formato de número de carta (ej: "15434 - 2025").
        
        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if not numero:
            return False, "Número de carta no puede estar vacío"
        
        if not re.match(r'^\d+ - \d{4}$', numero):
            return False, "Número de carta debe tener formato: 15434 - 2025"
        
        # Extraer año y validar
        parts = numero.split(' - ')
        try:
            year = int(parts[1])
            current_year = datetime.now().year
            if year < 2000 or year > current_year + 1:
                return False, f"Año debe estar entre 2000 y {current_year + 1}"
        except (IndexError, ValueError):
            return False, "Formato de año inválido"
        
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
