"""
New document creation page with form.
"""
from datetime import date
from decimal import Decimal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QPushButton,
    QScrollArea, QGroupBox, QLineEdit, QDateEdit, QComboBox, QSpinBox,
    QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QDate
from PyQt6.QtGui import QDoubleValidator

from gui.theme import Spacing, get_card_style, get_form_layout_spacing
from gui.widgets.validated_input import ValidatedLineEdit, NITInput, PhoneInput, CurrencyInput
from gui.widgets.toast import show_toast
from models.documento import Documento, MontosCobro
from models.asegurado import Asegurado
from models.poliza import Poliza
from generators.carta_cobro_generator import CartaCobroGenerator
from utils.payee_manager import payee_manager
from utils.versioning import version_manager
from utils.logger import get_logger

logger = get_logger(__name__)


class PDFGeneratorWorker(QThread):
    """Background worker for PDF generation."""
    
    finished = pyqtSignal(str)  # file_path
    error = pyqtSignal(str)  # error_message
    progress = pyqtSignal(int)  # progress percentage
    
    def __init__(self, documento: Documento):
        super().__init__()
        self.documento = documento
    
    def run(self):
        """Generate PDF in background thread."""
        try:
            self.progress.emit(25)
            generator = CartaCobroGenerator()
            
            self.progress.emit(50)
            output_path = generator.generate(self.documento)
            
            self.progress.emit(100)
            self.finished.emit(str(output_path))
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}", exc_info=True)
            self.error.emit(str(e))


