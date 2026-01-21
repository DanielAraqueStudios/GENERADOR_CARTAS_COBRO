"""
Modelo de datos del documento (carta de cobro completa).
"""
from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Optional, Literal
from datetime import date, datetime
from decimal import Decimal

from .asegurado import Asegurado
from .poliza import Poliza


class MontosCobro(BaseModel):
    """
    Representa los montos del cobro en formato normalizado y raw.
    """
    
    prima: Decimal = Field(..., ge=0, decimal_places=2)
    otros_rubros: Decimal = Field(default=Decimal('0.00'), ge=0, decimal_places=2)
    impuesto: Decimal = Field(default=Decimal('0.00'), ge=0, decimal_places=2)
    valor_externo: Decimal = Field(default=Decimal('0.00'), ge=0, decimal_places=2)
    
    @computed_field
    @property
    def total(self) -> Decimal:
        """Calcula el total automáticamente."""
        return self.prima + self.otros_rubros + self.impuesto + self.valor_externo
    
    def to_raw_format(self) -> dict[str, str]:
        """Convierte los montos a formato colombiano (punto miles, coma decimales)."""
        def format_cop(value: Decimal) -> str:
            # Formato: 1.372.412,00
            formatted = f"{value:,.2f}"
            return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        return {
            "prima": format_cop(self.prima),
            "otros_rubros": format_cop(self.otros_rubros),
            "impuesto": format_cop(self.impuesto),
            "valor_externo": format_cop(self.valor_externo),
            "total": format_cop(self.total)
        }


