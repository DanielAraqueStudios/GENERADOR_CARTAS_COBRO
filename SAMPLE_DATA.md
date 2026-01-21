# 📋 SAMPLE DATA - Estructura de Carta de Cobro

Este documento describe la estructura de datos de una carta de cobro real de SEGUROS DE VIDA SURAMERICANA S.A. y define qué campos son **editables** (inputs del usuario) vs **estáticos** (plantilla fija).

---

## 📄 Ejemplo Real de Carta de Cobro

```
Medellín, 18 de diciembre de 2025

CARTA COBRO N° 15434 - 2025

Señores
COOPERATIVA DEL COMERCIO EXTERIOR COLOMBIANO    NIT 860023108 - 6
CR 13 28 01 P 5    Teléfono 6067676
Bogotá D.C.

ASUNTO: POLIZA DE VIDA GRUPO N° 3144016
        COOPERATIVA DEL COMERCIO EXTERIOR COLOMBIANO

Cordial saludo

Cobro mensual correspondiente al mes de Octubre

┌──────────────┬─────────────┬──────────┬─────────────┬──────────────┬───────────┬────────────┬──────────────┐
│ Ramo         │ Plan Póliza │ Doc.     │ Prima       │ Otros Rubros │ Impuesto  │ Val. Exter.│ Total        │
├──────────────┼─────────────┼──────────┼─────────────┼──────────────┼───────────┼────────────┼──────────────┤
│ VIDA GRUPO   │ 06 3144016  │21155722  │ 1.372.412,00│ 0,00         │ 0,00      │ 0,00       │ 1.372.412,00 │
└──────────────┴─────────────┴──────────┴─────────────┴──────────────┴───────────┴────────────┴──────────────┘

*CUOTA MENSUAL N° 5 VIGENCIA 30-SEPT.-2025 - 30-OCT.-2025
VALOR A PAGAR A FAVOR DE SEGUROS DE VIDA SURAMERICANA S.A.    1.372.412,00

*Otros Rubros: Se refiere a gastos de expedición y/o otros conceptos.
*Val. Exter. (Valores externos): Se refiere a costos bancarios y/o gastos de operación.

PUEDE REALIZAR SUS PAGOS POR PSE EN LA PAGINA WEB WWW.SURA.COM - PAGO EXPRESS...

NIT 890903790-5
RECUERDE ENVIARNOS EL SOPORTE DE PAGO…

Nota: Las primas de seguros aquí relacionadas deben ser declaradas a nombre de la aseguradora...
F. Límite de pago: 23-dic.-2025

REITERAMOS NUESTRA DISPOSICIÓN DE SERVICIO.

Atentamente,

YULIANA ANDREA VELASQUEZ VALENCI
Ejecutivo YAVV

Carrera 77 A # 49 - 37 .Sector Estadio - Medellin E-mail: gerencia@segurosunion.com
```

---

## �️ Estructura JSON del Documento

El documento sigue una estructura jerárquica normalizada que separa **datos crudos** (raw) de **datos normalizados** para facilitar procesamiento y validación:

