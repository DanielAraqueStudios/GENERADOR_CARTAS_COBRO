# 📄 Generador de Cartas de Cobro - SEGUROS UNIÓN

Sistema profesional de generación automática de cartas de cobro en formato PDF, diseñado para SEGUROS UNIÓN con interfaz gráfica moderna en dark mode, gestión completa de aseguradoras y generación de ejecutables standalone.

## � Novedades de esta Versión

### ✨ Mejoras en Gestión de Pólizas

#### **Sistema de Montos Independientes por Póliza**
- ✅ Cada póliza ahora tiene sus propios montos (Prima, IVA, Otros Rubros)
- ✅ El total general se calcula automáticamente sumando todas las pólizas activas
- ✅ Checkboxes individuales para controlar qué montos se incluyen por póliza

#### **Cálculo Automático de IVA**
- ✅ Selector de porcentaje de IVA: **19%** o **5%**
- ✅ Cálculo automático basado en el valor de la Prima
- ✅ Fórmula: `IVA = Prima × Porcentaje seleccionado`
- ✅ Se recalcula al cambiar la prima o el porcentaje
- ✅ Sigue siendo editable manualmente si es necesario

#### **Botón Modificar Póliza**
- ✅ Permite editar pólizas existentes en la tabla
- ✅ Similar al botón "Modificar Aseguradora"
- ✅ Carga todos los datos actuales para modificación

#### **Gestión de Descripciones**
- ✅ Campo "Descripción" ahora es un combobox editable
- ✅ Guarda automáticamente descripciones nuevas
- ✅ Botón ⚙️ para abrir administrador de descripciones
- ✅ **Administrador completo**: Agregar, Editar, Eliminar descripciones
- ✅ Persistencia en `logs/descripciones.json`
- ✅ 5 descripciones predefinidas incluidas

### 📋 Mejoras en Presentación de PDF

#### **Formato de Tabla Optimizado**
- ✅ Columnas: Ramo, Descripción, Doc. (eliminadas fechas de vigencia)
- ✅ Cada fila muestra montos individuales de la póliza
- ✅ Columna "Total" por póliza
- ✅ Descripción solo se muestra si checkbox está activo

#### **Link de Pago Mejorado**
- ✅ Ahora aparece como **hipervínculo azul clickeable**
- ✅ Auto-agrega "https://" si no está presente
- ✅ Formato: "PUEDE REALIZAR SUS PAGOS POR PSE EN LA PAGINA WEB [link]"

#### **Sección ASUNTO Simplificada**
- ✅ Eliminado nombre del cliente (evita duplicación)
- ✅ Solo muestra: Tipo de póliza y número

#### **Sección Destinatario Optimizada**
- ✅ Eliminada dirección del cliente
- ✅ Muestra: Señores, Nombre, Ciudad, NIT

#### **Detalle de Pago Simplificado**
- ✅ Eliminada línea "CUOTA MENSUAL N° X VIGENCIA..."
- ✅ Solo muestra: "VALOR A PAGAR A FAVOR DE..." y el monto total

#### **Campo Retorno Opcional**
- ✅ Nuevo campo editable "Retorno"
- ✅ Checkbox para incluir/excluir del PDF
- ✅ Aparece debajo del valor a pagar si está activo
- ✅ Ejemplo: "RETORNO: Retorno a cuenta de ahorros del titular"

#### **Footer Centrado**
- ✅ Dirección y email ahora están **centrados**
- ✅ Mejor presentación profesional del documento

### 🏢 Base de Datos de Aseguradoras

#### **24 Aseguradoras Colombianas Precargadas**
- ✅ Seguros Bolívar, Seguros del Estado, Mapfre, Liberty, Allianz
- ✅ AXA Colpatria, Chubb, Zurich, Equidad, Previsora
- ✅ HDI, SBS, MetLife, Positiva, Aseguradora Solidaria
- ✅ Y más... (ver lista completa en `utils/payee_manager.py`)
- ✅ Incluye NITs y enlaces de pago verificados

### 🔓 Validaciones Flexibles

