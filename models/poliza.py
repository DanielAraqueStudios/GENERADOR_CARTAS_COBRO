"""
Modelo de datos de la póliza.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
from datetime import date


class Poliza(BaseModel):
    """
    Representa los datos de la póliza de seguro.
    """
    
    numero: str = Field(
        ..., 
        description="Número de póliza"
    )
    tipo: str = Field(
        default="POLIZA DE VIDA GRUPO",
        description="Tipo de póliza"
    )
    plan_poliza: str = Field(
        default="N/A",
        description="Plan de la póliza"
    )
    documento_referencia: str = Field(
        default="N/A",
        description="Documento de referencia interno"
    )
    cuota_numero: int = Field(
        default=1,
        description="Número de cuota mensual"
    )
    vigencia_inicio: date = Field(
        ...,
        description="Fecha de inicio del período de cobertura"
    )
    vigencia_fin: date = Field(
        ...,
        description="Fecha de fin del período de cobertura"
    )
    
    @field_validator('tipo')
    @classmethod
    def normalize_tipo(cls, v: str) -> str:
        """Retorna el tipo tal cual sin validaciones."""
        return v.strip()
    
    @field_validator('vigencia_fin')
    @classmethod
    def validate_vigencia(cls, v: date, info) -> date:
        """Retorna la fecha tal cual sin validaciones."""
        return v
    
    @property
    def plan_code(self) -> str:
        """Extrae el código de plan del campo plan_poliza."""
        if '  ' in self.plan_poliza:
            return self.plan_poliza.split('  ')[0]
        return "N/A"
    
    @property
    def ramo(self) -> str:
        """Extrae el ramo del tipo de póliza."""
        return self.tipo.replace("POLIZA DE ", "").replace("POLIZA ", "")
    
    def model_dump_for_pdf(self) -> dict:
        """Retorna datos formateados para insertar en el PDF."""
        return {
            "poliza_numero": self.numero,
            "poliza_tipo": self.tipo,
            "poliza_ramo": self.ramo,
            "plan_poliza": self.plan_poliza,
            "plan_code_inferred": self.plan_code,
            "documento_referencia": self.documento_referencia,
            "cuota_numero": self.cuota_numero,
            "vigencia_inicio": self.vigencia_inicio.isoformat(),
            "vigencia_fin": self.vigencia_fin.isoformat()
        }
    
    class Config:
        json_schema_extra = {
            "example": {
                "numero": "3144016",
                "tipo": "POLIZA DE VIDA GRUPO",
                "plan_poliza": "06  3144016",
                "documento_referencia": "21155722",
                "cuota_numero": 5,
                "vigencia_inicio": "2025-09-30",
                "vigencia_fin": "2025-10-30"
            }
        }