```python
Document Structure:
├── issue (metadata de emisión)
│   ├── city: "Medellín"
│   ├── date_text: "18 de diciembre de 2025"  # Formato largo español
│   └── date_iso: "2025-12-18"                # ISO 8601
│
├── identifiers (identificación del documento)
│   ├── title_label: "CARTA COBRO N°"
│   ├── document_number_text: "15434 - 2025"  # Con espacios
│   └── document_number_normalized: "15434-2025"  # Sin espacios
│
├── recipient (datos del cliente destinatario)
│   ├── organization_name: "COOPERATIVA DEL COMERCIO..."
│   ├── nit: "860023108-6"                    # Con guión
│   ├── address_text: "CR 13 28 01 P 5"
│   ├── phone: "6067676"
│   └── city: "Bogotá D.C."
│
├── subject (asunto de la carta)
│   ├── lines: ["POLIZA DE VIDA GRUPO N° 3144016", ...]
│   ├── policy_number: "3144016"
│   └── policy_type: "Vida Grupo"
│
├── billing_table (tabla de cobro)
│   └── rows[0]
│       ├── ramo: "VIDA GRUPO"
│       ├── plan_poliza_text: "06  3144016"    # 2 espacios
│       ├── plan_code_inferred: "06"           # Extraído
│       ├── policy_number: "3144016"           # Extraído
│       ├── document_reference: "21155722"     # Doc. separado
│       ├── amounts_raw: {                     # Formato colombiano
│       │   "prima": "1.372.412,00",
│       │   "total": "1.372.412,00"
│       │ }
│       └── amounts_normalized: {              # Numérico
│           "currency": "COP",
│           "prima": 1372412.0,
│           "total": 1372412.0
│         }
│
├── installment_detail (detalle de cuota)
│   ├── monthly_installment_number: 5
│   ├── coverage_period_text: "30-SEPT.-2025 - 30-OCT.-2025"
│   └── coverage_period_iso: {
│       "start_date": "2025-09-30",
│       "end_date": "2025-10-30"
│     }
│
├── payee (beneficiario del pago) ⚠️ DIFERENTE AL EMISOR
│   ├── company_name: "SEGUROS DE VIDA SURAMERICANA S.A."
│   └── company_nit: "890903790-5"
│
├── due_date (fecha límite)
│   ├── date_text: "23-dic.-2025"              # Formato corto
│   └── date_iso: "2025-12-23"
│
├── signature (firma)
│   ├── name: "YULIANA ANDREA VELASQUEZ VALENCI"
│   ├── role: "Ejecutivo"
│   └── initials: "YAVV"
│
└── sender_contact_footer (emisor/remitente)
    ├── address: "Carrera 77 A # 49 - 37 .Sector Estadio - Medellin"
    └── email: "gerencia@segurosunion.com"
```

### 🏢 Modelo de Doble Compañía

**IMPORTANTE**: El sistema maneja DOS entidades diferentes:

| Rol | Compañía | Identificación | Aparece en |
|-----|----------|----------------|------------|
| **Emisor** | SEGUROS UNIÓN | gerencia@segurosunion.com | Footer, firma |
| **Beneficiario del Pago** | SEGUROS DE VIDA SURAMERICANA S.A. | NIT 890903790-5 | Cuerpo del documento |

**Significado**: SEGUROS UNIÓN emite la carta de cobro **en representación de** SEGUROS DE VIDA SURAMERICANA S.A., quien es la aseguradora real.

---

## �🔧 Campos Editables (Inputs del Usuario)

### 1️⃣ **Encabezado del Documento**

| Campo | Tipo | Ejemplo | Validación |
|-------|------|---------|------------|
| `ciudad_emision` | Text | "Medellín" | Requerido |
| `fecha_emision` | Date | "18 de diciembre de 2025" | Formato: dd de mes de yyyy |
| `numero_carta` | Text | "15434 - 2025" | Patrón: `\d+ - \d{4}` |

### 2️⃣ **Datos del Cliente (Destinatario)**

| Campo | Tipo | Ejemplo | Validación |
|-------|------|---------|------------|
| `cliente_razon_social` | Text | "COOPERATIVA DEL COMERCIO EXTERIOR COLOMBIANO" | Requerido, máx. 100 chars |
| `cliente_nit` | Text | "860023108 - 6" | Formato NIT colombiano: `\d{9} - \d` |
| `cliente_direccion` | Text | "CR 13 28 01 P 5" | Requerido |
| `cliente_telefono` | Text | "6067676" | 7-10 dígitos |
| `cliente_ciudad` | Text | "Bogotá D.C." | Requerido |

### 3️⃣ **Datos de la Póliza**

| Campo | Tipo | Ejemplo | Validación |
|-------|------|---------|------------|
| `poliza_numero` | Text | "3144016" | 7 dígitos |
| `poliza_tipo` | Select | "POLIZA DE VIDA GRUPO" | Opciones: VIDA GRUPO, COLECTIVO, INDIVIDUAL |
| `poliza_ramo` | Text | "VIDA GRUPO" | Auto-calculado desde poliza_tipo |
| `mes_cobro` | Select | "Octubre" | Meses del año |

