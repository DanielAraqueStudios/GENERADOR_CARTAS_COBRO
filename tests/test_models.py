"""
Tests para el módulo de modelos.
"""
import pytest
from decimal import Decimal
from datetime import date

from models.asegurado import Asegurado
from models.poliza import Poliza
from models.documento import Documento, MontosCobro


def test_asegurado_valid():
    """Test de creación de asegurado válido."""
    asegurado = Asegurado(
        razon_social="COOPERATIVA DEL COMERCIO EXTERIOR COLOMBIANO",
        nit="860023108-9",  # Dígito verificador correcto
        direccion="CR 13 28 01 P 5",
        telefono="6067676",
        ciudad="Bogotá D.C."
    )
    
    assert asegurado.razon_social == "COOPERATIVA DEL COMERCIO EXTERIOR COLOMBIANO"
    assert asegurado.nit == "860023108-9"


def test_asegurado_invalid_nit():
    """Test de NIT inválido."""
    with pytest.raises(ValueError):
        Asegurado(
            razon_social="TEST",
            nit="123456789-5",  # Dígito verificador incorrecto
            direccion="CR 1 1 1",
            telefono="1234567",
            ciudad="Bogotá"
        )


def test_montos_cobro_total():
    """Test de cálculo automático del total."""
    montos = MontosCobro(
        prima=Decimal("1372412.00"),
        otros_rubros=Decimal("50000.00"),
        impuesto=Decimal("10000.00"),
        valor_externo=Decimal("5000.00")
    )
    
    assert montos.total == Decimal("1437412.00")


def test_montos_cobro_format():
    """Test de formato colombiano de moneda."""
    montos = MontosCobro(prima=Decimal("1372412.00"))
    raw = montos.to_raw_format()
    
    assert raw['prima'] == "1.372.412,00"
    assert raw['total'] == "1.372.412,00"


# TODO: Agregar más tests
