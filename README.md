# 📄 Generador de Cartas de Cobro - SEGUROS UNIÓN

Sistema profesional de generación automática de cartas de cobro en formato PDF, diseñado para SEGUROS UNIÓN con interfaz gráfica moderna en dark mode, gestión completa de aseguradoras y generación de ejecutables standalone.

## 🎯 Objetivo del Proyecto

Automatizar la generación de cartas de cobro personalizadas con:
- **Interfaz gráfica moderna** (PyQt6 Dark Mode) para captura de datos
- **Gestión de aseguradoras** con sistema CRUD completo
- **Validación flexible** de datos del asegurado y póliza (adaptado a datos reales)
- **Generación PDF profesional** con formato legal colombiano (ReportLab)
- **Selección de carpeta de salida** para organizar archivos
- **Ejecutable standalone** (.exe) listo para distribución
- **Trazabilidad completa** con registro de auditoría

## 🏗️ Arquitectura del Sistema

```
┌──────────────────────┐
│   GUI Simple (PyQt6) │  ← Interfaz Dark Mode en un solo archivo
│   - Tabs organizadas │  ← 3 sub-tabs para formulario extenso
│   - CRUD Aseguradoras│  ← Gestión completa inline
│   - Selector carpeta │  ← Configurar destino de PDFs
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│  Modelos Pydantic    │  ← Validación flexible de datos
│  - Asegurado         │  ← NIT, dirección, teléfono
│  - Poliza            │  ← Número flexible, tipos normalizados
│  - Documento         │  ← Carta completa con metadatos
│  - MontosCobro       │  ← Prima, IVA, otros, total calculado
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│  Generadores PDF     │  ← ReportLab con formato legal
│  - CartaCobro        │  ← Headers, tablas, firmas
│  - BaseGenerator     │  ← Clase abstracta reutilizable
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│  Utils / Managers    │  ← Servicios auxiliares
│  - PayeeManager      │  ← CRUD aseguradoras (JSON)
│  - Logger            │  ← Auditoría completa
│  - Config            │  ← Configuración global
└──────────────────────┘
```

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.10+** - Lenguaje principal
- **ReportLab 4.0+** - Generación de PDFs con control preciso de diseño
- **Pydantic 2.0+** - Validación de datos y modelos
- **Threading** - Operaciones no bloqueantes en GUI

### Frontend
- **PyQt6 6.6+** - Interfaz gráfica profesional
- **Qt Designer** - Diseño visual de formularios

### Utilidades
- **JSON** - Configuración de plantillas
- **Logging** - Registro de auditoría
- **pathlib** - Manejo de rutas multiplataforma

## 📂 Estructura de Archivos

```
GENERADOR_CARTAS_COBRO/
│
├── templates/                  # Plantillas de documentos (JSON)
│   ├── carta_cobro_primera.json
│   ├── carta_cobro_segunda.json
│   ├── carta_cobro_judicial.json
│   └── template_schema.json
│
├── generators/                 # Generadores PDF por tipo de documento
│   ├── __init__.py
│   ├── base_generator.py      # Clase base abstracta
│   ├── carta_cobro_generator.py
│   └── pdf_components.py      # Componentes reutilizables (headers, footers)
│
├── gui/                        # Interfaz gráfica PyQt6
│   ├── __init__.py
│   ├── main_window.py         # Ventana principal
│   ├── form_builder.py        # Auto-generador de formularios
│   ├── preview_dialog.py      # Vista previa del documento
│   └── ui/                    # Archivos .ui de Qt Designer
│
├── validators/                 # Sistema de validación
│   ├── __init__.py
│   ├── field_validators.py    # Validadores de campos individuales
│   └── business_rules.py      # Reglas de negocio (póliza, montos)
│
├── models/                     # Modelos de datos Pydantic
│   ├── __init__.py
│   ├── asegurado.py
│   ├── poliza.py
│   └── documento.py
│
├── utils/                      # Utilidades
│   ├── __init__.py
│   ├── logger.py              # Sistema de logging
│   ├── versioning.py          # Control de versiones
│   └── config.py              # Configuración global
│
├── output/                     # PDFs generados
│   ├── cartas/                # Cartas finales
│   └── borradores/            # Borradores (watermark)
│
├── logs/                       # Registros de auditoría
│   └── audit_trail.log
│
├── tests/                      # Tests unitarios
│   ├── test_validators.py
│   ├── test_generators.py
│   └── test_templates.py
│
├── main.py                     # Punto de entrada GUI
├── cli.py                      # Interfaz CLI alternativa
├── requirements.txt            # Dependencias Python
└── README.md                   # Este archivo
```