### 4️⃣ **Detalle de Cobro (Tabla)**

| Campo | Tipo | Ejemplo | Validación |
|-------|------|---------|------------|
| `plan_poliza` | Text | "06  3144016" | Formato: `\d{2}  \d{7}` |
| `documento_referencia` | Text | "21155722" | 8 dígitos |
| `prima` | Currency | "1.372.412,00" | Formato colombiano (punto miles, coma decimales) |
| `otros_rubros` | Currency | "0,00" | Opcional, default: 0,00 |
| `impuesto` | Currency | "0,00" | Opcional, default: 0,00 |
| `valor_externo` | Currency | "0,00" | Opcional, default: 0,00 |
| `total` | Currency | "1.372.412,00" | Auto-calculado: suma de todos |

### 5️⃣ **Información de Cuota**

| Campo | Tipo | Ejemplo | Validación |
|-------|------|---------|------------|
| `cuota_numero` | Integer | "5" | 1-999 |
| `vigencia_inicio` | Date | "30-SEPT.-2025" | Formato: dd-MMM-yyyy (español) |
| `vigencia_fin` | Date | "30-OCT.-2025" | Formato: dd-MMM-yyyy (español) |
| `fecha_limite_pago` | Date | "23-dic.-2025" | Formato: dd-mes-yyyy |

### 6️⃣ **Firma**

| Campo | Tipo | Ejemplo | Validación |
|-------|------|---------|------------|
| `firmante_nombre` | Text | "YULIANA ANDREA VELASQUEZ VALENCI" | Requerido, mayúsculas |
| `firmante_cargo` | Text | "Ejecutivo YAVV" | Requerido |

---

## 🔒 Elementos Estáticos (No Editables)

Estos elementos son parte de la plantilla y **NO** deben ser inputs:

### Textos Legales Fijos
```python
TEXTO_INSTRUCCIONES_PAGO = """
*Otros Rubros: Se refiere a gastos de expedición y/o otros conceptos.
*Val. Exter. (Valores externos): Se refiere a costos bancarios y/o gastos de operación.
PUEDE REALIZAR SUS PAGOS POR PSE EN LA PAGINA WEB WWW.SURA.COM - 
PAGO EXPRESS CON EL RECIBO DE PAGO EN LOS BANCOS AUTORIZADOS POR LA COMPAÑÍA
"""

TEXTO_NOTA_LEGAL = """
Nota: Las primas de seguros aquí relacionadas deben ser declaradas a nombre 
de la aseguradora que los expide. ART 1068 C. De C. La mora en el pago de 
la prima de la póliza o de los certificados o anexos que se expidan con 
fundamento en ella, producirá la terminación automática del contrato.
"""

TEXTO_RECORDATORIO = "NIT 890903790-5\nRECUERDE ENVIARNOS EL SOPORTE DE PAGO…"

TEXTO_DESPEDIDA = "REITERAMOS NUESTRA DISPOSICIÓN DE SERVICIO."

TEXTO_SALUDO = "Cordial saludo"
```

### Información de la Empresa (Footer)
```python
EMPRESA_DIRECCION = "Carrera 77 A # 49 - 37 .Sector Estadio - Medellin"
EMPRESA_EMAIL = "gerencia@segurosunion.com"
EMPRESA_NIT = "890903790-5"
EMPRESA_NOMBRE = "SEGUROS DE VIDA SURAMERICANA S.A."
```

### Headers de Tabla
```python
TABLA_HEADERS = ["Ramo", "Plan Póliza", "Doc.", "Prima", "Otros Rubros", 
                  "Impuesto", "Val. Exter.", "Total"]
```

---

## � Reglas de Normalización de Datos

### 1. Conversión de Moneda (Colombian Format ↔ Decimal)

