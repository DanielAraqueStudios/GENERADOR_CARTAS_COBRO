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
        description="Razón social o nombre completo del cliente"
    )
    nit: str = Field(
        ..., 
        description="NIT del cliente"
    )
    direccion: str = Field(
        ..., 
        description="Dirección completa del cliente"
    )
    telefono: str = Field(
        ..., 
        description="Teléfono del cliente"
    )
    ciudad: str = Field(
        ..., 
        description="Ciudad de residencia del cliente"
    )
    
    @field_validator('razon_social')
    @classmethod
    def uppercase_razon_social(cls, v: str) -> str:
        """Convierte la razón social a mayúsculas."""
        return v.upper().strip()
    
    @field_validator('ciudad')
    @classmethod
    def uppercase_ciudad(cls, v: str) -> str:
        """Convierte la ciudad a mayúsculas."""
        return v.upper().strip()
    
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
