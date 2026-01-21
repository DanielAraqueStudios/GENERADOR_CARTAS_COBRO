"""
Modelo de datos del asegurado/cliente.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class Asegurado(BaseModel):
    """
    Representa los datos del asegurado/cliente destinatario de la carta de cobro.
    """
    
    razon_social: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Razón social o nombre completo del cliente"
    )
    nit: str = Field(
        ..., 
        pattern=r"^\d{9}-\d$",
        description="NIT colombiano con dígito de verificación (formato: 123456789-0)"
    )
    direccion: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Dirección completa del cliente"
    )
    telefono: str = Field(
        ..., 
        pattern=r"^\d{7,10}$",
        description="Teléfono fijo o móvil (7-10 dígitos)"
    )
    ciudad: str = Field(
        ..., 
        min_length=1,
        description="Ciudad de residencia del cliente"
    )
    
    @field_validator('razon_social')
    @classmethod
    def uppercase_razon_social(cls, v: str) -> str:
        """Convierte la razón social a mayúsculas."""
        return v.upper().strip()
    
    @field_validator('nit')
    @classmethod
    def validate_nit(cls, v: str) -> str:
        """
        Valida el formato y dígito de verificación del NIT colombiano.
        
        Algoritmo de dígito de verificación según DIAN Colombia.
        """
        if not v or len(v) < 11:
            raise ValueError("NIT debe tener formato 123456789-0")
        
        # Extraer dígitos sin el guión
        digits = v.replace('-', '')
        if len(digits) != 10:
            raise ValueError("NIT debe tener 9 dígitos + 1 dígito de verificación")
        
        # Validar dígito de verificación
        base = digits[:9]
        check_digit = int(digits[9])
        
        primes = [3, 7, 13, 17, 19, 23, 29, 37, 41]
        total = sum(int(base[i]) * primes[i] for i in range(9))
        calculated_check = (11 - (total % 11)) % 11
        
        if calculated_check != check_digit:
            raise ValueError(f"Dígito de verificación inválido. Esperado: {calculated_check}, Recibido: {check_digit}")
        
        return v
    
    def model_dump_for_pdf(self) -> dict:
        """Retorna datos formateados para insertar en el PDF."""
        return {
            "cliente_razon_social": self.razon_social,
            "cliente_nit": self.nit,
            "cliente_direccion": self.direccion,
            "cliente_telefono": self.telefono,
            "cliente_ciudad": self.ciudad
        }
    
    class Config:
        json_schema_extra = {
            "example": {
                "razon_social": "COOPERATIVA DEL COMERCIO EXTERIOR COLOMBIANO",
                "nit": "860023108-6",
                "direccion": "CR 13 28 01 P 5",
                "telefono": "6067676",
                "ciudad": "Bogotá D.C."
            }
        }