class NewDocumentPage(QWidget):
    """
    Page for creating new collection letters.
    
    Provides a comprehensive form with validation and PDF generation.
    """
    
    document_created = pyqtSignal(str)  # Emits file path when document is created
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.worker = None
        self._build_ui()
        self._load_initial_data()
    
    def _build_ui(self):
        """Build the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        layout.setSpacing(Spacing.LG)
        
        # Header
        header = QLabel("Nueva Carta de Cobro")
        header.setProperty("styleClass", "title")
        layout.addWidget(header)
        
        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(Spacing.XL)
        
        # Build form sections
        form_layout.addWidget(self._build_emission_section())
        form_layout.addWidget(self._build_client_section())
        form_layout.addWidget(self._build_policy_section())
        form_layout.addWidget(self._build_amounts_section())
        form_layout.addWidget(self._build_payee_section())
        form_layout.addWidget(self._build_signature_section())
        
        form_layout.addStretch()
        
        scroll.setWidget(form_container)
        layout.addWidget(scroll, 1)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.clear_btn = QPushButton("Limpiar")
        self.clear_btn.clicked.connect(self._clear_form)
        button_layout.addWidget(self.clear_btn)
        
        self.generate_btn = QPushButton("Generar Carta")
        self.generate_btn.setProperty("styleClass", "primary")
        self.generate_btn.clicked.connect(self._generate_document)
        button_layout.addWidget(self.generate_btn)
        
        layout.addLayout(button_layout)
    
    def _build_emission_section(self) -> QGroupBox:
        """Build emission data section."""
        group = QGroupBox("Datos de Emisión")
        layout = QFormLayout()
        layout.setSpacing(Spacing.MD)
        layout.setHorizontalSpacing(Spacing.LG)
        
        # City
        self.city_input = QLineEdit("Medellín")
        layout.addRow("Ciudad:", self.city_input)
        
        # Emission date
        self.emission_date = QDateEdit(QDate.currentDate())
        self.emission_date.setCalendarPopup(True)
        self.emission_date.setDisplayFormat("dd/MM/yyyy")
        layout.addRow("Fecha de emisión:", self.emission_date)
        
        # Letter number (auto-generated, read-only)
        self.letter_number = QLineEdit()
        self.letter_number.setReadOnly(True)
        self.letter_number.setPlaceholderText("Se generará automáticamente")
        layout.addRow("Número de carta:", self.letter_number)
        
        # Collection month
        self.collection_month = QLineEdit()
        self.collection_month.setPlaceholderText("Ej: Octubre")
        layout.addRow("Mes de cobro:", self.collection_month)
        
        # Payment deadline
        self.deadline_date = QDateEdit(QDate.currentDate().addDays(5))
        self.deadline_date.setCalendarPopup(True)
        self.deadline_date.setDisplayFormat("dd/MM/yyyy")
        layout.addRow("Fecha límite de pago:", self.deadline_date)
        
        group.setLayout(layout)
        return group
    
    def _build_client_section(self) -> QGroupBox:
        """Build client data section."""
        group = QGroupBox("Datos del Asegurado")
        layout = QFormLayout()
        layout.setSpacing(Spacing.MD)
        layout.setHorizontalSpacing(Spacing.LG)
        
        # Business name
        self.client_name = ValidatedLineEdit(
            validator_func=lambda x: (len(x) > 0, "Nombre requerido")
        )
        layout.addRow("Razón social:", self.client_name)
        
        # NIT
        self.client_nit = NITInput()
        layout.addRow("NIT:", self.client_nit)
        
        # Address
        self.client_address = QLineEdit()
        layout.addRow("Dirección:", self.client_address)
        
        # Phone
        self.client_phone = PhoneInput()
        layout.addRow("Teléfono:", self.client_phone)
        
        # City
        self.client_city = QLineEdit()
        layout.addRow("Ciudad:", self.client_city)
        
        group.setLayout(layout)
        return group
    
    def _build_policy_section(self) -> QGroupBox:
        """Build policy data section."""
        group = QGroupBox("Datos de la Póliza")
        layout = QFormLayout()
        layout.setSpacing(Spacing.MD)
        layout.setHorizontalSpacing(Spacing.LG)
        
        # Policy number
        self.policy_number = QLineEdit()
        layout.addRow("Número de póliza:", self.policy_number)
        
        # Policy type
        self.policy_type = QLineEdit("POLIZA DE VIDA GRUPO")
        layout.addRow("Tipo de póliza:", self.policy_type)
        
        # Plan
        self.policy_plan = QLineEdit()
        self.policy_plan.setPlaceholderText("Ej: 06  3144016")
        layout.addRow("Plan póliza:", self.policy_plan)
        
        # Reference document
        self.reference_doc = QLineEdit()
        layout.addRow("Documento referencia:", self.reference_doc)
        
        # Installment number
        self.installment_number = QSpinBox()
        self.installment_number.setRange(1, 999)
        self.installment_number.setValue(1)
        layout.addRow("Número de cuota:", self.installment_number)
        
        # Validity start
        self.validity_start = QDateEdit(QDate.currentDate())
        self.validity_start.setCalendarPopup(True)
        self.validity_start.setDisplayFormat("dd/MM/yyyy")
        layout.addRow("Vigencia inicio:", self.validity_start)
        
        # Validity end
        self.validity_end = QDateEdit(QDate.currentDate().addMonths(1))
        self.validity_end.setCalendarPopup(True)
        self.validity_end.setDisplayFormat("dd/MM/yyyy")
        layout.addRow("Vigencia fin:", self.validity_end)
        
        group.setLayout(layout)
        return group
    
    def _build_amounts_section(self) -> QGroupBox:
        """Build amounts section."""
        group = QGroupBox("Montos")
        layout = QFormLayout()
        layout.setSpacing(Spacing.MD)
        layout.setHorizontalSpacing(Spacing.LG)
        
        self.premium = CurrencyInput("Prima (COP)")
        layout.addRow("Prima:", self.premium)
        
        self.other_amounts = CurrencyInput("Otros rubros (COP)")
        layout.addRow("Otros rubros:", self.other_amounts)
        
        self.tax = CurrencyInput("Impuesto (COP)")
        layout.addRow("Impuesto:", self.tax)
        
        self.external_value = CurrencyInput("Valor externo (COP)")
        layout.addRow("Valor externo:", self.external_value)
        
        # Total (read-only, calculated)
        self.total_label = QLabel("$0,00")
        self.total_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addRow("Total:", self.total_label)
        
        # Connect signals to update total
        self.premium.valueChanged.connect(self._update_total)
        self.other_amounts.valueChanged.connect(self._update_total)
        self.tax.valueChanged.connect(self._update_total)
        self.external_value.valueChanged.connect(self._update_total)
        
        group.setLayout(layout)
        return group
    
    def _build_payee_section(self) -> QGroupBox:
        """Build payee selection section."""
        group = QGroupBox("Aseguradora Beneficiaria")
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.MD)
        
        # Combo box for payee selection
        select_layout = QHBoxLayout()
        
        self.payee_combo = QComboBox()
        self.payee_combo.setMinimumWidth(300)
        select_layout.addWidget(self.payee_combo, 1)
        
        manage_btn = QPushButton("Gestionar")
        manage_btn.clicked.connect(self._manage_payees)
        select_layout.addWidget(manage_btn)
        
        layout.addLayout(select_layout)
        
        # Display NIT
        self.payee_nit_label = QLabel()
        self.payee_nit_label.setProperty("styleClass", "muted")
        layout.addWidget(self.payee_nit_label)
        
        # Connect combo change
        self.payee_combo.currentIndexChanged.connect(self._on_payee_changed)
        
        group.setLayout(layout)
        return group
    
    def _build_signature_section(self) -> QGroupBox:
        """Build signature section."""
        group = QGroupBox("Firma")
        layout = QFormLayout()
        layout.setSpacing(Spacing.MD)
        layout.setHorizontalSpacing(Spacing.LG)
        
        self.signer_name = QLineEdit()
        layout.addRow("Nombre del firmante:", self.signer_name)
        
        self.signer_position = QLineEdit()
        layout.addRow("Cargo:", self.signer_position)
        
        self.signer_initials = QLineEdit()
        self.signer_initials.setMaxLength(10)
        self.signer_initials.setPlaceholderText("Opcional")
        layout.addRow("Iniciales:", self.signer_initials)
        
        group.setLayout(layout)
        return group
    
    def _load_initial_data(self):
        """Load initial data into form."""
        # Load payees
        self._refresh_payees()
        
        # Generate letter number
        self.letter_number.setText(version_manager.get_next_numero_carta())
    
    def _refresh_payees(self):
        """Refresh payee combo box."""
        self.payee_combo.clear()
        payees = payee_manager.get_all_payees()
        
        for payee in payees:
            self.payee_combo.addItem(
                f"{payee['name']} - Usada {payee['usage_count']} veces",
                userData=payee
            )
        
        if payees:
            self._on_payee_changed(0)
    
    def _on_payee_changed(self, index: int):
        """Handle payee selection change."""
        if index >= 0:
            payee = self.payee_combo.itemData(index)
            if payee:
                self.payee_nit_label.setText(f"NIT: {payee['nit']}")
    
    def _manage_payees(self):
        """Open payee management dialog."""
        # Signal parent to switch to payee management page
        if self.parent() and hasattr(self.parent(), 'navigate_to_page'):
            self.parent().navigate_to_page(1)
    
    def _update_total(self):
        """Update total amount display."""
        total = (
            self.premium.value() +
            self.other_amounts.value() +
            self.tax.value() +
            self.external_value.value()
        )
        
        from validators.field_validators import CurrencyFormatter
        self.total_label.setText(CurrencyFormatter.to_colombian_format(total))
    
    def _validate_form(self) -> tuple[bool, str]:
        """
        Validate all form fields.
        
        Returns:
            (is_valid, error_message)
        """
        # Check required fields
        if not self.city_input.text().strip():
            return False, "Ciudad es requerida"
        
        if not self.collection_month.text().strip():
            return False, "Mes de cobro es requerido"
        
        if not self.client_name.text().strip():
            return False, "Razón social del asegurado es requerida"
        
        if not self.client_nit.is_valid() or not self.client_nit.text().strip():
            return False, "NIT del asegurado es inválido o faltante"
        
        if not self.client_address.text().strip():
            return False, "Dirección del asegurado es requerida"
        
        if not self.client_phone.is_valid() or not self.client_phone.text().strip():
            return False, "Teléfono del asegurado es inválido o faltante"
        
        if not self.client_city.text().strip():
            return False, "Ciudad del asegurado es requerida"
        
        if not self.policy_number.text().strip():
            return False, "Número de póliza es requerido"
        
        if self.premium.value() <= 0:
            return False, "Prima debe ser mayor a cero"
        
        if self.payee_combo.currentIndex() < 0:
            return False, "Debe seleccionar una aseguradora beneficiaria"
        
        if not self.signer_name.text().strip():
            return False, "Nombre del firmante es requerido"
        
        if not self.signer_position.text().strip():
            return False, "Cargo del firmante es requerido"
        
        return True, ""
    
    def _generate_document(self):
        """Generate PDF document."""
        # Validate form
        is_valid, error_msg = self._validate_form()
        if not is_valid:
            show_toast(self, f"Error: {error_msg}", "error")
            return
        
        try:
            # Build documento model
            documento = self._build_documento()
            
            # Disable UI
            self.generate_btn.setEnabled(False)
            self.clear_btn.setEnabled(False)
            self.progress_bar.show()
            self.progress_bar.setValue(0)
            
            # Start background worker
            self.worker = PDFGeneratorWorker(documento)
            self.worker.finished.connect(self._on_generation_finished)
            self.worker.error.connect(self._on_generation_error)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.start()
            
        except Exception as e:
            logger.error(f"Failed to create document: {e}", exc_info=True)
            show_toast(self, f"Error: {str(e)}", "error")
    
    def _build_documento(self) -> Documento:
        """Build Documento model from form data."""
        # Asegurado
        asegurado = Asegurado(
            razon_social=self.client_name.text().strip(),
            nit=self.client_nit.text().strip(),
            direccion=self.client_address.text().strip(),
            telefono=self.client_phone.text().strip(),
            ciudad=self.client_city.text().strip()
        )
        
        # Poliza
        poliza = Poliza(
            numero=self.policy_number.text().strip(),
            tipo=self.policy_type.text().strip(),
            plan_poliza=self.policy_plan.text().strip(),
            documento_referencia=self.reference_doc.text().strip(),
            cuota_numero=self.installment_number.value(),
            vigencia_inicio=self.validity_start.date().toPyDate(),
            vigencia_fin=self.validity_end.date().toPyDate()
        )
        
        # Montos
        montos = MontosCobro(
            prima=Decimal(str(self.premium.value())),
            otros_rubros=Decimal(str(self.other_amounts.value())),
            impuesto=Decimal(str(self.tax.value())),
            valor_externo=Decimal(str(self.external_value.value()))
        )
        
        # Get selected payee
        payee = self.payee_combo.currentData()
        
        # Documento
        documento = Documento(
            ciudad_emision=self.city_input.text().strip(),
            fecha_emision=self.emission_date.date().toPyDate(),
            numero_carta=self.letter_number.text().strip(),
            mes_cobro=self.collection_month.text().strip(),
            fecha_limite_pago=self.deadline_date.date().toPyDate(),
            asegurado=asegurado,
            poliza=poliza,
            montos=montos,
            payee_company_name=payee['name'],
            payee_company_nit=payee['nit'],
            firmante_nombre=self.signer_name.text().strip(),
            firmante_cargo=self.signer_position.text().strip(),
            firmante_iniciales=self.signer_initials.text().strip() or None,
            es_borrador=False
        )
        
        return documento
    
    def _on_generation_finished(self, file_path: str):
        """Handle successful generation."""
        self.progress_bar.hide()
        self.generate_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        
        show_toast(self, f"Carta generada exitosamente", "success")
        self.document_created.emit(file_path)
        
        # Increment payee usage
        payee = self.payee_combo.currentData()
        if payee:
            payee_manager.increment_usage(payee['name'])
            self._refresh_payees()
        
        # Ask if user wants to clear form
        from PyQt6.QtWidgets import QMessageBox
        response = QMessageBox.question(
            self,
            "Carta Generada",
            "Carta generada exitosamente.\n\n¿Desea crear otra carta?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if response == QMessageBox.StandardButton.Yes:
            self._clear_form()
    
    def _on_generation_error(self, error_msg: str):
        """Handle generation error."""
        self.progress_bar.hide()
        self.generate_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        
        show_toast(self, f"Error al generar: {error_msg}", "error")
    
    def _clear_form(self):
        """Clear all form fields."""
        # Emission
        self.city_input.setText("Medellín")
        self.emission_date.setDate(QDate.currentDate())
        self.letter_number.setText(version_manager.get_next_numero_carta())
        self.collection_month.clear()
        self.deadline_date.setDate(QDate.currentDate().addDays(5))
        
        # Client
        self.client_name.setText("")
        self.client_nit.setText("")
        self.client_address.clear()
        self.client_phone.setText("")
        self.client_city.clear()
        
        # Policy
        self.policy_number.clear()
        self.policy_type.setText("POLIZA DE VIDA GRUPO")
        self.policy_plan.clear()
        self.reference_doc.clear()
        self.installment_number.setValue(1)
        self.validity_start.setDate(QDate.currentDate())
        self.validity_end.setDate(QDate.currentDate().addMonths(1))
        
        # Amounts
        self.premium.setValue(0)
        self.other_amounts.setValue(0)
        self.tax.setValue(0)
        self.external_value.setValue(0)
        
        # Signature
        self.signer_name.clear()
        self.signer_position.clear()
        self.signer_initials.clear()
        
        show_toast(self, "Formulario limpiado", "info")
