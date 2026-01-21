"""
Demo rápida del sistema de aseguradoras beneficiarias.
"""
from utils.payee_manager import payee_manager

print("=" * 60)
print("SISTEMA DE GESTIÓN DE ASEGURADORAS BENEFICIARIAS")
print("=" * 60)

# Agregar algunas aseguradoras de ejemplo
print("\n1. Agregando aseguradoras de ejemplo...")

payees_ejemplo = [
    ("SEGUROS BOLÍVAR S.A.", "860002503-4"),
    ("POSITIVA COMPAÑÍA DE SEGUROS S.A.", "800235861-9"),
    ("SEGUROS DEL ESTADO S.A.", "860028415-1"),
    ("AXA COLPATRIA SEGUROS S.A.", "860037013-8")
]

for nombre, nit in payees_ejemplo:
    payee = payee_manager.add_payee(nombre, nit)
    print(f"   ✓ {nombre}")

# Listar todas las aseguradoras
print("\n2. Aseguradoras guardadas (ordenadas por uso):")
all_payees = payee_manager.get_all_payees()
for idx, payee in enumerate(all_payees, 1):
    print(f"   {idx}. {payee['name']}")
    print(f"      NIT: {payee['nit']}")
    print(f"      Veces usada: {payee['usage_count']}")

# Simular uso
print("\n3. Incrementando uso de 'SEGUROS BOLÍVAR S.A.'...")
for _ in range(3):
    payee_manager.increment_usage("SEGUROS BOLÍVAR S.A.")

# Buscar aseguradora
print("\n4. Buscando 'SEGUROS BOLÍVAR S.A.':")
payee = payee_manager.get_payee_by_name("SEGUROS BOLÍVAR S.A.")
if payee:
    print(f"   Encontrada: {payee['name']}")
    print(f"   NIT: {payee['nit']}")
    print(f"   Veces usada: {payee['usage_count']}")

# Listar nombres solamente
print("\n5. Nombres disponibles para autocompletado:")
nombres = payee_manager.get_payee_names()
for nombre in nombres[:3]:
    print(f"   - {nombre}")

print("\n" + "=" * 60)
print("Archivo de almacenamiento: logs/payees.json")
print("=" * 60)