## 🚀 Instalación y Uso

### 1. Configurar Entorno Virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

#### Modo GUI (interfaz gráfica)
```powershell
python main.py
```
*Nota: GUI en desarrollo. Actualmente disponible solo CLI.*

#### Modo CLI Interactivo (recomendado)
```powershell
python cli.py --interactive
```
El modo interactivo te guía paso a paso para:
- Ingresar datos del cliente y póliza
- **Seleccionar o ingresar nueva aseguradora beneficiaria**
- Definir montos de cobro
- Generar PDF automáticamente

#### Modo CLI desde JSON
```powershell
# Generar desde archivo JSON
python cli.py --from-json ejemplo_carta.json

# Mostrar estadísticas
python cli.py --stats
```

### 3. Gestión de Aseguradoras Beneficiarias 🏢

El sistema permite gestionar las aseguradoras que reciben el pago:

#### Menú de Gestión Completo:
```powershell
python cli.py --manage-payees
```
Este menú te permite:
- ➕ **Agregar** nuevas aseguradoras al catálogo
- ✏️ **Editar** nombre y NIT de aseguradoras existentes
- 🗑️ **Eliminar** aseguradoras que ya no uses
- 📋 **Ver detalles** con contador de uso

#### En Modo Interactivo:
Cuando llegues a la sección "ASEGURADORA BENEFICIARIA", verás:
```
Aseguradoras guardadas:
1. SEGUROS DE VIDA SURAMERICANA S.A. (NIT: 890903790-5) - Usada 15 veces
2. SEGUROS BOLÍVAR S.A. (NIT: 860002503-4) - Usada 8 veces
3. Ingresar nueva aseguradora
4. Editar aseguradora existente
5. Eliminar aseguradora

Seleccione opción [1-5]: _
```

- **Selecciona un número**: Usa una aseguradora guardada
- **Opción "Ingresar nueva"**: Agrega una nueva al catálogo
- **Opción "Editar"**: Modifica nombre o NIT de una existente
- **Opción "Eliminar"**: Elimina del catálogo
- Las más usadas aparecen primero

#### En archivos JSON:
```json
{
  "payee_company_name": "SEGUROS DE VIDA SURAMERICANA S.A.",
  "payee_company_nit": "890903790-5"
}
```

Las aseguradoras se guardan automáticamente en `logs/payees.json` con contador de uso.

Ver [DEMO_ASEGURADORAS.md](DEMO_ASEGURADORAS.md) para más detalles.

### 4. Crear Nueva Plantilla

```json
{
  "template_id": "carta_cobro_primera",
  "version": "1.0",
  "document_type": "Carta de Cobro - Primera Notificación",
  "fields": [
    {
      "id": "asegurado_nombre",
      "label": "Nombre del Asegurado",
      "type": "text",
      "required": true,
      "validation": "nombre_completo"
    },
    {
      "id": "poliza_numero",
      "label": "Número de Póliza",
      "type": "text",
      "required": true,
      "validation": "poliza_format",
      "pattern": "^POL-\\d{8}$"
    },
    {
      "id": "deuda_total",
      "label": "Deuda Total",
      "type": "currency",
      "required": true,
      "validation": "positive_amount"
    }
  ],
  "sections": [
    {
      "type": "header",
      "content": "SEGUROS UNIÓN - Departamento de Cobros"
    },
    {
      "type": "body",
      "paragraphs": [
        "Estimado/a {asegurado_nombre},",
        "Por medio de la presente, le notificamos que su póliza número {poliza_numero} presenta un saldo pendiente de {deuda_total}.",
        "Le rogamos regularice su situación en un plazo máximo de 15 días hábiles."
      ]
    },
    {
      "type": "signature",
      "position": "Departamento de Cobros",
      "company": "SEGUROS UNIÓN"
    }
  ]
}
```

