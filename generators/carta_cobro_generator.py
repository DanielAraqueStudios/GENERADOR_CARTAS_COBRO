"""
Generador PDF especializado para cartas de cobro de SEGUROS UNIÓN.
"""
from pathlib import Path
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

from .base_generator import BaseGenerator


class CartaCobroGenerator(BaseGenerator):
    """
    Generador de PDF para cartas de cobro de pólizas de seguros.
    """
    
    def __init__(self, output_dir: Path = None):
        super().__init__(output_dir)
        self.page_width, self.page_height = letter
        self.margin = 2.5 * cm
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Valida que los datos contengan todos los campos requeridos.
        
        Raises:
            ValueError: Si falta algún campo requerido
        """
        required_fields = [
            'ciudad_emision', 'fecha_emision', 'numero_carta',
            'cliente_razon_social', 'cliente_nit', 'cliente_direccion',
            'cliente_telefono', 'cliente_ciudad', 'poliza_numero',
            'poliza_tipo', 'amounts_raw'
        ]
        
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValueError(f"Faltan campos requeridos: {', '.join(missing)}")
        
        return True
    
    def generate(self, data: Dict[str, Any], output_filename: str) -> Path:
        """
        Genera el PDF de la carta de cobro.
        
        Args:
            data: Datos del documento (salida de Documento.to_pdf_data())
            output_filename: Nombre del archivo de salida
        
        Returns:
            Path: Ruta al archivo PDF generado
        """
        # Validar datos
        self.validate_data(data)
        
        # Determinar ruta de salida
        is_draft = data.get('es_borrador', False)
        output_path = self._get_output_path(output_filename, is_draft)
        
        # Crear documento PDF
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            topMargin=self.margin,
            bottomMargin=2 * cm,
            leftMargin=self.margin,
            rightMargin=self.margin,
            title=f"Carta de Cobro {data['numero_carta']}",
            author=data.get('sender_company_name', 'SEGUROS UNIÓN')
        )
        
        # Construir contenido
        story = []
        styles = self._create_styles()
        
        # Header (ciudad, fecha, número de carta)
        story.extend(self._build_header(data, styles))
        story.append(Spacer(1, 0.5 * cm))
        
        # Datos del cliente
        story.extend(self._build_recipient_section(data, styles))
        story.append(Spacer(1, 0.5 * cm))
        
        # Asunto
        story.extend(self._build_subject_section(data, styles))
        story.append(Spacer(1, 0.5 * cm))
        
        # Saludo
        story.append(Paragraph("Cordial saludo", styles['Normal']))
        story.append(Spacer(1, 0.3 * cm))
        
        # Contexto de cobro
        story.append(Paragraph(
            f"Cobro mensual correspondiente al mes de {data.get('mes_cobro', '')}",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.3 * cm))
        
        # Tabla de cobro
        story.append(self._build_billing_table(data))
        story.append(Spacer(1, 0.3 * cm))
        
        # Detalle de cuota
        story.extend(self._build_installment_detail(data, styles))
        story.append(Spacer(1, 0.3 * cm))
        
        # Definiciones
        story.extend(self._build_definitions(styles))
        story.append(Spacer(1, 0.3 * cm))
        
        # Instrucciones de pago
        story.extend(self._build_payment_instructions(data, styles))
        story.append(Spacer(1, 0.3 * cm))
        
        # Nota legal
        story.extend(self._build_legal_notice(data, styles))
        story.append(Spacer(1, 0.5 * cm))
        
        # Cierre
        story.append(Paragraph("REITERAMOS NUESTRA DISPOSICIÓN DE SERVICIO.", styles['Normal']))
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph("Atentamente,", styles['Normal']))
        story.append(Spacer(1, 1 * cm))
        
        # Firma
        story.extend(self._build_signature(data, styles))
        story.append(Spacer(1, 0.5 * cm))
        
        # Footer - Centrado
        footer_style = ParagraphStyle(
            name='CenteredSmall',
            parent=styles['Small'],
            alignment=TA_CENTER
        )
        story.append(Paragraph(
            f"{data.get('sender_address', '')} E-mail: {data.get('sender_email', '')}",
            footer_style
        ))
        
        # Marca de agua si es borrador
        if is_draft:
            doc.build(story, onFirstPage=self._add_watermark, onLaterPages=self._add_watermark)
        else:
            doc.build(story)
        
        # Log de auditoría
        self._log_generation(data, output_path, success=True)
        
        return output_path
    
    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Crea los estilos de párrafo personalizados."""
        styles = getSampleStyleSheet()
        
        # Modificar el estilo Normal para usar justificación
        styles['Normal'].alignment = TA_JUSTIFY
        styles['Normal'].fontName = 'Helvetica'
        styles['Normal'].fontSize = 10
        
        # Crear o sobrescribir estilos personalizados
        if 'CartaTitle' not in styles:
            styles.add(ParagraphStyle(
                name='CartaTitle',
                parent=styles['Heading1'],
                fontSize=14,
                textColor=colors.black,
                alignment=TA_LEFT,
                spaceAfter=6,
                fontName='Helvetica-Bold'
            ))
        
        if 'Small' not in styles:
            styles.add(ParagraphStyle(
                name='Small',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.black,
                alignment=TA_JUSTIFY  # También justificado para textos pequeños
            ))
        
        return styles
    
    def _build_header(self, data: Dict, styles) -> list:
        """Construye la sección de encabezado."""
        elements = []
        
        # Fecha alineada a la izquierda
        elements.append(Paragraph(
            f"{data['ciudad_emision']}, {data['fecha_emision']}",
            styles['Normal']
        ))
        
        # Número de carta alineado a la derecha
        elements.append(Paragraph(
            f"<b>CARTA COBRO N° {data['numero_carta']}</b>",
            ParagraphStyle(
                name='HeaderRight',
                parent=styles['Normal'],
                alignment=TA_RIGHT,
                fontSize=12,
                fontName='Helvetica-Bold'
            )
        ))
        
        return elements
    
    def _build_recipient_section(self, data: Dict, styles) -> list:
        """Construye la sección de datos del destinatario (sin dirección)."""
        elements = []
        
        elements.append(Paragraph("<b>Señores</b>", styles['Normal']))
        elements.append(Paragraph(
            f"{data['cliente_razon_social']}",
            styles['Normal']
        ))
        elements.append(Paragraph(
            f"{data['cliente_ciudad']}",
            styles['Normal']
        ))
        elements.append(Paragraph(
            f"NIT {data['cliente_nit']}",
            styles['Normal']
        ))
        
        return elements
    
    def _build_subject_section(self, data: Dict, styles) -> list:
        """Construye la sección de asunto."""
        elements = []
        
        elements.append(Paragraph(f"<b>ASUNTO:</b>", styles['Normal']))
        elements.append(Paragraph(
            f"<b>{data['poliza_tipo']} N° {data['poliza_numero']}</b>",
            styles['Normal']
        ))
        
        return elements
    
    def _build_billing_table(self, data: Dict) -> Table:
        """Construye la tabla de detalles de cobro con soporte para múltiples pólizas."""
        amounts = data['amounts_raw']
        campos_activos = data.get('campos_activos', {
            'prima': True,
            'impuesto': True,
            'otros_rubros': True
        })
        
        # Headers base (sin fechas de vigencia)
        headers = ['Ramo', 'Descripción', 'Doc.']
        col_widths = [3.5*cm, 3.5*cm, 2.5*cm]
        
        # Agregar columnas según campos activos
        if campos_activos.get('prima', True):
            headers.append('Prima')
            col_widths.append(2.8*cm)
        
        if campos_activos.get('otros_rubros', True):
            headers.append('Otros Rubros')
            col_widths.append(2.8*cm)
        
        if campos_activos.get('impuesto', True):
            headers.append('Impuesto')
            col_widths.append(2.5*cm)
        
        # Total siempre va al final
        headers.append('Total')
        col_widths.append(2.8*cm)
        
        # Inicializar tabla con headers
        table_data = [headers]
        
        # Obtener lista de pólizas (si existe múltiple, sino usar la póliza principal)
        polizas = data.get('polizas', [])
        
        if polizas:
            # Múltiples pólizas: crear una fila por cada póliza con sus propios montos (sin fechas)
            for poliza in polizas:
                # Descripción solo si checkbox está activo
                plan_text = poliza.get('plan', '') if poliza.get('check_plan', True) else ''
                
                row_data = [
                    poliza.get('tipo', 'VIDA GRUPO'),
                    plan_text,
                    poliza.get('numero', '')
                ]
                
                # Calcular total de esta póliza
                total_poliza = 0
                
                # Agregar montos según campos activos - USAR MONTOS DE CADA PÓLIZA
                if campos_activos.get('prima', True):
                    prima_val = poliza.get('prima', 0)
                    if poliza.get('check_prima', True):
                        row_data.append(f"${prima_val:,.2f}")
                        total_poliza += prima_val
                    else:
                        row_data.append("-")
                
                if campos_activos.get('otros_rubros', True):
                    otros_val = poliza.get('otros', 0)
                    if poliza.get('check_otros', True):
                        row_data.append(f"${otros_val:,.2f}")
                        total_poliza += otros_val
                    else:
                        row_data.append("-")
                
                if campos_activos.get('impuesto', True):
                    iva_val = poliza.get('iva', 0)
                    if poliza.get('check_iva', True):
                        row_data.append(f"${iva_val:,.2f}")
                        total_poliza += iva_val
                    else:
                        row_data.append("-")
                
                row_data.append(f"${total_poliza:,.2f}")
                table_data.append(row_data)
        else:
            # Póliza única (modo compatibilidad con versión anterior)
            row_data = [
                data.get('poliza_ramo', 'VIDA GRUPO'),
                data.get('plan_poliza', ''),
                data.get('documento_referencia', '')
            ]
            
            if campos_activos.get('prima', True):
                row_data.append(amounts['prima'])
            
            if campos_activos.get('otros_rubros', True):
                row_data.append(amounts['otros_rubros'])
            
            if campos_activos.get('impuesto', True):
                row_data.append(amounts['impuesto'])
            
            row_data.append(amounts['total'])
            table_data.append(row_data)
        
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            # Header style
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            
            # Data style
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        
        return table
    
    def _build_installment_detail(self, data: Dict, styles) -> list:
        """Construye el detalle de la cuota (sin línea de cuota mensual y vigencia)."""
        elements = []
        
        elements.append(Paragraph(
            f"<b>VALOR A PAGAR A FAVOR DE {data.get('payee_company_name', '')} - NIT {data.get('payee_company_nit', '')}</b>",
            styles['Normal']
        ))
        
        elements.append(Paragraph(
            f"<b>{data['amounts_raw']['total']}</b>",
            styles['CartaTitle']
        ))
        
        # Agregar campo de retorno si está habilitado
        if data.get('incluir_retorno', False) and data.get('retorno', '').strip():
            elements.append(Spacer(1, 0.2 * cm))
            elements.append(Paragraph(
                f"<b>RETORNO:</b> {data.get('retorno', '')}",
                styles['Normal']
            ))
        
        return elements
    
    def _build_definitions(self, styles) -> list:
        """Construye las definiciones de términos."""
        elements = []
        
        # Sin definiciones por ahora
        
        return elements
    
    def _build_payment_instructions(self, data: Dict, styles) -> list:
        """Construye las instrucciones de pago."""
        elements = []
        
        # Obtener link de pago dinámico o usar uno por defecto
        link_pago = data.get('payee_link_pago', 'WWW.SURA.COM').strip()
        if not link_pago:
            link_pago = 'WWW.SURA.COM'
        
        # Asegurar que el link tenga protocolo para ser clickeable
        if not link_pago.startswith(('http://', 'https://')):
            link_url = f'https://{link_pago}'
        else:
            link_url = link_pago
        
        # Crear párrafo con link azul clickeable
        elements.append(Paragraph(
            f'PUEDE REALIZAR SUS PAGOS POR PSE EN LA PAGINA WEB <a href="{link_url}" color="blue"><u>{link_pago}</u></a>',
            styles['Normal']
        ))
        
        elements.append(Paragraph(
            "<b>RECUERDE ENVIARNOS EL SOPORTE DE PAGO…</b>",
            styles['Normal']
        ))
        
        return elements
    
    def _build_legal_notice(self, data: Dict, styles) -> list:
        """Construye la nota legal."""
        elements = []
        
        legal_text = (
            "Nota: Las primas de seguros aquí relacionadas deben ser declaradas a nombre de la aseguradora "
            "que los expide. ART 1068 C. De C. La mora en el pago de la prima de la póliza o de los "
            "certificados o anexos que se expidan con fundamento en ella, producirá la terminación automática del contrato."
        )
        elements.append(Paragraph(legal_text, styles['Small']))
        
        elements.append(Paragraph(
            f"<b>F. Límite de pago: {data.get('fecha_limite_pago', '')}</b>",
            styles['Normal']
        ))
        
        return elements
    
    def _build_signature(self, data: Dict, styles) -> list:
        """Construye el bloque de firma."""
        elements = []
        
        elements.append(Paragraph(data['firmante_nombre'], styles['Normal']))
        
        cargo_completo = data['firmante_cargo']
        if data.get('firmante_iniciales'):
            cargo_completo += f" {data['firmante_iniciales']}"
        
        elements.append(Paragraph(cargo_completo, styles['Normal']))
        
        return elements
    
    def _add_watermark(self, canvas_obj, doc):
        """Agrega marca de agua BORRADOR al PDF."""
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica-Bold', 60)
        canvas_obj.setFillColorRGB(0.9, 0.9, 0.9, alpha=0.3)
        canvas_obj.translate(letter[0] / 2, letter[1] / 2)
        canvas_obj.rotate(45)
        canvas_obj.drawCentredString(0, 0, "BORRADOR")
        canvas_obj.restoreState()