#### **Sin Restricciones de Formato**
- ✅ **NIT**: Acepta cualquier formato (no solo colombiano)
- ✅ **Teléfono**: Acepta letras, guiones, espacios, cualquier formato
- ✅ **Números**: Sin límites de longitud
- ✅ **Montos**: Permite valores negativos si es necesario
- ✅ **Fechas**: Sin validación de orden (vigencia_fin puede ser antes de inicio)
- ✅ **Textos**: Sin límites de caracteres en ningún campo

#### **Validación Mínima**
- ⚠️ Solo verifica que campos obligatorios no estén vacíos
- ⚠️ Números deben ser valores numéricos válidos

### 🎨 Mejoras de Interfaz

#### **Tabla de Pólizas Actualizada**
- 7 columnas: Número, Tipo, Descripción, Prima, IVA, Otros, Total
- Muestra "-" para campos desactivados
- Resaltado de fila seleccionada

#### **Diálogos Mejorados**
- Diálogo de póliza con selector de IVA integrado
- Administrador de descripciones con tabla y CRUD completo
- Botones con iconos y colores distintivos

## �🎯 Objetivo del Proyecto

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
- **Python 3.13.2** - Lenguaje principal
- **ReportLab 4.0+** - Generación de PDFs con control preciso de diseño
- **Pydantic 2.0+** - Validación flexible de datos y modelos
- **PyInstaller 6.18+** - Empaquetado de ejecutables standalone

### Frontend
- **PyQt6 6.6+** - Interfaz gráfica moderna con Dark Mode
- **QSS (Qt Style Sheets)** - Diseño personalizado con gradientes

### Utilidades
- **JSON** - Persistencia de aseguradoras y configuración
- **Logging** - Registro de auditoría completo
- **pathlib** - Manejo de rutas multiplataforma

### Validación Colombia
- **Algoritmo DIAN** - Validación de dígito verificador NIT
- **Formato moneda COP** - 1.372.412,00 (punto miles, coma decimales)
- **Validación teléfonos** - Formato colombiano 10 dígitos

## 📂 Estructura de Archivos

```
GENERADOR_CARTAS_COBRO/
│
├── gui_simple.py               # 🎨 GUI PRINCIPAL - Un solo archivo (~1200 líneas)
│                               #    - Interfaz Dark Mode completa
│                               #    - 3 sub-tabs organizadas
│                               #    - CRUD aseguradoras inline
│                               #    - Selección carpeta salida
│
├── build_exe.py                # 🔨 Script de construcción de .exe
│                               #    - Instala PyInstaller automáticamente
│                               #    - Limpia builds anteriores
│                               #    - Crea ejecutable + paquete portable
│
├── generators/                 # 📄 Generadores PDF por tipo de documento
│   ├── __init__.py
│   ├── base_generator.py      # Clase base abstracta
│   ├── carta_cobro_generator.py  # Generador de cartas de cobro
│   └── pdf_components.py      # Componentes reutilizables (headers, footers)
│
├── models/                     # 🗂️ Modelos de datos Pydantic
│   ├── __init__.py
│   ├── asegurado.py           # Modelo de cliente (validación NIT DIAN)
│   ├── poliza.py              # Modelo de póliza (validación flexible)
│   └── documento.py           # Modelo de documento completo + MontosCobro
│
├── utils/                      # 🛠️ Utilidades
│   ├── __init__.py
│   ├── payee_manager.py       # 🏢 GESTOR DE ASEGURADORAS (CRUD + JSON)
│   ├── logger.py              # Sistema de logging
│   ├── validators.py          # Validadores colombianos (NIT, teléfono)
│   └── config.py              # Configuración global
│
├── templates/                  # 📋 Plantillas de documentos (JSON)
│   ├── carta_cobro_primera.json
│   └── template_schema.json
│
├── output/                     # 📦 PDFs generados (carpeta por defecto)
│   └── *.pdf                  # Cartas generadas
│
├── logs/                       # 📊 Registros
│   ├── payees.json            # Base de datos de aseguradoras
│   └── *.log                  # Logs de auditoría
│
├── tests/                      # ✅ Tests unitarios
│   ├── test_payee_manager.py  # 14 tests - gestión aseguradoras
│   ├── test_validators.py
│   └── test_generators.py
│
├── dist/                       # 🚀 Ejecutable compilado
│   └── GeneradorCartasCobro.exe  # 45.48 MB - standalone
│
├── GeneradorCartasCobro_Portable/  # 📦 PAQUETE PORTABLE COMPLETO
│   ├── GeneradorCartasCobro.exe    # Ejecutable
│   ├── output/                     # Carpeta para PDFs
│   ├── logs/                       # Carpeta para logs
│   └── LEEME.txt                   # Instrucciones de uso
│
├── main.py                     # 🎯 Punto de entrada GUI
├── cli.py                      # 💻 Interfaz CLI alternativa
├── requirements.txt            # 📋 Dependencias Python
└── README.md                   # 📖 Este archivo
```