```python
# Input usuario → Raw (almacenamiento) → Normalized (cálculos)
1372412.00 → "1.372.412,00" → 1372412.0

# Reglas:
# - Separador de miles: punto (.)
# - Separador decimal: coma (,)
# - Siempre 2 decimales en formato raw
# - Float estándar en normalized

class CurrencyParser:
    @staticmethod
    def to_raw(value: float) -> str:
        """1372412.0 → '1.372.412,00'"""
        formatted = f"{value:,.2f}"
        return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @staticmethod
    def to_normalized(raw: str) -> float:
        """'1.372.412,00' → 1372412.0"""
        cleaned = raw.replace('.', '').replace(',', '.')
        return float(cleaned)
```

### 2. Conversión de Fechas (Multiple Spanish Formats)

```python
class DateFormatter:
    FORMATS = {
        "long_spanish": "%d de %B de %Y",      # 18 de diciembre de 2025
        "short_upper": "%d-%b.-%Y",           # 30-SEPT.-2025 (uppercase)
        "short_lower": "%d-%b.-%Y",           # 23-dic.-2025 (lowercase)
        "iso": "%Y-%m-%d"                      # 2025-12-18
    }
    
    MONTH_NAMES_ES = {
        "enero": "ene.", "febrero": "feb.", "marzo": "mar.",
        "abril": "abr.", "mayo": "may.", "junio": "jun.",
        "julio": "jul.", "agosto": "ago.", "septiembre": "sept.",
        "octubre": "oct.", "noviembre": "nov.", "diciembre": "dic."
    }
    
    @staticmethod
    def to_long_spanish(date_iso: str) -> str:
        """2025-12-18 → '18 de diciembre de 2025'"""
        pass
    
    @staticmethod
    def to_short_upper(date_iso: str) -> str:
        """2025-09-30 → '30-SEPT.-2025'"""
        pass
    
    @staticmethod
    def to_short_lower(date_iso: str) -> str:
        """2025-12-23 → '23-dic.-2025'"""
        pass
```

### 3. Normalización de NIT

```python
class NITValidator:
    @staticmethod
    def normalize(nit_input: str) -> str:
        """Normaliza NIT a formato estándar con guión"""
        # Input posible: "860023108-6" o "8600231086" o "860023108 - 6"
        # Output: "860023108-6"
        digits_only = ''.join(filter(str.isdigit, nit_input))
        return f"{digits_only[:9]}-{digits_only[9]}"
    
    @staticmethod
    def validate_check_digit(nit: str) -> bool:
        """Valida dígito verificador según algoritmo colombiano"""
        # Algoritmo: https://www.dian.gov.co/
        digits = nit.replace('-', '')
        base = digits[:9]
        check = int(digits[9])
        
        primes = [3, 7, 13, 17, 19, 23, 29, 37, 41]
        total = sum(int(base[i]) * primes[i] for i in range(9))
        calculated = (11 - (total % 11)) % 11
        
        return calculated == check
```

### 4. Parseo de Plan Póliza

```python
class PolicyParser:
    @staticmethod
    def parse_plan_poliza(plan_text: str) -> dict:
        """'06  3144016' → {'plan_code': '06', 'policy_number': '3144016'}"""
        # Nota: DOS espacios separan código de plan y número de póliza
        parts = plan_text.split('  ')  # Doble espacio
        return {
            "plan_code_inferred": parts[0].strip(),
            "policy_number": parts[1].strip() if len(parts) > 1 else ""
        }
```

---

## �📊 Reglas de Negocio

### Cálculo Automático del Total
```python
total = prima + otros_rubros + impuesto + valor_externo
```

### Formato de Moneda Colombiano
```python
# Input: 1372412.00
# Output: "1.372.412,00"
# Separador de miles: punto (.)
# Separador decimal: coma (,)
# Siempre 2 decimales
```

### Formato de Fechas
```python
# Fecha emisión: "18 de diciembre de 2025"
# Fecha límite: "23-dic.-2025"
# Fecha vigencia: "30-SEPT.-2025"
```

### Generación Automática de Número de Carta
```python
# Formato: {consecutivo} - {año}
# Ejemplo: "15434 - 2025"
# El consecutivo se incrementa automáticamente
```

---

## 🎨 Formato Visual (ReportLab)