## 📋 Características Principales

### ✅ Sistema de Plantillas
- **JSON configurables**: Define estructura sin tocar código
- **Recarga en caliente**: Cambios de plantilla sin reiniciar
- **Validación de esquema**: Asegura integridad de plantillas

### ✅ Validación Inteligente
- **Validación en tiempo real**: Feedback inmediato en formularios
- **Reglas de negocio**: Validación de números de póliza, NIFs, montos
- **Validación cruzada**: Comprobaciones entre múltiples campos

### ✅ Generación PDF Profesional
- **Formato legal**: Márgenes, tipografía y espaciado según normativa
- **Elementos estructurados**: Headers, cláusulas numeradas, firmas
- **Marca de agua**: BORRADOR/CONFIDENCIAL según estado
- **Metadatos**: Autor, fecha, versión embebidos

### ✅ Trazabilidad y Auditoría
- **Registro completo**: Timestamp, usuario, plantilla, versión
- **Control de versiones**: Histórico de documentos generados
- **Logs detallados**: Acciones, errores, cambios de estado

### ✅ Interfaz Profesional
- **Diseño claro**: Alto contraste, fuentes legibles
- **Navegación por teclado**: Accesibilidad completa
- **Vista previa**: Revisar documento antes de generar
- **Feedback visual**: Indicadores de progreso y validación

## 🔐 Cumplimiento Legal

### Elementos Obligatorios
Todas las cartas incluyen:
- **Identificación de la compañía**: Logo, CIF, domicilio social
- **Fecha de emisión**: Formato legal dd/mm/yyyy
- **Identificación del destinatario**: Nombre completo, DNI/NIF
- **Número de referencia**: Código único de documento
- **Cláusulas numeradas**: Términos y condiciones claros
- **Plazos**: Fechas límite explícitas
- **Pie legal**: Protección de datos (LOPD/RGPD)

### Registro de Auditoría
Cada documento generado registra:
```python
{
    "timestamp": "2026-01-20T14:30:00Z",
    "user": "usuario.cobros",
    "template": "carta_cobro_primera",
    "template_version": "1.0",
    "document_id": "CART-2026-0001",
    "recipient_nif": "12345678Z",
    "poliza": "POL-20240001",
    "status": "FINAL",
    "output_path": "./output/cartas/CART-2026-0001.pdf"
}
```

## 🧪 Testing

```powershell
# Ejecutar todos los tests
pytest tests/

# Tests con cobertura
pytest --cov=generators --cov=validators tests/

# Test específico
pytest tests/test_generators.py::test_carta_cobro_primera
```

## 📦 Empaquetado

```powershell
# Generar ejecutable con PyInstaller
pyinstaller --onefile --windowed --name "GeneradorCartas" main.py

# El ejecutable estará en dist/GeneradorCartas.exe
```

## 🤝 Contribución

### Workflow de Desarrollo
1. **Definir nueva plantilla** en `templates/` (JSON)
2. **Crear generador** en `generators/` si es necesario
3. **Actualizar validadores** en `validators/` para nuevos campos
4. **Probar** con `pytest`
5. **Documentar** cambios en este README

### Convenciones de Código
- **PEP 8** para estilo Python
- **Type hints** en todas las funciones
- **Docstrings** en formato Google
- **Nombres en español** para variables de dominio (asegurado, poliza)
- **Nombres en inglés** para conceptos técnicos (generator, validator)

## 📞 Soporte

**Proyecto**: Automatizaciones - SEGUROS UNIÓN  
**Departamento**: Tecnología  
**Última actualización**: Enero 2026

---

**Nota**: Este sistema es de uso interno exclusivo de SEGUROS UNIÓN. Los datos procesados están protegidos según LOPD/RGPD.