## 🚀 Instalación y Uso

### Opción 1: Ejecutable Standalone (RECOMENDADO) 🎯

**Para usuarios finales - Sin necesidad de Python:**

1. **Descargar** el paquete `GeneradorCartasCobro_Portable`
2. **Extraer** en cualquier carpeta
3. **Ejecutar** `GeneradorCartasCobro.exe`
4. ¡Listo! La interfaz se abre automáticamente

**Características del ejecutable:**
- ✅ 45.48 MB - Todo incluido en un solo .exe
- ✅ Sin instalación - Portable
- ✅ Sin dependencias - Python embebido
- ✅ Carpetas automáticas - output/ y logs/

---

### Opción 2: Desde Código Fuente (Desarrollo) 💻

#### 1. Configurar Entorno Virtual

```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

#### 2. Ejecutar la Aplicación

**Interfaz Gráfica (GUI Simple):**
```powershell
python gui_simple.py
# O
python main.py
```

**Interfaz CLI Interactiva:**
```powershell
python cli.py --interactive
```

**Gestión de Aseguradoras:**
```powershell
python cli.py --manage-payees
```

## 🎨 Interfaz Gráfica - Guía de Uso

### Pestaña 1: 📝 Nueva Carta

**Sub-pestaña "Emisión y Cliente":**
- Ciudad de emisión (default: MEDELLÍN)
- Fecha de emisión
- Número de carta (formato: `15434 - 2025`)
- Mes de cobro (selector)
- Fecha límite de pago
- Datos del asegurado:
  - Nombre completo / Razón social
  - NIT (validación con dígito verificador DIAN)
  - Dirección
  - Teléfono
  - Ciudad

**Sub-pestaña "Póliza y Montos":**
- Número de póliza (flexible - cualquier formato)
- Tipo de póliza:
  - VIDA GRUPO
  - SOAT
  - COLECTIVA
  - INDIVIDUAL
  - Otros (se normalizan automáticamente)
- Plan de póliza
- Fechas de vigencia (inicio/fin con validación)
- Montos:
  - Prima
  - IVA (impuesto)
  - Otros rubros
  - **Total calculado automáticamente** ✨

**Sub-pestaña "Aseguradora y Firma":**
- Selección de aseguradora beneficiaria:
  - Combo con aseguradoras guardadas
  - O escribir nueva (se guarda automáticamente)
  - NIT de la aseguradora
- Datos de firma:
  - Nombre del firmante
  - Cargo
  - Iniciales
- **📁 Carpeta de Salida:**
  - Ver carpeta actual
  - Botón "Cambiar Carpeta" para seleccionar destino
  - Botón "Abrir Carpeta" para ver PDFs generados

**Botones de Acción:**
- **📝 Llenar Ejemplo** - Carga datos de prueba válidos
- **🗑️ Limpiar Todo** - Resetea el formulario
- **📄 Generar PDF** - Crea la carta y pregunta si abrir

---

### Pestaña 2: 🏢 Aseguradoras

Gestión completa de aseguradoras beneficiarias:

**Tabla con columnas:**
- Nombre
- NIT
- Veces Usado (contador automático)

**Botones:**
- **➕ Agregar** - Nueva aseguradora
- **✏️ Editar** - Modificar seleccionada
- **🗑️ Eliminar** - Borrar (con confirmación)

Las aseguradoras se guardan en `logs/payees.json` y aparecen automáticamente en el combo de la primera pestaña.

---

### 💡 Tips de Uso

1. **Datos de ejemplo:** Usa el botón "Llenar Ejemplo" para ver un caso completo
2. **Validación en tiempo real:** Los campos inválidos se marcan en rojo
3. **NIT automático:** Al seleccionar aseguradora guardada, el NIT se llena solo
4. **Total automático:** Al cambiar prima/IVA/otros, el total se recalcula
5. **Carpeta personalizada:** Configura una vez y se recuerda para todos los PDFs
6. **Abrir PDF:** Después de generar, elige si crear otra carta o abrir el PDF

---

## 🏢 Gestión de Aseguradoras Beneficiarias

### Desde la GUI:

**Pestaña "Aseguradoras":**
- Tabla visual con todas las aseguradoras
- Doble clic para editar
- Botones grandes y claros
- Contador de uso para ver las más utilizadas

**Desde el formulario:**
- El combo muestra aseguradoras ordenadas por uso
- Escribir nombre nuevo lo guarda automáticamente al generar PDF
- Incrementa contador cada vez que se usa

### Desde CLI:

```powershell
python cli.py --manage-payees
```

Menú completo:
```
1. ➕ Agregar nueva aseguradora
2. 📋 Listar todas
3. ✏️ Editar aseguradora
4. 🗑️ Eliminar aseguradora
5. 🔍 Ver detalles
0. Salir
```

### Estructura JSON (`logs/payees.json`):

```json
{
  "payees": [
    {
      "name": "SEGUROS DE VIDA SURAMERICANA S.A.",
      "nit": "890903790-5",
      "usage_count": 15,
      "created_at": "2026-01-15T10:30:00",
      "last_used": "2026-01-21T14:25:00"
    }
  ]
}
```

## 📦 Construcción del Ejecutable

### Script Automatizado (`build_exe.py`)

```powershell
# Construcción automática completa
python build_exe.py
```

**El script hace todo automáticamente:**
1. ✅ Verifica/Instala PyInstaller
2. ✅ Limpia builds anteriores (dist/, build/, *.spec)
3. ✅ Compila con configuración optimizada:
   - `--onefile` - Un solo .exe
   - `--windowed` - Sin ventana de consola
   - `--clean` - Cache limpio
   - Incluye todos los módulos necesarios
   - Excluye librerías innecesarias (numpy, matplotlib)
4. ✅ Crea paquete portable con:
   - Ejecutable
   - Carpetas output/ y logs/
   - Archivo LEEME.txt con instrucciones
5. ✅ Muestra tamaño final y ubicaciones

**Resultado:**
```
dist/GeneradorCartasCobro.exe                    # 45.48 MB
GeneradorCartasCobro_Portable/                    # Paquete completo
├── GeneradorCartasCobro.exe
├── output/                                       # Para PDFs
├── logs/                                         # Para auditoría
└── LEEME.txt                                     # Instrucciones
```

### Personalización (Opcional)

Edita `build_exe.py` para cambiar:
- Nombre del ejecutable (línea 75: `app_name`)
- Icono personalizado (`--icon`, línea ~95)
- Módulos adicionales (`--hidden-import`)
- Carpetas extra (`--add-data`)

### Distribución

**Compartir solo la carpeta portable:**
```
GeneradorCartasCobro_Portable/  ← Esta carpeta completa
```

El usuario final solo necesita:
1. Extraer carpeta
2. Doble clic en .exe
3. Usar la aplicación (sin instalación)

## 📋 Características Principales

### ✅ Interfaz Gráfica Moderna
- **Dark Mode profesional**: Alto contraste (#1a1a1a fondo, #e0e0e0 texto)
- **Botones con gradientes**: Azul (acciones), Verde (éxito), Rojo (eliminar)
- **3 sub-tabs organizadas**: Evita scroll infinito en formularios largos
- **Responsive**: Scroll areas donde se necesita
- **Validación visual**: Campos inválidos se marcan claramente

### ✅ Gestión Completa de Aseguradoras
- **CRUD inline**: Agregar, editar, eliminar desde la GUI
- **Contador de uso**: Ordena aseguradoras por frecuencia
- **Autocompletado**: Selecciona y el NIT se llena automáticamente
- **Persistencia JSON**: Datos guardados en `logs/payees.json`
- **14 tests unitarios**: Cobertura completa del PayeeManager

### ✅ Validación Flexible y Robusta
- **NIT colombiano**: Algoritmo DIAN para dígito verificador
- **Números de póliza flexibles**: Acepta cualquier formato (no solo 7 dígitos)
- **Tipos normalizados**: "VIDA GRUPO" → "POLIZA DE VIDA GRUPO" automáticamente
- **Valores por defecto sensatos**: Plan "N/A" si no se especifica
- **Fechas validadas**: Fin de vigencia > Inicio
- **Cálculo automático**: Total = Prima + IVA + Otros

### ✅ Generación PDF Profesional
- **Formato legal**: Márgenes, tipografía según normativa
- **Formato colombiano**: Moneda 1.372.412,00 (punto miles, coma decimales)
- **Headers y footers**: Logotipos, datos de empresa
- **Tablas estructuradas**: Detalles de póliza y montos
- **Metadatos embebidos**: Autor, fecha, título del PDF

### ✅ Experiencia de Usuario
- **Botón "Llenar Ejemplo"**: Datos válidos para prueba rápida
- **Selector de carpeta**: Configura una vez, usa siempre
- **Botón "Abrir Carpeta"**: Acceso directo a PDFs generados
- **Pregunta al finalizar**: "¿Crear otra carta o abrir PDF?"
- **Mensajes claros**: Confirmaciones y errores descriptivos

### ✅ Ejecutable Standalone
- **45.48 MB**: Todo incluido en un .exe
- **Sin instalación**: Portable - copia y usa
- **Sin dependencias**: Python embebido
- **Paquete completo**: Con carpetas output/, logs/, instrucciones

### ✅ Trazabilidad y Auditoría
- **Registro completo**: Timestamp, acciones, errores
- **Formato estructurado**: JSON y texto plano
- **Ubicación fija**: `logs/` para análisis posterior

## 🔐 Cumplimiento Legal y Formato Colombiano

### Elementos Obligatorios
Todas las cartas incluyen:
- **Identificación de la compañía**: Razón social, NIT
- **Fecha de emisión**: Formato español largo (21 de enero de 2026)
- **Identificación del destinatario**: Nombre completo, NIT, dirección
- **Número de referencia**: Formato único de documento
- **Detalles de póliza**: Número, tipo, vigencia, plan
- **Montos desglosados**: Prima, IVA, otros rubros, total
- **Plazos**: Mes de cobro, fecha límite de pago
- **Firma**: Nombre, cargo, iniciales del firmante

### Formato Colombiano
- **Moneda COP**: 1.372.412,00 (punto miles, coma decimales)
- **NIT validado**: Algoritmo DIAN para dígito verificador
- **Fechas españolas**: "21 de enero de 2026"
- **Teléfonos**: 10 dígitos (301XXXXXXX)

### Validación NIT (Algoritmo DIAN)
```python
# Ejemplo: 900123456-6
# Dígito verificador calculado automáticamente
def calcular_digito_verificador(nit: str) -> str:
    # Algoritmo oficial DIAN Colombia
    pesos = [71, 67, 59, 53, 47, 43, 41, 37, 29, 23, 19, 17, 13, 7, 3]
    # ... resto del algoritmo