### Tipografía
- **Título "CARTA COBRO N°"**: Helvetica-Bold, 14pt
- **Datos del cliente**: Helvetica, 10pt
- **Tabla**: Helvetica, 9pt
- **Textos legales**: Helvetica, 8pt
- **Firma**: Helvetica-Bold, 10pt

### Márgenes
- Superior: 2.5 cm
- Inferior: 2 cm
- Izquierdo: 2.5 cm
- Derecho: 2.5 cm

### Colores
- Header tabla: RGB(200, 200, 200) - Gris claro
- Bordes tabla: Negro 0.5pt
- Texto principal: Negro

### Espaciado
- Entre secciones: 0.5 cm
- Interlineado: 1.15
- Antes de tabla: 0.3 cm
- Después de tabla: 0.3 cm

---

## 🗂️ JSON Template Example

```json
{
  "template_id": "carta_cobro_seguros_union",
  "version": "1.0",
  "document_type": "Carta de Cobro - SEGUROS UNIÓN",
  "fields": [
    {
      "id": "ciudad_emision",
      "label": "Ciudad de Emisión",
      "type": "text",
      "required": true,
      "default": "Medellín",
      "validation": "text_not_empty"
    },
    {
      "id": "fecha_emision",
      "label": "Fecha de Emisión",
      "type": "date",
      "required": true,
      "format": "dd de MMMM de yyyy",
      "validation": "valid_date"
    },
    {
      "id": "numero_carta",
      "label": "Número de Carta",
      "type": "text",
      "required": true,
      "pattern": "^\\d+ - \\d{4}$",
      "auto_generate": true,
      "help_text": "Se genera automáticamente: {consecutivo} - {año}"
    },
    {
      "id": "cliente_razon_social",
      "label": "Razón Social del Cliente",
      "type": "text",
      "required": true,
      "max_length": 100,
      "validation": "text_not_empty"
    },
    {
      "id": "cliente_nit",
      "label": "NIT del Cliente",
      "type": "text",
      "required": true,
      "pattern": "^\\d{9} - \\d$",
      "validation": "nit_colombiano",
      "help_text": "Formato: 123456789 - 0"
    },
    {
      "id": "cliente_direccion",
      "label": "Dirección",
      "type": "text",
      "required": true,
      "max_length": 100
    },
    {
      "id": "cliente_telefono",
      "label": "Teléfono",
      "type": "text",
      "required": true,
      "pattern": "^\\d{7,10}$",
      "validation": "telefono_colombiano"
    },
    {
      "id": "cliente_ciudad",
      "label": "Ciudad",
      "type": "text",
      "required": true,
      "validation": "text_not_empty"
    },
    {
      "id": "poliza_numero",
      "label": "Número de Póliza",
      "type": "text",
      "required": true,
      "pattern": "^\\d{7}$",
      "validation": "numero_poliza"
    },
    {
      "id": "poliza_tipo",
      "label": "Tipo de Póliza",
      "type": "select",
      "required": true,
      "options": [
        "POLIZA DE VIDA GRUPO",
        "POLIZA COLECTIVA",
        "POLIZA INDIVIDUAL"
      ],
      "default": "POLIZA DE VIDA GRUPO"
    },
    {
      "id": "mes_cobro",
      "label": "Mes de Cobro",
      "type": "select",
      "required": true,
      "options": [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
      ]
    },
    {
      "id": "plan_poliza",
      "label": "Plan Póliza",
      "type": "text",
      "required": true,
      "pattern": "^\\d{2}  \\d{7}$",
      "help_text": "Formato: 06  3144016 (dos espacios)"
    },
    {
      "id": "documento_referencia",
      "label": "Documento de Referencia",
      "type": "text",
      "required": true,
      "pattern": "^\\d{8}$"
    },
    {
      "id": "prima",
      "label": "Prima (COP)",
      "type": "currency",
      "required": true,
      "min": 0,
      "format": "colombian",
      "validation": "positive_amount",
      "storage": {
        "raw": "amounts_raw.prima",
        "normalized": "amounts_normalized.prima"
      },
      "normalization": {
        "input": "float",
        "display": "colombian_currency",
        "storage": "dual"
      }
    },
    {
      "id": "otros_rubros",
      "label": "Otros Rubros (COP)",
      "type": "currency",
      "required": false,
      "default": 0,
      "min": 0,
      "format": "colombian"
    },
    {
      "id": "impuesto",
      "label": "Impuesto (COP)",
      "type": "currency",
      "required": false,
      "default": 0,
      "min": 0,
      "format": "colombian"
    },
    {
      "id": "valor_externo",
      "label": "Valores Externos (COP)",
      "type": "currency",
      "required": false,
      "default": 0,
      "min": 0,
      "format": "colombian"
    },
    {
      "id": "cuota_numero",
      "label": "Número de Cuota",
      "type": "integer",
      "required": true,
      "min": 1,
      "max": 999
    },
    {
      "id": "vigencia_inicio",
      "label": "Inicio de Vigencia",
      "type": "date",
      "required": true,
      "format": "dd-MMM-yyyy",
      "validation": "valid_date"
    },
    {
      "id": "vigencia_fin",
      "label": "Fin de Vigencia",
      "type": "date",
      "required": true,
      "format": "dd-MMM-yyyy",
      "validation": "valid_date"
    },
    {
      "id": "fecha_limite_pago",
      "label": "Fecha Límite de Pago",
      "type": "date",
      "required": true,
      "format": "dd-mes-yyyy",
      "validation": "valid_date"
    },
    {
      "id": "firmante_nombre",
      "label": "Nombre del Firmante",
      "type": "text",
      "required": true,
      "transform": "uppercase",
      "validation": "text_not_empty"
    },
    {
      "id": "firmante_cargo",
      "label": "Cargo del Firmante",
      "type": "text",
      "required": true,
      "validation": "text_not_empty"
    }
  ],
  "static_fields": [
    {
      "id": "payee_company_name",
      "label": "Empresa Beneficiaria del Pago",
      "value": "SEGUROS DE VIDA SURAMERICANA S.A.",
      "editable": false,
      "description": "Aseguradora real que recibe el pago"
    },
    {
      "id": "payee_company_nit",
      "label": "NIT Beneficiario",
      "value": "890903790-5",
      "editable": false
    },
    {
      "id": "sender_company_name",
      "label": "Empresa Emisora",
      "value": "SEGUROS UNIÓN",
      "editable": false,
      "description": "Intermediario que emite la carta de cobro"
    },
    {
      "id": "sender_email",
      "value": "gerencia@segurosunion.com",
      "editable": false
    },
    {
      "id": "sender_address",
      "value": "Carrera 77 A # 49 - 37 .Sector Estadio - Medellin",
      "editable": false
    }
  ],
  "computed_fields": [
    {
      "id": "total",
      "formula": "amounts_normalized.prima + amounts_normalized.otros_rubros + amounts_normalized.impuesto + amounts_normalized.valor_externo",
      "type": "currency",
      "format": "colombian",
      "description": "Suma automática de todos los rubros"
    },
    {
      "id": "total_raw",
      "formula": "CurrencyParser.to_raw(total)",
      "type": "string",
      "description": "Total en formato colombiano para display"
    },
    {
      "id": "poliza_ramo",
      "formula": "poliza_tipo.replace('POLIZA DE ', '')",
      "type": "text",
      "description": "Extrae el tipo de ramo del nombre de póliza"
    },
    {
      "id": "plan_code_inferred",
      "formula": "PolicyParser.parse_plan_poliza(plan_poliza)['plan_code_inferred']",
      "type": "text",
      "description": "Código de plan extraído de plan_poliza_text"
    },
    {
      "id": "document_number_normalized",
      "formula": "numero_carta.replace(' - ', '-')",
      "type": "text",
      "description": "Número de carta sin espacios alrededor del guión"
    },
    {
      "id": "date_iso",
      "formula": "DateFormatter.to_iso(fecha_emision)",
      "type": "date",
      "description": "Fecha de emisión en formato ISO 8601"
    }
  ]
}
```

