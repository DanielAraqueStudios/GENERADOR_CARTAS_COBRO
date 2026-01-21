# Sistema de Aseguradoras Beneficiarias

## ¿Qué cambió?

Antes, el campo **"VALOR A PAGAR A FAVOR DE"** tenía un texto fijo:
- `SEGUROS DE VIDA SURAMERICANA S.A.` (NIT: 890903790-5)

Ahora, este campo es **editable** y el sistema permite:

### 1. 📝 Escribir el nombre de una nueva aseguradora
Cuando generas una carta de cobro en modo interactivo, puedes ingresar:
- Nombre de la aseguradora
- NIT de la aseguradora

### 2. 💾 Guardar automáticamente
El sistema guarda automáticamente cada aseguradora que ingresas en:
```
logs/payees.json
```

### 3. 🔄 Seleccionar aseguradoras guardadas
La próxima vez que generes una carta:
- Se muestra un listado de aseguradoras guardadas
- Puedes seleccionar una con solo presionar un número
- Las más usadas aparecen primero
- También puedes ingresar una nueva

### 4. ✏️ Editar aseguradoras existentes
Puedes modificar el nombre o NIT de cualquier aseguradora guardada:
- En modo interactivo durante generación de carta
- Usando el menú de gestión: `python cli.py --manage-payees`
- El contador de uso se preserva al editar

### 5. 🗑️ Eliminar aseguradoras
Puedes eliminar aseguradoras que ya no uses:
- En modo interactivo durante generación de carta
- Usando el menú de gestión: `python cli.py --manage-payees`

### 6. 📊 Contador de uso
El sistema lleva un contador de cuántas veces usas cada aseguradora,
mostrándote las más frecuentes primero.

---

## Cómo usar en CLI Interactivo

```bash
python cli.py --interactive
```

Cuando llegues a la sección **"ASEGURADORA BENEFICIARIA"**, verás:

```
🏢 ASEGURADORA BENEFICIARIA (quien recibe el pago)

Aseguradoras guardadas:
1. SEGUROS DE VIDA SURAMERICANA S.A. (NIT: 890903790-5) - Usada 15 veces
2. SEGUROS BOLÍVAR S.A. (NIT: 860002503-4) - Usada 8 veces
3. POSITIVA COMPAÑÍA DE SEGUROS S.A. (NIT: 800235861-9) - Usada 3 veces
4. Ingresar nueva aseguradora
5. Editar aseguradora existente
6. Eliminar aseguradora

Seleccione opción [1-6]: _
```

### Opciones:
- **Presionar 1, 2, o 3**: Selecciona una aseguradora guardada
- **Opción 4**: Ingresa una nueva aseguradora
- **Opción 5**: Edita nombre o NIT de una aseguradora existente
- **Opción 6**: Elimina una aseguradora del catálogo

---

## Menú de Gestión de Aseguradoras

Para gestionar el catálogo completo sin generar cartas:

```bash
python cli.py --manage-payees
```

Este menú permite:
- ➕ Agregar nuevas aseguradoras
- ✏️ Editar aseguradoras existentes (nombre y NIT)
- 🗑️ Eliminar aseguradoras del catálogo
- 📋 Ver detalles completos (con contador de uso)

---

## Cómo usar desde JSON

En tu archivo `ejemplo_carta.json`, ahora incluye:

```json
{
  "ciudad_emision": "Medellín",
  "fecha_emision": "2025-12-18",
  ...
  "payee_company_name": "SEGUROS DE VIDA SURAMERICANA S.A.",
  "payee_company_nit": "890903790-5",
  ...
}
```

Si omites estos campos, se usa el valor por defecto.

---

## Archivo de almacenamiento

Las aseguradoras se guardan en `logs/payees.json`:

```json
{
  "payees": [
    {
      "name": "SEGUROS DE VIDA SURAMERICANA S.A.",
      "nit": "890903790-5",
      "usage_count": 15
    },
    {
      "name": "SEGUROS BOLÍVAR S.A.",
      "nit": "860002503-4",
      "usage_count": 8
    }
  ]
}
```

---

## Gestión programática

También puedes usar `PayeeManager` desde código Python:

```python

# Editar aseguradora
payee_manager.update_payee(
    "SEGUROS SURA S.A.",
    "SEGUROS SURA ACTUALIZADO S.A.",
    "800088702-7"
)

# Eliminar aseguradora
payee_manager.delete_payee("SEGUROS SURA ACTUALIZADO S.A.")
from utils.payee_manager import payee_manager

# Agregar nueva aseguradora
payee_manager.add_payee(
    "SEGUROS SURA S.A.",
    "800088702-7"
)

# Listar todas
payees = payee_manager.get_all_payees()

# Buscar por nombre
payee = payee_manager.get_payee_by_name("SEGUROS SURA S.A.")

# Incrementar uso
payee_manager.increment_usage("SEGUROS SURA S.A.")

# Obtener solo nombres
nombres = payee_manager.get_payee_names()
```

---

## Validación

El campo `payee_company_nit` está validado con el algoritmo DIAN para NITs colombianos,
igual que los otros campos NIT del sistema.

---

## Migración de datos existentes

Si tienes archivos JSON antiguos sin estos campos, el sistema usará los valores por defecto:
- `payee_company_name`: "SEGUROS DE VIDA SURAMERICANA S.A."
- `payee_company_nit`: "890903790-5"

No necesitas actualizar archivos existentes.