class Documento(BaseModel):
    """
    Representa una carta de cobro completa con todos sus datos.
    """
    
    # Metadatos del documento
    ciudad_emision: str = Field(default="Medellín", description="Ciudad donde se emite la carta")
    fecha_emision: date = Field(default_factory=date.today, description="Fecha de emisión")
    numero_carta: str = Field(..., description="Número de la carta (formato: 15434 - 2025)")
    mes_cobro: Literal[
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ] = Field(..., description="Mes al que corresponde el cobro")
    fecha_limite_pago: date = Field(..., description="Fecha límite para realizar el pago")
    
    # Datos del cliente
    asegurado: Asegurado
    
    # Datos de la póliza
    poliza: Poliza
    
    # Montos del cobro
    montos: MontosCobro
    
    # Aseguradora beneficiaria (quien recibe el pago)
    payee_company_name: str = Field(
        default="SEGUROS DE VIDA SURAMERICANA S.A.",
        min_length=1,
        description="Nombre de la aseguradora que recibe el pago"
    )
    payee_company_nit: str = Field(
        default="890903790-5",
        min_length=1,
        description="NIT de la aseguradora beneficiaria"
    )
    
    # Firma
    firmante_nombre: str = Field(..., min_length=1, max_length=60)
    firmante_cargo: str = Field(..., min_length=1, max_length=50)
    firmante_iniciales: Optional[str] = Field(default=None, max_length=10)
    
    # Estado del documento
    es_borrador: bool = Field(default=False, description="Si es True, se marca como BORRADOR")
    
    @field_validator('firmante_nombre')
    @classmethod
    def uppercase_firmante(cls, v: str) -> str:
        """Convierte el nombre del firmante a mayúsculas."""
        return v.upper().strip()
    
    @field_validator('numero_carta')
    @classmethod
    def validate_numero_carta(cls, v: str) -> str:
        """Valida el formato del número de carta."""
        import re
        if not re.match(r'^\d+ - \d{4}$', v):
            raise ValueError("Número de carta debe tener formato: 15434 - 2025")
        return v
    
    @computed_field
    @property
    def numero_carta_normalized(self) -> str:
        """Número de carta sin espacios alrededor del guión."""
        return self.numero_carta.replace(' - ', '-')
    
    def format_fecha_emision(self) -> str:
        """Formatea la fecha de emisión al formato español largo."""
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        return f"{self.fecha_emision.day} de {meses[self.fecha_emision.month - 1]} de {self.fecha_emision.year}"
    
    def format_fecha_limite(self) -> str:
        """Formatea la fecha límite al formato español corto."""
        meses_cortos = {
            1: "ene.", 2: "feb.", 3: "mar.", 4: "abr.", 5: "may.", 6: "jun.",
            7: "jul.", 8: "ago.", 9: "sept.", 10: "oct.", 11: "nov.", 12: "dic."
        }
        return f"{self.fecha_limite_pago.day}-{meses_cortos[self.fecha_limite_pago.month]}-{self.fecha_limite_pago.year}"
    
    def format_vigencia(self, fecha: date, uppercase: bool = True) -> str:
        """Formatea fechas de vigencia."""
        meses = {
            1: "ENE.", 2: "FEB.", 3: "MAR.", 4: "ABR.", 5: "MAY.", 6: "JUN.",
            7: "JUL.", 8: "AGO.", 9: "SEPT.", 10: "OCT.", 11: "NOV.", 12: "DIC."
        }
        mes = meses[fecha.month] if uppercase else meses[fecha.month].lower()
        return f"{fecha.day}-{mes}-{fecha.year}"
    
    def to_pdf_data(self) -> dict:
        """Genera el diccionario completo de datos para el PDF."""
        return {
            # Metadatos
            "ciudad_emision": self.ciudad_emision,
            "fecha_emision": self.format_fecha_emision(),
            "numero_carta": self.numero_carta,
            "mes_cobro": self.mes_cobro,
            "fecha_limite_pago": self.format_fecha_limite(),
            
            # Cliente
            **self.asegurado.model_dump_for_pdf(),
            
            # Póliza
            **self.poliza.model_dump_for_pdf(),
            "vigencia_inicio_text": self.format_vigencia(self.poliza.vigencia_inicio, uppercase=True),
            "vigencia_fin_text": self.format_vigencia(self.poliza.vigencia_fin, uppercase=True),
            
            # Montos
            "amounts_raw": self.montos.to_raw_format(),
            "amounts_normalized": {
                "currency": "COP",
                "prima": float(self.montos.prima),
                "otros_rubros": float(self.montos.otros_rubros),
                "impuesto": float(self.montos.impuesto),
                "valor_externo": float(self.montos.valor_externo),
                "total": float(self.montos.total)
            },
            
            # Aseguradora beneficiaria
            "payee_company_name": self.payee_company_name,
            "payee_company_nit": self.payee_company_nit,
            
            # Firma
            "firmante_nombre": self.firmante_nombre,
            "firmante_cargo": self.firmante_cargo,
            "firmante_iniciales": self.firmante_iniciales or "",
            
            # Estado
            "es_borrador": self.es_borrador,
            
            # Datos estáticos (de configuración)
            "sender_company_name": "SEGUROS UNIÓN",
            "sender_email": "gerencia@segurosunion.com",
            "sender_address": "Carrera 77 A # 49 - 37 .Sector Estadio - Medellin"
        }
    
    class Config:
        json_schema_extra = {
            "example": {
                "ciudad_emision": "Medellín",
                "fecha_emision": "2025-12-18",
                "numero_carta": "15434 - 2025",
                "mes_cobro": "Octubre",
                "fecha_limite_pago": "2025-12-23",
                "asegurado": {
                    "razon_social": "COOPERATIVA DEL COMERCIO EXTERIOR COLOMBIANO",
                    "nit": "860023108-6",
                    "direccion": "CR 13 28 01 P 5",
                    "telefono": "6067676",
                    "ciudad": "Bogotá D.C."
                },
                "poliza": {
                    "numero": "3144016",
                    "tipo": "POLIZA DE VIDA GRUPO",
                    "plan_poliza": "06  3144016",
                    "documento_referencia": "21155722",
                    "cuota_numero": 5,
                    "vigencia_inicio": "2025-09-30",
                    "vigencia_fin": "2025-10-30"
                },
                "montos": {
                    "prima": 1372412.00,
                    "otros_rubros": 0.00,
                    "impuesto": 0.00,
                    "valor_externo": 0.00
                },
                "firmante_nombre": "YULIANA ANDREA VELASQUEZ VALENCI",
                "firmante_cargo": "Ejecutivo",
                "firmante_iniciales": "YAVV",
                "es_borrador": False
            }
        }