---

## 🧪 Datos de Prueba (Testing)

```python
TEST_DATA_VALID = {
    # Datos de emisión
    "ciudad_emision": "Medellín",
    "fecha_emision": "2025-12-18",
    "fecha_emision_text": "18 de diciembre de 2025",  # Formato largo
    "numero_carta": "15434 - 2025",
    "numero_carta_normalized": "15434-2025",
    
    # Datos del cliente
    "cliente_razon_social": "COOPERATIVA DEL COMERCIO EXTERIOR COLOMBIANO",
    "cliente_nit": "860023108-6",
    "cliente_direccion": "CR 13 28 01 P 5",
    "cliente_telefono": "6067676",
    "cliente_ciudad": "Bogotá D.C.",
    
    # Datos de póliza
    "poliza_numero": "3144016",
    "poliza_tipo": "POLIZA DE VIDA GRUPO",
    "mes_cobro": "Octubre",
    "plan_poliza": "06  3144016",  # DOS espacios
    "plan_code_inferred": "06",  # Extraído
    "documento_referencia": "21155722",
    
    # Montos (input numérico)
    "prima": 1372412.00,
    "otros_rubros": 0.00,
    "impuesto": 0.00,
    "valor_externo": 0.00,
    
    # Montos raw (para documento)
    "amounts_raw": {
        "prima": "1.372.412,00",
        "otros_rubros": "0,00",
        "impuesto": "0,00",
        "valor_externo": "0,00",
        "total": "1.372.412,00"
    },
    
    # Montos normalized (para cálculos)
    "amounts_normalized": {
        "currency": "COP",
        "prima": 1372412.0,
        "otros_rubros": 0.0,
        "impuesto": 0.0,
        "valor_externo": 0.0,
        "total": 1372412.0
    },
    
    # Detalles de cuota
    "cuota_numero": 5,
    "vigencia_inicio": "2025-09-30",
    "vigencia_inicio_text": "30-SEPT.-2025",  # Formato corto uppercase
    "vigencia_fin": "2025-10-30",
    "vigencia_fin_text": "30-OCT.-2025",
    "fecha_limite_pago": "2025-12-23",
    "fecha_limite_pago_text": "23-dic.-2025",  # Formato corto lowercase
    
    # Firma
    "firmante_nombre": "YULIANA ANDREA VELASQUEZ VALENCI",
    "firmante_cargo": "Ejecutivo",
    "firmante_iniciales": "YAVV",
    
    # Empresas (estáticos)
    "payee_company_name": "SEGUROS DE VIDA SURAMERICANA S.A.",
    "payee_company_nit": "890903790-5",
    "sender_company_name": "SEGUROS UNIÓN",
    "sender_email": "gerencia@segurosunion.com",
    "sender_address": "Carrera 77 A # 49 - 37 .Sector Estadio - Medellin"
}

TEST_DATA_INVALID_NIT = {
    **TEST_DATA_VALID,
    "cliente_nit": "12345678"  # Falta el dígito de verificación
}

TEST_DATA_INVALID_CURRENCY = {
    **TEST_DATA_VALID,
    "prima": -100.00  # Valor negativo no permitido
}
```

---

## 📝 Notas de Implementación

### Prioridades
1. ✅ Validación estricta de NIT colombiano (formato + dígito verificador)
2. ✅ Formato de moneda colombiano (punto miles, coma decimales)
3. ✅ Generación automática de número de carta (consecutivo)
4. ✅ Cálculo automático del total
5. ✅ Conversión de fechas a formato español (SEPT., OCT., dic.)

### Campos Calculados
- `total`: Suma automática de prima + otros_rubros + impuesto + valor_externo
- `poliza_ramo`: Extracción automática desde poliza_tipo
- `numero_carta`: Auto-incremento de consecutivo anual

### Validaciones Críticas
- **NIT**: Algoritmo de dígito verificador colombiano
- **Teléfono**: 7-10 dígitos (fijos y móviles Colombia)
- **Monedas**: Valores positivos o cero, formato colombiano
- **Fechas**: vigencia_fin > vigencia_inicio

---

**Última actualización**: Enero 20, 2026  
**Basado en**: Carta de cobro real SEGUROS DE VIDA SURAMERICANA S.A.