```

### Registro de Auditoría
Cada documento generado registra:
```json
{
    "timestamp": "2026-01-21T14:30:00",
    "documento_id": "carta_cobro_15434-2025_9001234566.pdf",
    "asegurado_nit": "900123456-6",
    "poliza": "VG-2026-0001",
    "montos": {
        "prima": 1500000.00,
        "impuesto": 285000.00,
        "otros_rubros": 50000.00,
        "total": 1835000.00
    },
    "aseguradora": "SEGUROS DE VIDA SURAMERICANA S.A.",
    "output_path": "output/carta_cobro_15434-2025_9001234566.pdf"
}
```

## 🧪 Testing

```powershell
# Ejecutar todos los tests
pytest tests/ -v

# Tests de gestión de aseguradoras (14 tests)
pytest tests/test_payee_manager.py -v

# Tests con cobertura
pytest --cov=utils --cov=models --cov=generators tests/

# Test específico
pytest tests/test_payee_manager.py::test_add_payee -v
```

**Cobertura actual:**
- ✅ PayeeManager: 14 tests (CRUD completo, validaciones, persistencia)
- ✅ Validadores: NIT DIAN, teléfonos, formatos
- ✅ Generadores: Creación de PDFs, formato colombiano

**Para agregar tests nuevos:**
```python
# tests/test_nuevo_modulo.py
import pytest
from models.documento import Documento

