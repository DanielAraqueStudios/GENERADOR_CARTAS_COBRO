"""
Tests para validadores.
"""
import pytest
from validators.field_validators import FieldValidator, CurrencyFormatter, DateFormatter
from datetime import date


def test_validate_nit_valid():
    """Test de NIT válido."""
    is_valid, error = FieldValidator.validate_nit_colombiano("860023108-9")
    assert is_valid
    assert error is None


def test_validate_nit_invalid_check_digit():
    """Test de NIT con dígito verificador inválido."""
    is_valid, error = FieldValidator.validate_nit_colombiano("860023108-5")
    assert not is_valid
    assert "Dígito de verificación incorrecto" in error


def test_validate_telefono_valid():
    """Test de teléfono válido."""
    is_valid, error = FieldValidator.validate_telefono_colombiano("6067676")
    assert is_valid
    assert error is None


def test_validate_telefono_invalid():
    """Test de teléfono inválido."""
    is_valid, error = FieldValidator.validate_telefono_colombiano("123")
    assert not is_valid


def test_currency_formatter():
    """Test de formato de moneda."""
    formatted = CurrencyFormatter.to_colombian_format(1372412.00)
    assert formatted == "1.372.412,00"
    
    parsed = CurrencyFormatter.from_colombian_format("1.372.412,00")
    assert parsed == 1372412.00


def test_date_formatter():
    """Test de formato de fechas."""
    test_date = date(2025, 12, 18)
    
    long_format = DateFormatter.to_long_spanish(test_date)
    assert long_format == "18 de diciembre de 2025"
    
    short_upper = DateFormatter.to_short_upper(test_date)
    assert short_upper == "18-DIC.-2025"
    
    short_lower = DateFormatter.to_short_lower(test_date)
    assert short_lower == "18-dic.-2025"


# TODO: Agregar más tests
