"""
Tests para PayeeManager (gestor de aseguradoras beneficiarias).
"""
import pytest
from pathlib import Path
import tempfile
import json
from utils.payee_manager import PayeeManager


@pytest.fixture
def temp_storage():
    """Crea un archivo temporal para pruebas."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = Path(f.name)
    yield temp_path
    if temp_path.exists():
        temp_path.unlink()


def test_payee_manager_init_creates_default(temp_storage):
    """Verifica que se crea aseguradora por defecto."""
    manager = PayeeManager(storage_file=temp_storage)
    
    payees = manager.get_all_payees()
    assert len(payees) == 1
    assert payees[0]['name'] == "SEGUROS DE VIDA SURAMERICANA S.A."
    assert payees[0]['nit'] == "890903790-5"
    assert payees[0]['usage_count'] == 0


def test_add_new_payee(temp_storage):
    """Verifica que se puede agregar una nueva aseguradora."""
    manager = PayeeManager(storage_file=temp_storage)
    
    payee = manager.add_payee("SEGUROS BOLÍVAR S.A.", "860002503-4")
    
    assert payee['name'] == "SEGUROS BOLÍVAR S.A."
    assert payee['nit'] == "860002503-4"
    assert payee['usage_count'] == 1
    
    all_payees = manager.get_all_payees()
    assert len(all_payees) == 2


def test_add_existing_payee_updates_usage(temp_storage):
    """Verifica que agregar aseguradora existente incrementa uso."""
    manager = PayeeManager(storage_file=temp_storage)
    
    # Primera vez
    manager.add_payee("SEGUROS BOLÍVAR S.A.", "860002503-4")
    # Segunda vez
    payee = manager.add_payee("SEGUROS BOLÍVAR S.A.", "860002503-4")
    
    assert payee['usage_count'] == 2
    assert len(manager.get_all_payees()) == 2  # No duplicado


def test_get_payee_by_name(temp_storage):
    """Verifica búsqueda por nombre."""
    manager = PayeeManager(storage_file=temp_storage)
    manager.add_payee("SEGUROS BOLÍVAR S.A.", "860002503-4")
    
    # Búsqueda exacta
    payee = manager.get_payee_by_name("SEGUROS BOLÍVAR S.A.")
    assert payee is not None
    assert payee['nit'] == "860002503-4"
    
    # Búsqueda case-insensitive
    payee = manager.get_payee_by_name("seguros bolívar s.a.")
    assert payee is not None
    
    # No encontrada
    payee = manager.get_payee_by_name("NO EXISTE")
    assert payee is None


def test_increment_usage(temp_storage):
    """Verifica incremento de contador de uso."""
    manager = PayeeManager(storage_file=temp_storage)
    manager.add_payee("SEGUROS BOLÍVAR S.A.", "860002503-4")
    
    manager.increment_usage("SEGUROS BOLÍVAR S.A.")
    manager.increment_usage("SEGUROS BOLÍVAR S.A.")
    
    payee = manager.get_payee_by_name("SEGUROS BOLÍVAR S.A.")
    assert payee['usage_count'] == 3  # 1 del add + 2 incrementos


def test_payees_sorted_by_usage(temp_storage):
    """Verifica que las aseguradoras se ordenan por uso."""
    manager = PayeeManager(storage_file=temp_storage)
    
    manager.add_payee("ASEGURADORA A", "111111111-1")
    manager.add_payee("ASEGURADORA B", "222222222-2")
    manager.add_payee("ASEGURADORA C", "333333333-3")
    
    # Incrementar uso de C
    for _ in range(5):
        manager.increment_usage("ASEGURADORA C")
    
    # Incrementar uso de A
    for _ in range(3):
        manager.increment_usage("ASEGURADORA A")
    
    payees = manager.get_all_payees()
    assert payees[0]['name'] == "ASEGURADORA C"  # Más usada
    assert payees[1]['name'] == "ASEGURADORA A"
    assert payees[2]['name'] == "ASEGURADORA B"


def test_get_payee_names(temp_storage):
    """Verifica obtención de lista de nombres."""
    manager = PayeeManager(storage_file=temp_storage)
    
    manager.add_payee("ASEGURADORA A", "111111111-1")
    manager.add_payee("ASEGURADORA B", "222222222-2")
    
    nombres = manager.get_payee_names()
    assert len(nombres) == 3  # 2 agregadas + 1 por defecto
    assert "ASEGURADORA A" in nombres
    assert "ASEGURADORA B" in nombres


def test_persistence(temp_storage):
    """Verifica que los datos se persisten en el archivo."""
    manager1 = PayeeManager(storage_file=temp_storage)
    manager1.add_payee("SEGUROS BOLÍVAR S.A.", "860002503-4")
    
    # Crear nueva instancia (debería cargar del archivo)
    manager2 = PayeeManager(storage_file=temp_storage)
    payees = manager2.get_all_payees()
    
    assert len(payees) == 2  # Default + agregada
    payee = manager2.get_payee_by_name("SEGUROS BOLÍVAR S.A.")
    assert payee is not None


def test_uppercase_normalization(temp_storage):
    """Verifica que los nombres se normalizan a mayúsculas."""
    manager = PayeeManager(storage_file=temp_storage)
    
    payee = manager.add_payee("seguros bolívar s.a.", "860002503-4")
    
    assert payee['name'] == "SEGUROS BOLÍVAR S.A."


def test_delete_payee(temp_storage):
    """Verifica que se puede eliminar una aseguradora."""
    manager = PayeeManager(storage_file=temp_storage)
    manager.add_payee("SEGUROS BOLÍVAR S.A.", "860002503-4")
    manager.add_payee("POSITIVA S.A.", "800235861-9")
    
    # Verificar que existe
    assert len(manager.get_all_payees()) == 3  # Default + 2 agregadas
    
    # Eliminar
    result = manager.delete_payee("SEGUROS BOLÍVAR S.A.")
    assert result is True
    assert len(manager.get_all_payees()) == 2
    
    # Verificar que no existe
    payee = manager.get_payee_by_name("SEGUROS BOLÍVAR S.A.")
    assert payee is None
    
    # Intentar eliminar inexistente
    result = manager.delete_payee("NO EXISTE")
    assert result is False


def test_delete_payee_case_insensitive(temp_storage):
    """Verifica que delete es case-insensitive."""
    manager = PayeeManager(storage_file=temp_storage)
    manager.add_payee("SEGUROS BOLÍVAR S.A.", "860002503-4")
    
    result = manager.delete_payee("seguros bolívar s.a.")
    assert result is True
    assert manager.get_payee_by_name("SEGUROS BOLÍVAR S.A.") is None


def test_update_payee(temp_storage):
    """Verifica que se puede actualizar una aseguradora."""
    manager = PayeeManager(storage_file=temp_storage)
    manager.add_payee("SEGUROS BOLÍVAR S.A.", "860002503-4")
    
    # Actualizar nombre y NIT
    updated = manager.update_payee(
        "SEGUROS BOLÍVAR S.A.",
        "SEGUROS BOLÍVAR ACTUALIZADO S.A.",
        "111111111-1"
    )
    
    assert updated is not None
    assert updated['name'] == "SEGUROS BOLÍVAR ACTUALIZADO S.A."
    assert updated['nit'] == "111111111-1"
    
    # Verificar que el viejo nombre no existe
    old_payee = manager.get_payee_by_name("SEGUROS BOLÍVAR S.A.")
    assert old_payee is None
    
    # Verificar que el nuevo nombre existe
    new_payee = manager.get_payee_by_name("SEGUROS BOLÍVAR ACTUALIZADO S.A.")
    assert new_payee is not None


def test_update_payee_not_found(temp_storage):
    """Verifica que update retorna None si no encuentra la aseguradora."""
    manager = PayeeManager(storage_file=temp_storage)
    
    result = manager.update_payee("NO EXISTE", "NUEVO NOMBRE", "111111111-1")
    assert result is None


def test_update_payee_preserves_usage_count(temp_storage):
    """Verifica que update preserva el contador de uso."""
    manager = PayeeManager(storage_file=temp_storage)
    manager.add_payee("SEGUROS BOLÍVAR S.A.", "860002503-4")
    
    # Incrementar uso
    for _ in range(5):
        manager.increment_usage("SEGUROS BOLÍVAR S.A.")
    
    # Actualizar
    manager.update_payee(
        "SEGUROS BOLÍVAR S.A.",
        "SEGUROS BOLÍVAR NUEVO",
        "111111111-1"
    )
    
    # Verificar que el contador se preservó
    updated_payee = manager.get_payee_by_name("SEGUROS BOLÍVAR NUEVO")
    assert updated_payee['usage_count'] == 6  # 1 del add + 5 incrementos


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