def test_documento_con_datos_minimos():
    """Test que el documento acepta datos mínimos válidos."""
    doc = Documento(
        numero_carta="15434 - 2025",
        mes_cobro="Enero",
        # ... resto de campos
    )
    assert doc.numero_carta == "15434 - 2025"
```

## 📦 Empaquetado

```powershell
# Generar ejecutable con PyInstaller
pyinstaller --onefile --windowed --name "GeneradorCartas" main.py

# El ejecutable estará en dist/GeneradorCartas.exe
```

## 🤝 Contribución y Desarrollo

### Workflow de Desarrollo
1. **Clonar repositorio**
2. **Crear rama** para nueva funcionalidad
3. **Implementar cambios** con tests
4. **Ejecutar tests**: `pytest tests/ -v`
5. **Actualizar README** si hay cambios de API
6. **Commit y push**

### Estructura de Commits
```
feat: Agregar validación de vigencia de póliza
fix: Corregir cálculo de dígito verificador NIT
docs: Actualizar README con nueva funcionalidad
test: Agregar tests para PayeeManager
refactor: Simplificar generador de PDFs
```

### Convenciones de Código
- **PEP 8** para estilo Python
- **Type hints** en todas las funciones públicas
- **Docstrings** en formato Google:
  ```python
  def agregar_aseguradora(nombre: str, nit: str) -> dict:
      """Agrega una nueva aseguradora al catálogo.
      
      Args:
          nombre: Razón social de la aseguradora
          nit: NIT con dígito verificador (formato: 890903790-5)
      
      Returns:
          Diccionario con los datos de la aseguradora creada
      
      Raises:
          ValueError: Si la aseguradora ya existe o el NIT es inválido
      """
  ```
- **Nombres en español** para dominio de negocio (asegurado, poliza, montos)
- **Nombres en inglés** para conceptos técnicos (generator, validator, manager)
- **Logging estructurado**: `logger.info(f"Acción realizada: {detalle}")`

### Agregar Nueva Funcionalidad

**Ejemplo: Agregar nuevo tipo de documento**

1. **Crear modelo** en `models/`:
```python
# models/acta_entrega.py
class ActaEntrega(BaseModel):
    numero: str
    fecha: date
    # ... campos específicos
```

2. **Crear generador** en `generators/`:
```python
# generators/acta_entrega_generator.py
class ActaEntregaGenerator(BaseGenerator):
    def generate(self, data: dict, output_filename: str) -> Path:
        # ... lógica de generación
```

3. **Agregar a GUI** en `gui_simple.py`:
```python
# Agregar nuevo tab o ampliar existente
self.tipo_documento = QComboBox()
self.tipo_documento.addItems(["Carta Cobro", "Acta Entrega"])
```

4. **Escribir tests**:
```python
# tests/test_acta_entrega.py
def test_generar_acta_entrega():
    acta = ActaEntrega(numero="AE-001", fecha=date.today())
    generator = ActaEntregaGenerator()
    pdf_path = generator.generate(acta.to_pdf_data(), "acta_001.pdf")
    assert pdf_path.exists()
```

### Rebuild del Ejecutable

Después de cualquier cambio en el código:
```powershell
python build_exe.py
```

Esto regenera automáticamente:
- `dist/GeneradorCartasCobro.exe`
- `GeneradorCartasCobro_Portable/` completo

## 📞 Soporte y Contacto

**Proyecto**: Automatizaciones - SEGUROS UNIÓN  
**Desarrollador**: DANIEL GARCIA ARAQUE  
**Cargo**: Desarrollador  
**Departamento**: Tecnología  

**Versión**: 1.0.0  
**Fecha**: Enero 2026  
**Python**: 3.13.2  
**PyQt6**: 6.6+  

### Roadmap Futuro
- [ ] Envío automático por correo electrónico
- [ ] Firma digital integrada
- [ ] Plantillas personalizables desde GUI
- [ ] Generación masiva (batch) desde Excel/CSV
- [ ] Dashboard de estadísticas de cobros
- [ ] Integración con bases de datos SQL
- [ ] API REST para integración con otros sistemas
- [ ] Modo offline con sincronización posterior

### Changelog

**v1.0.0** (Enero 2026)
- ✅ GUI completa con Dark Mode
- ✅ Gestión CRUD de aseguradoras
- ✅ Validación flexible de datos
- ✅ Formato colombiano (NIT DIAN, moneda COP)
- ✅ Selector de carpeta de salida
- ✅ Ejecutable standalone 45.48 MB
- ✅ Script automatizado de build
- ✅ 14 tests unitarios para PayeeManager
- ✅ Documentación completa

---

## 📸 Capturas de Pantalla

### Interfaz Principal - Dark Mode
```
┌────────────────────────────────────────────────────────────┐
│  [📝 Nueva Carta]  [🏢 Aseguradoras]                       │
│                                                             │
│  ┌─ 1️⃣ Emisión y Cliente ─────────────────────────────┐   │
│  │                                                       │   │
│  │  Ciudad de Emisión: [MEDELLIN        ]              │   │
│  │  Fecha de Emisión:  [21/01/2026    ▼]              │   │
│  │  Número de Carta:   [15434 - 2025   ]              │   │
│  │  Mes de Cobro:      [Enero         ▼]              │   │
│  │  Fecha Límite Pago: [20/02/2026    ▼]              │   │
│  │                                                       │   │
│  │  👤 Datos del Asegurado:                            │   │
│  │  Nombre Completo:   [JUAN CARLOS RODRIGUEZ...     ]│   │
│  │  NIT:               [900123456-6    ] ✓ Válido     │   │
│  │  Dirección:         [Carrera 45 # 76-32...       ]│   │
│  │  Teléfono:          [3001234567      ]             │   │
│  │  Ciudad:            [MEDELLIN        ]             │   │
│  └───────────────────────────────────────────────────┘   │
│                                                             │
│  [📝 Llenar Ejemplo] [🗑️ Limpiar] [📄 Generar PDF]       │
└────────────────────────────────────────────────────────────┘
```

### Pestaña Gestión de Aseguradoras
```
┌────────────────────────────────────────────────────────────┐
│  🏢 Gestión de Aseguradoras                                │
├────────────────────────────────────────────────────────────┤
│  [➕ Agregar] [✏️ Editar] [🗑️ Eliminar]                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Nombre                     │ NIT           │ Usado   │  │
│  ├────────────────────────────┼───────────────┼────────┤  │
│  │ SEGUROS SURAMERICANA S.A. │ 890903790-5   │ 15     │  │
│  │ SEGUROS BOLÍVAR S.A.      │ 860002503-4   │ 8      │  │
│  │ SEGUROS MUNDIAL S.A.      │ 860014968-9   │ 3      │  │
│  └─────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### Selector de Carpeta de Salida
```
┌────────────────────────────────────────────────────────────┐
│  📁 Carpeta de Salida                                      │
│                                                             │
│  📂 C:\Users\...\output                                    │
│                                                             │
│  [📁 Cambiar Carpeta]  [🗂️ Abrir Carpeta]                │
└────────────────────────────────────────────────────────────┘
```

---

**⚠️ Nota de Privacidad**: Este sistema es de uso interno exclusivo de SEGUROS UNIÓN. Los datos procesados contienen información sensible y están protegidos según normativas de protección de datos colombianas y GDPR.
