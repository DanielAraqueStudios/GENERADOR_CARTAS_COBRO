"""
GUI Simple para Generador de Cartas de Cobro
Todo en un solo archivo - PyQt6
"""
import sys
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QTextEdit,
    QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox, QGroupBox,
    QFormLayout, QHeaderView, QDialog, QDialogButtonBox, QScrollArea, QCheckBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIcon

# Imports del proyecto
from models.documento import Documento, Asegurado, Poliza, MontosCobro
from generators.carta_cobro_generator import CartaCobroGenerator
from utils.payee_manager import payee_manager
from utils.config import config
from utils.logger import get_logger

logger = get_logger(__name__)


class AseguradoraDialog(QDialog):
    """Diálogo para agregar/editar aseguradoras."""
    
    def __init__(self, parent=None, nombre="", nit="", link_pago=""):
        super().__init__(parent)
        self.setWindowTitle("Aseguradora")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QFormLayout(self)
        
        # Campos
        self.nombre_input = QLineEdit(nombre)
        self.nit_input = QLineEdit(nit)
        self.link_pago_input = QLineEdit(link_pago)
        self.link_pago_input.setPlaceholderText("Ej: WWW.SURA.COM")
        
        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("NIT:", self.nit_input)
        layout.addRow("Link de Pago:", self.link_pago_input)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def get_data(self):
        """Retorna los datos ingresados."""
        return {
            'nombre': self.nombre_input.text().strip(),
            'nit': self.nit_input.text().strip(),
            'link_pago': self.link_pago_input.text().strip()
        }


class PolizaDialog(QDialog):
    """Diálogo para agregar/editar pólizas."""
    
    def __init__(self, parent=None, numero="", tipo="VIDA GRUPO", plan="", fecha_inicio=None, fecha_fin=None, 
                 prima="0", iva="0", otros="0", check_prima=True, check_iva=True, check_otros=True, check_plan=True):
        super().__init__(parent)
        self.setWindowTitle("Agregar Póliza")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        main_layout = QVBoxLayout(self)
        
        # Sección de datos de la póliza
        group_datos = QGroupBox("Datos de la Póliza")
        layout = QFormLayout()
        
        # Campos básicos
        self.numero_input = QLineEdit(numero)
        self.numero_input.setPlaceholderText("Ej: VG-2026-0001")
        
        self.tipo_input = QLineEdit(tipo)
        self.tipo_input.setPlaceholderText("Ej: VIDA GRUPO, SOAT, etc.")
        
        # Descripción con checkbox
        layout_plan = QHBoxLayout()
        self.check_plan = QCheckBox("")
        self.check_plan.setChecked(check_plan)
        self.plan_input = QLineEdit(plan)
        self.plan_input.setPlaceholderText("Ej: Plan Empresarial Plus")
        self.plan_input.setEnabled(check_plan)
        self.check_plan.stateChanged.connect(lambda: self.plan_input.setEnabled(self.check_plan.isChecked()))
        layout_plan.addWidget(self.check_plan)
        layout_plan.addWidget(self.plan_input)
        
        self.fecha_inicio_input = QDateEdit()
        self.fecha_inicio_input.setCalendarPopup(True)
        self.fecha_inicio_input.setDate(fecha_inicio if fecha_inicio else QDate.currentDate())
        
        self.fecha_fin_input = QDateEdit()
        self.fecha_fin_input.setCalendarPopup(True)
        self.fecha_fin_input.setDate(fecha_fin if fecha_fin else QDate.currentDate().addYears(1))
        
        layout.addRow("Número de Póliza:", self.numero_input)
        layout.addRow("Ramo:", self.tipo_input)
        layout.addRow("Descripción:", layout_plan)
        layout.addRow("Inicio de Vigencia:", self.fecha_inicio_input)
        layout.addRow("Fin de Vigencia:", self.fecha_fin_input)
        
        group_datos.setLayout(layout)
        main_layout.addWidget(group_datos)
        
        # Sección de montos
        group_montos = QGroupBox("Montos de Cobro")
        layout_montos = QVBoxLayout()
        
        # Prima
        layout_prima = QHBoxLayout()
        self.check_prima = QCheckBox("Prima ($):")
        self.check_prima.setChecked(check_prima)
        self.check_prima.setStyleSheet("QCheckBox { font-weight: bold; }")
        self.prima_input = QLineEdit(prima)
        self.prima_input.setEnabled(check_prima)
        self.check_prima.stateChanged.connect(lambda: self.prima_input.setEnabled(self.check_prima.isChecked()))
        self.prima_input.textChanged.connect(self.calcular_total)
        layout_prima.addWidget(self.check_prima, 1)
        layout_prima.addWidget(self.prima_input, 2)
        layout_montos.addLayout(layout_prima)
        
        # IVA
        layout_iva = QHBoxLayout()
        self.check_iva = QCheckBox("IVA ($):")
        self.check_iva.setChecked(check_iva)
        self.check_iva.setStyleSheet("QCheckBox { font-weight: bold; }")
        self.iva_input = QLineEdit(iva)
        self.iva_input.setEnabled(check_iva)
        self.check_iva.stateChanged.connect(lambda: self.iva_input.setEnabled(self.check_iva.isChecked()))
        self.iva_input.textChanged.connect(self.calcular_total)
        layout_iva.addWidget(self.check_iva, 1)
        layout_iva.addWidget(self.iva_input, 2)
        layout_montos.addLayout(layout_iva)
        
        # Otros
        layout_otros = QHBoxLayout()
        self.check_otros = QCheckBox("Otros Conceptos ($):")
        self.check_otros.setChecked(check_otros)
        self.check_otros.setStyleSheet("QCheckBox { font-weight: bold; }")
        self.otros_input = QLineEdit(otros)
        self.otros_input.setEnabled(check_otros)
        self.check_otros.stateChanged.connect(lambda: self.otros_input.setEnabled(self.check_otros.isChecked()))
        self.otros_input.textChanged.connect(self.calcular_total)
        layout_otros.addWidget(self.check_otros, 1)
        layout_otros.addWidget(self.otros_input, 2)
        layout_montos.addLayout(layout_otros)
        
        # Total
        layout_total = QHBoxLayout()
        label_total = QLabel("TOTAL:")
        label_total.setStyleSheet("QLabel { font-weight: bold; }")
        self.total_input = QLineEdit("0")
        self.total_input.setReadOnly(True)
        self.total_input.setStyleSheet("QLineEdit { background-color: #e8f5e9; font-weight: bold; }")
        layout_total.addWidget(label_total, 1)
        layout_total.addWidget(self.total_input, 2)
        layout_montos.addLayout(layout_total)
        
        group_montos.setLayout(layout_montos)
        main_layout.addWidget(group_montos)
        
        # Calcular total inicial
        self.calcular_total()
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)
    
    def calcular_total(self):
        """Calcula el total sumando los montos activos."""
        total = 0
        
        if self.check_prima.isChecked():
            try:
                total += float(self.prima_input.text().replace(',', ''))
            except ValueError:
                pass
        
        if self.check_iva.isChecked():
            try:
                total += float(self.iva_input.text().replace(',', ''))
            except ValueError:
                pass
        
        if self.check_otros.isChecked():
            try:
                total += float(self.otros_input.text().replace(',', ''))
            except ValueError:
                pass
        
        self.total_input.setText(f"{total:,.2f}")
    
    def get_data(self):
        """Retorna los datos ingresados."""
        return {
            'numero': self.numero_input.text().strip(),
            'tipo': self.tipo_input.text().strip(),
            'plan': self.plan_input.text().strip(),
            'fecha_inicio': self.fecha_inicio_input.date(),
            'fecha_fin': self.fecha_fin_input.date(),
            'prima': self.prima_input.text().strip(),
            'iva': self.iva_input.text().strip(),
            'otros': self.otros_input.text().strip(),
            'check_prima': self.check_prima.isChecked(),
            'check_iva': self.check_iva.isChecked(),
            'check_otros': self.check_otros.isChecked(),
            'check_plan': self.check_plan.isChecked()
        }


class GeneradorCartasGUI(QMainWindow):
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{config.APP_NAME} - v{config.APP_VERSION}")
        self.setMinimumSize(1000, 700)
        
        # Aplicar paleta de colores moderna DARK MODE
        self.setStyleSheet("""
            /* Colores principales - DARK MODE */
            QMainWindow {
                background-color: #1a1a1a;
            }
            
            /* Pestañas principales */
            QTabWidget::pane {
                border: none;
                background-color: #2d2d2d;
                border-radius: 8px;
            }
            
            QTabBar::tab {
                background-color: #383838;
                color: #b0b0b0;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            
            QTabBar::tab:selected {
                background-color: #1e88e5;
                color: #ffffff;
                font-weight: 600;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #505050;
                color: #e0e0e0;
            }
            
            /* Sub-pestañas */
            QTabWidget QTabWidget::pane {
                background-color: #252525;
                border: 1px solid #404040;
            }
            
            QTabWidget QTabBar::tab {
                background-color: #333333;
                color: #b0b0b0;
                padding: 10px 20px;
                font-size: 13px;
            }
            
            QTabWidget QTabBar::tab:selected {
                background-color: #42a5f5;
                color: #ffffff;
            }
            
            /* Labels y títulos */
            QLabel {
                color: #e0e0e0;
                font-size: 13px;
            }
            
            QGroupBox {
                background-color: #2d2d2d;
                border: 2px solid #1e88e5;
                border-radius: 10px;
                margin-top: 12px;
                padding: 20px;
                font-size: 14px;
                font-weight: 600;
                color: #64b5f6;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 15px;
                background-color: #1e88e5;
                border-radius: 6px;
                color: #ffffff;
            }
            
            /* Inputs */
            QLineEdit, QComboBox, QDateEdit, QSpinBox {
                background-color: #383838;
                border: 2px solid #505050;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                color: #ffffff;
            }
            
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #42a5f5;
                background-color: #404040;
            }
            
            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
                border: 2px solid #64b5f6;
                background-color: #3d3d3d;
            }
            
            QLineEdit[readOnly="true"] {
                background-color: #2d2d2d;
                color: #b0b0b0;
            }
            
            QLineEdit::placeholder {
                color: #707070;
            }
            
            /* ComboBox dropdown */
            QComboBox::drop-down {
                border: none;
                width: 30px;
                background-color: transparent;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #64b5f6;
                margin-right: 8px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #383838;
                color: #ffffff;
                selection-background-color: #1e88e5;
                border: 1px solid #505050;
            }
            
            /* Botones estándar */
            QPushButton {
                background-color: #455a64;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #546e7a;
            }
            
            QPushButton:pressed {
                background-color: #37474f;
            }
            
            /* Tabla */
            QTableWidget {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                gridline-color: #404040;
                font-size: 13px;
                color: #e0e0e0;
            }
            
            QTableWidget::item {
                padding: 8px;
                color: #e0e0e0;
            }
            
            QTableWidget::item:selected {
                background-color: #1e88e5;
                color: #ffffff;
            }
            
            QHeaderView::section {
                background-color: #1e88e5;
                color: #ffffff;
                padding: 10px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }
            
            QTableWidget::item:alternate {
                background-color: #333333;
            }
            
            /* ScrollBar */
            QScrollBar:vertical {
                background: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: #505050;
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #606060;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            /* Diálogos */
            QDialog {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            
            /* Scroll Area */
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            
            /* Message Box */
            QMessageBox {
                background-color: #2d2d2d;
            }
            
            QMessageBox QLabel {
                color: #e0e0e0;
            }
        """)
        
        # Widget central con pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Carpeta de salida predeterminada (DEBE IR ANTES de crear pestañas)
        self.output_folder = Path("output")
        
        # Crear pestañas
        self.crear_tab_nueva_carta()
        self.crear_tab_aseguradoras()
        
        # Cargar datos iniciales
        self.cargar_aseguradoras()
        
        logger.info("GUI Simple iniciada")
    
    def crear_tab_nueva_carta(self):
        """Crea la pestaña para generar nueva carta."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Título
        titulo = QLabel("📄 Nueva Carta de Cobro")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        titulo.setFont(font)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            color: #ffffff;
            background-color: #1e88e5;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
        """)
        layout.addWidget(titulo)
        
        # Sub-pestañas para organizar mejor
        self.sub_tabs = QTabWidget()
        
        # PESTAÑA 1: Emisión y Asegurado
        self.crear_tab_emision_asegurado()
        
        # PESTAÑA 2: Póliza y Montos
        self.crear_tab_poliza_montos()
        
        # PESTAÑA 3: Aseguradora y Firma
        self.crear_tab_aseguradora_firma()
        
        layout.addWidget(self.sub_tabs)
        
        # Botones de acción al final (siempre visibles)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_ejemplo = QPushButton("📝 Llenar Ejemplo")
        btn_ejemplo.setFixedHeight(45)
        btn_ejemplo.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #42a5f5, stop:1 #1e88e5);
                color: white;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #64b5f6, stop:1 #2196f3);
            }
            QPushButton:pressed {
                background: #1565c0;
            }
        """)
        btn_ejemplo.clicked.connect(self.llenar_ejemplo)
        
        btn_limpiar = QPushButton("🗑️ Limpiar Todo")
        btn_limpiar.setFixedHeight(45)
        btn_limpiar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ef5350, stop:1 #e53935);
                color: white;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f44336, stop:1 #d32f2f);
            }
            QPushButton:pressed {
                background: #c62828;
            }
        """)
        btn_limpiar.clicked.connect(self.limpiar_formulario)
        
        btn_generar = QPushButton("📄 Generar PDF")
        btn_generar.setFixedHeight(45)
        btn_generar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #66bb6a, stop:1 #43a047);
                color: white;
                padding: 10px 30px;
                font-size: 15px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #81c784, stop:1 #4caf50);
            }
            QPushButton:pressed {
                background: #2e7d32;
            }
        """)
        btn_generar.clicked.connect(self.generar_pdf)
        
        btn_layout.addWidget(btn_ejemplo)
        btn_layout.addWidget(btn_limpiar)
        btn_layout.addWidget(btn_generar)
        layout.addLayout(btn_layout)
        
        self.tabs.addTab(tab, "📝 Nueva Carta")
    
    def crear_tab_emision_asegurado(self):
        """Crea la sub-pestaña de Emisión y Asegurado."""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)
        
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # === DATOS DE EMISIÓN ===
        group_emision = QGroupBox("📅 Datos de Emisión")
        group_emision.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        form_emision = QFormLayout()
        form_emision.setSpacing(10)
        
        self.ciudad_emision = QLineEdit("MEDELLIN")
        self.ciudad_emision.setMinimumHeight(35)
        
        self.fecha_emision = QDateEdit()
        self.fecha_emision.setCalendarPopup(True)
        self.fecha_emision.setDate(QDate.currentDate())
        self.fecha_emision.setMinimumHeight(35)
        
        self.numero_carta = QLineEdit()
        self.numero_carta.setPlaceholderText("Ej: 15434 - 2025")
        self.numero_carta.setMinimumHeight(35)
        
        self.mes_cobro = QComboBox()
        self.mes_cobro.addItems([
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.mes_cobro.setCurrentText(QDate.currentDate().toString("MMMM").capitalize())
        self.mes_cobro.setMinimumHeight(35)
        
        self.fecha_limite_pago = QDateEdit()
        self.fecha_limite_pago.setCalendarPopup(True)
        self.fecha_limite_pago.setDate(QDate.currentDate().addDays(30))
        self.fecha_limite_pago.setMinimumHeight(35)
        
        form_emision.addRow("Ciudad de Emisión:", self.ciudad_emision)
        form_emision.addRow("Fecha de Emisión:", self.fecha_emision)
        form_emision.addRow("Número de Carta:", self.numero_carta)
        form_emision.addRow("Mes de Cobro:", self.mes_cobro)
        form_emision.addRow("Fecha Límite Pago:", self.fecha_limite_pago)
        group_emision.setLayout(form_emision)
        layout.addWidget(group_emision)
        
        # === DATOS DEL ASEGURADO (CLIENTE) ===
        group_asegurado = QGroupBox("👤 Datos del Asegurado (Cliente)")
        group_asegurado.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        form_asegurado = QFormLayout()
        form_asegurado.setSpacing(10)
        
        self.nombre_asegurado = QLineEdit()
        self.nombre_asegurado.setMinimumHeight(35)
        self.nombre_asegurado.setPlaceholderText("Nombre completo del asegurado")
        
        self.nit_asegurado = QLineEdit()
        self.nit_asegurado.setMinimumHeight(35)
        self.nit_asegurado.setPlaceholderText("123456789-0")
        
        self.direccion_asegurado = QLineEdit()
        self.direccion_asegurado.setMinimumHeight(35)
        self.direccion_asegurado.setPlaceholderText("Dirección completa")
        
        self.telefono_asegurado = QLineEdit()
        self.telefono_asegurado.setMinimumHeight(35)
        self.telefono_asegurado.setPlaceholderText("3001234567")
        
        self.ciudad_asegurado = QLineEdit()
        self.ciudad_asegurado.setMinimumHeight(35)
        self.ciudad_asegurado.setPlaceholderText("Ciudad del asegurado")
        
        form_asegurado.addRow("Nombre Completo:", self.nombre_asegurado)
        form_asegurado.addRow("NIT:", self.nit_asegurado)
        form_asegurado.addRow("Dirección:", self.direccion_asegurado)
        form_asegurado.addRow("Teléfono:", self.telefono_asegurado)
        form_asegurado.addRow("Ciudad:", self.ciudad_asegurado)
        group_asegurado.setLayout(form_asegurado)
        layout.addWidget(group_asegurado)
        
        layout.addStretch()
        
        self.sub_tabs.addTab(scroll, "1️⃣ Emisión y Cliente")
    
    def crear_tab_poliza_montos(self):
        """Crea la sub-pestaña de Póliza y Montos."""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)
        
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # === DATOS DE LAS PÓLIZAS (MÚLTIPLES) ===
        group_poliza = QGroupBox("📋 Datos de las Pólizas")
        group_poliza.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        layout_polizas = QVBoxLayout()
        layout_polizas.setSpacing(10)
        
        # Botones para gestionar pólizas
        btn_layout = QHBoxLayout()
        btn_agregar_poliza = QPushButton("➕ Agregar Póliza")
        btn_agregar_poliza.setMinimumHeight(35)
        btn_agregar_poliza.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_agregar_poliza.clicked.connect(self.agregar_poliza)
        
        btn_eliminar_poliza = QPushButton("➖ Eliminar Póliza")
        btn_eliminar_poliza.setMinimumHeight(35)
        btn_eliminar_poliza.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        btn_eliminar_poliza.clicked.connect(self.eliminar_poliza)
        
        btn_layout.addWidget(btn_agregar_poliza)
        btn_layout.addWidget(btn_eliminar_poliza)
        btn_layout.addStretch()
        layout_polizas.addLayout(btn_layout)
        
        # Tabla de pólizas (sin fechas de vigencia)
        self.tabla_polizas = QTableWidget()
        self.tabla_polizas.setColumnCount(7)
        self.tabla_polizas.setHorizontalHeaderLabels(["Número", "Tipo", "Descripción", "Prima", "IVA", "Otros", "Total"])
        self.tabla_polizas.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_polizas.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_polizas.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabla_polizas.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_polizas.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_polizas.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_polizas.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_polizas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_polizas.setMinimumHeight(150)
        self.tabla_polizas.setMaximumHeight(250)
        layout_polizas.addWidget(self.tabla_polizas)
        
        # Lista interna para almacenar las pólizas
        self.polizas_list = []
        
        group_poliza.setLayout(layout_polizas)
        layout.addWidget(group_poliza)
        
        # === TOTAL GENERAL (SUMA DE TODAS LAS PÓLIZAS) ===
        group_total = QGroupBox("💵 Total General")
        group_total.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        layout_total_general = QVBoxLayout()
        
        self.total_general = QLineEdit("$0.00")
        self.total_general.setMinimumHeight(50)
        self.total_general.setReadOnly(True)
        self.total_general.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2e7d32, stop:1 #1b5e20);
                font-weight: bold; 
                font-size: 24px;
                color: #a5d6a7;
                border: 3px solid #66bb6a;
                border-radius: 8px;
                padding: 10px;
                text-align: center;
            }
        """)
        layout_total_general.addWidget(self.total_general)
        group_total.setLayout(layout_total_general)
        layout.addWidget(group_total)
        
        layout.addStretch()
        
        self.sub_tabs.addTab(scroll, "2️⃣ Póliza y Montos")
    
    def crear_tab_aseguradora_firma(self):
        """Crea la sub-pestaña de Aseguradora y Firma."""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)
        
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # === ASEGURADORA (A FAVOR DE) ===
        group_aseguradora = QGroupBox("🏢 Pagar a Favor De (Aseguradora)")
        group_aseguradora.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        form_aseguradora = QFormLayout()
        form_aseguradora.setSpacing(10)
        
        self.aseguradora_combo = QComboBox()
        self.aseguradora_combo.setEditable(True)
        self.aseguradora_combo.setMinimumHeight(35)
        self.aseguradora_combo.currentTextChanged.connect(self.on_aseguradora_changed)
        
        self.nit_aseguradora = QLineEdit()
        self.nit_aseguradora.setMinimumHeight(35)
        self.nit_aseguradora.setPlaceholderText("NIT de la aseguradora")
        
        form_aseguradora.addRow("Nombre Aseguradora:", self.aseguradora_combo)
        form_aseguradora.addRow("NIT Aseguradora:", self.nit_aseguradora)
        group_aseguradora.setLayout(form_aseguradora)
        layout.addWidget(group_aseguradora)
        
        # === RETORNO ===
        group_retorno = QGroupBox("🔄 Retorno")
        group_retorno.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        layout_retorno = QVBoxLayout()
        layout_retorno.setSpacing(10)
        
        # Checkbox para incluir retorno
        layout_retorno_check = QHBoxLayout()
        self.check_incluir_retorno = QCheckBox("Incluir campo de Retorno en el PDF")
        self.check_incluir_retorno.setStyleSheet("QCheckBox { font-size: 13px; }")
        layout_retorno_check.addWidget(self.check_incluir_retorno)
        layout_retorno.addLayout(layout_retorno_check)
        
        # Campo de texto para el retorno
        label_retorno = QLabel("Valor de Retorno:")
        label_retorno.setStyleSheet("QLabel { font-weight: bold; }")
        self.retorno_input = QLineEdit()
        self.retorno_input.setMinimumHeight(35)
        self.retorno_input.setPlaceholderText("Ej: Realizar retorno a cuenta")
        self.retorno_input.setEnabled(False)
        
        # Conectar checkbox con el input
        self.check_incluir_retorno.stateChanged.connect(lambda: self.retorno_input.setEnabled(self.check_incluir_retorno.isChecked()))
        
        layout_retorno.addWidget(label_retorno)
        layout_retorno.addWidget(self.retorno_input)
        
        group_retorno.setLayout(layout_retorno)
        layout.addWidget(group_retorno)
        
        # === FIRMA ===
        group_firma = QGroupBox("✍️ Datos de Firma")
        group_firma.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        form_firma = QFormLayout()
        form_firma.setSpacing(10)
        
        self.nombre_firmante = QLineEdit("DANIEL GARCIA ARAQUE")
        self.nombre_firmante.setMinimumHeight(35)
        
        self.cargo_firmante = QLineEdit("DESARROLLADOR")
        self.cargo_firmante.setMinimumHeight(35)
        
        self.iniciales = QLineEdit("DGA")
        self.iniciales.setMinimumHeight(35)
        self.iniciales.setPlaceholderText("Ej: DAVP")
        
        form_firma.addRow("Nombre del Firmante:", self.nombre_firmante)
        form_firma.addRow("Cargo:", self.cargo_firmante)
        form_firma.addRow("Iniciales:", self.iniciales)
        group_firma.setLayout(form_firma)
        layout.addWidget(group_firma)
        
        # === CARPETA DE SALIDA ===
        group_salida = QGroupBox("📁 Carpeta de Salida")
        group_salida.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        layout_salida = QVBoxLayout()
        layout_salida.setSpacing(10)
        
        # Etiqueta que muestra la carpeta actual
        self.label_carpeta = QLabel(f"📂 {self.output_folder.absolute()}")
        self.label_carpeta.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                padding: 10px;
                border-radius: 6px;
                color: #66bb6a;
                font-family: 'Consolas', monospace;
            }
        """)
        self.label_carpeta.setWordWrap(True)
        layout_salida.addWidget(self.label_carpeta)
        
        # Botones
        btn_layout_salida = QHBoxLayout()
        
        btn_cambiar_carpeta = QPushButton("📁 Cambiar Carpeta")
        btn_cambiar_carpeta.setMinimumHeight(40)
        btn_cambiar_carpeta.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #42a5f5, stop:1 #1e88e5);
                color: white;
                font-size: 13px;
                font-weight: 600;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #64b5f6, stop:1 #2196f3);
            }
        """)
        btn_cambiar_carpeta.clicked.connect(self.seleccionar_carpeta_salida)
        
        btn_abrir_carpeta = QPushButton("🗂️ Abrir Carpeta")
        btn_abrir_carpeta.setMinimumHeight(40)
        btn_abrir_carpeta.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #66bb6a, stop:1 #43a047);
                color: white;
                font-size: 13px;
                font-weight: 600;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #81c784, stop:1 #4caf50);
            }
        """)
        btn_abrir_carpeta.clicked.connect(self.abrir_carpeta_salida)
        
        btn_layout_salida.addWidget(btn_cambiar_carpeta)
        btn_layout_salida.addWidget(btn_abrir_carpeta)
        layout_salida.addLayout(btn_layout_salida)
        
        group_salida.setLayout(layout_salida)
        layout.addWidget(group_salida)
        
        layout.addStretch()
        
        self.sub_tabs.addTab(scroll, "3️⃣ Aseguradora y Firma")
        
        layout.addStretch()
        
        self.sub_tabs.addTab(scroll, "3️⃣ Aseguradora y Firma")
    
    def crear_tab_aseguradoras(self):
        """Crea la pestaña para gestionar aseguradoras."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título
        titulo = QLabel("🏢 Gestión de Aseguradoras")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        titulo.setFont(font)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            color: #ffffff;
            background-color: #1e88e5;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
        """)
        layout.addWidget(titulo)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_agregar = QPushButton("➕ Agregar")
        btn_agregar.setMinimumHeight(40)
        btn_agregar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #66bb6a, stop:1 #43a047);
                color: white;
                font-size: 13px;
                font-weight: 600;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #81c784, stop:1 #4caf50);
            }
        """)
        btn_agregar.clicked.connect(self.agregar_aseguradora)
        
        btn_editar = QPushButton("✏️ Editar")
        btn_editar.setMinimumHeight(40)
        btn_editar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #42a5f5, stop:1 #1e88e5);
                color: white;
                font-size: 13px;
                font-weight: 600;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #64b5f6, stop:1 #2196f3);
            }
        """)
        btn_editar.clicked.connect(self.editar_aseguradora)
        
        btn_eliminar = QPushButton("🗑️ Eliminar")
        btn_eliminar.setMinimumHeight(40)
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ef5350, stop:1 #e53935);
                color: white;
                font-size: 13px;
                font-weight: 600;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f44336, stop:1 #d32f2f);
            }
        """)
        btn_eliminar.clicked.connect(self.eliminar_aseguradora)
        
        btn_refrescar = QPushButton("🔄 Refrescar")
        btn_refrescar.setMinimumHeight(40)
        btn_refrescar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #78909c, stop:1 #546e7a);
                color: white;
                font-size: 13px;
                font-weight: 600;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #90a4ae, stop:1 #607d8b);
            }
        """)
        btn_refrescar.clicked.connect(self.cargar_aseguradoras)
        
        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_editar)
        btn_layout.addWidget(btn_eliminar)
        btn_layout.addWidget(btn_refrescar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Tabla
        self.tabla_aseguradoras = QTableWidget()
        self.tabla_aseguradoras.setColumnCount(4)
        self.tabla_aseguradoras.setHorizontalHeaderLabels(["Nombre", "NIT", "Link de Pago", "Veces Usado"])
        self.tabla_aseguradoras.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tabla_aseguradoras.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_aseguradoras.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabla_aseguradoras.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_aseguradoras.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_aseguradoras.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_aseguradoras.setAlternatingRowColors(True)
        self.tabla_aseguradoras.setMinimumHeight(400)
        layout.addWidget(self.tabla_aseguradoras)
        
        self.tabs.addTab(tab, "🏢 Aseguradoras")
    
    def cargar_aseguradoras(self):
        """Carga las aseguradoras en el combo y en la tabla."""
        # Cargar en combo
        self.aseguradora_combo.clear()
        self.aseguradora_combo.addItem("-- Seleccione o escriba nueva --", None)
        
        payees = payee_manager.get_all_payees()
        for payee in payees:
            self.aseguradora_combo.addItem(payee['name'], payee)
        
        # Cargar en tabla
        self.tabla_aseguradoras.setRowCount(len(payees))
        for i, payee in enumerate(payees):
            self.tabla_aseguradoras.setItem(i, 0, QTableWidgetItem(payee['name']))
            self.tabla_aseguradoras.setItem(i, 1, QTableWidgetItem(payee['nit']))
            self.tabla_aseguradoras.setItem(i, 2, QTableWidgetItem(payee.get('link_pago', '')))
            self.tabla_aseguradoras.setItem(i, 3, QTableWidgetItem(str(payee.get('usage_count', 0))))
    
    def on_aseguradora_changed(self):
        """Se ejecuta cuando cambia la aseguradora seleccionada."""
        data = self.aseguradora_combo.currentData()
        if data:
            self.nit_aseguradora.setText(data['nit'])
        else:
            self.nit_aseguradora.clear()
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            "¿Desea limpiar todos los campos?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            self.ciudad_emision.setText("MEDELLIN")
            self.fecha_emision.setDate(QDate.currentDate())
            self.numero_carta.clear()
            self.mes_cobro.setCurrentText(QDate.currentDate().toString("MMMM").capitalize())
            self.fecha_limite_pago.setDate(QDate.currentDate().addDays(30))
            
            self.nombre_asegurado.clear()
            self.nit_asegurado.clear()
            self.direccion_asegurado.clear()
            self.telefono_asegurado.clear()
            self.ciudad_asegurado.clear()
            
            # Limpiar lista de pólizas
            self.polizas_list.clear()
            self.actualizar_tabla_polizas()
            self.calcular_total_general()
            
            self.aseguradora_combo.setCurrentIndex(0)
    
    def llenar_ejemplo(self):
        """Llena el formulario con datos de ejemplo para prueba rápida."""
        # Datos de emisión
        self.ciudad_emision.setText("MEDELLIN")
        self.fecha_emision.setDate(QDate.currentDate())
        self.numero_carta.setText("15434 - 2025")
        self.mes_cobro.setCurrentText("Enero")
        self.fecha_limite_pago.setDate(QDate.currentDate().addDays(30))
        
        # Datos del asegurado
        self.nombre_asegurado.setText("JUAN CARLOS RODRIGUEZ MARTINEZ")
        self.nit_asegurado.setText("900123456-6")
        self.direccion_asegurado.setText("Carrera 45 # 76-32, Oficina 501")
        self.telefono_asegurado.setText("3001234567")
        self.ciudad_asegurado.setText("MEDELLIN")
        
        # Limpiar y agregar pólizas de ejemplo
        self.polizas_list.clear()
        
        # Póliza 1
        poliza1 = {
            'numero': 'VG-2026-0001',
            'tipo': 'VIDA GRUPO',
            'plan': 'Plan Empresarial Plus',
            'fecha_inicio': QDate.currentDate(),
            'fecha_fin': QDate.currentDate().addYears(1),
            'prima': '1500000',
            'iva': '285000',
            'otros': '50000',
            'check_prima': True,
            'check_iva': True,
            'check_otros': True,
            'check_plan': True
        }
        self.polizas_list.append(poliza1)
        
        # Póliza 2
        poliza2 = {
            'numero': 'AP-2026-0002',
            'tipo': 'ACCIDENTES PERSONALES',
            'plan': 'Cobertura Total',
            'fecha_inicio': QDate.currentDate(),
            'fecha_fin': QDate.currentDate().addYears(1),
            'prima': '800000',
            'iva': '152000',
            'otros': '0',
            'check_prima': True,
            'check_iva': True,
            'check_otros': False,
            'check_plan': True
        }
        self.polizas_list.append(poliza2)
        
        self.actualizar_tabla_polizas()
        self.calcular_total_general()
        
        # Aseguradora - intentar seleccionar la primera si existe
        if self.aseguradora_combo.count() > 1:
            self.aseguradora_combo.setCurrentIndex(1)
        else:
            self.aseguradora_combo.setEditText("SEGUROS DE VIDA SURAMERICANA S.A.")
            self.nit_aseguradora.setText("890903790-5")
        
        # Cambiar a la primera pestaña para que vea los datos
        self.sub_tabs.setCurrentIndex(0)
        
        QMessageBox.information(
            self,
            "✅ Ejemplo Cargado",
            "Se han llenado todos los campos con datos de ejemplo (2 pólizas).\n\n"
            "Revise la información y presione 'Generar PDF' cuando esté listo."
        )
    
    def seleccionar_carpeta_salida(self):
        """Permite al usuario seleccionar la carpeta donde se guardarán los PDFs."""
        from PyQt6.QtWidgets import QFileDialog
        
        carpeta = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar Carpeta de Salida",
            str(self.output_folder.absolute()),
            QFileDialog.Option.ShowDirsOnly
        )
        
        if carpeta:
            self.output_folder = Path(carpeta)
            self.label_carpeta.setText(f"📂 {self.output_folder.absolute()}")
            logger.info(f"Carpeta de salida cambiada a: {self.output_folder}")
            QMessageBox.information(
                self,
                "✅ Carpeta Configurada",
                f"Los PDFs se guardarán en:\n\n{self.output_folder.absolute()}"
            )
    
    def abrir_carpeta_salida(self):
        """Abre la carpeta de salida en el explorador de archivos."""
        import os
        import platform
        
        # Crear carpeta si no existe
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # Abrir en explorador según el sistema operativo
        if platform.system() == "Windows":
            os.startfile(self.output_folder)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{self.output_folder}"')
        else:  # Linux
            os.system(f'xdg-open "{self.output_folder}"')
        
        logger.info(f"Carpeta abierta: {self.output_folder}")
    
    def validar_formulario(self):
        """Valida que los campos requeridos estén llenos."""
        errores = []
        
        if not self.numero_carta.text().strip():
            errores.append("- Número de carta")
        if not self.nombre_asegurado.text().strip():
            errores.append("- Nombre del asegurado")
        if not self.nit_asegurado.text().strip():
            errores.append("- NIT del asegurado")
        if len(self.polizas_list) == 0:
            errores.append("- Debe agregar al menos una póliza")
        if not self.aseguradora_combo.currentText().strip() or \
           self.aseguradora_combo.currentText() == "-- Seleccione o escriba nueva --":
            errores.append("- Aseguradora")
        if not self.nit_aseguradora.text().strip():
            errores.append("- NIT de aseguradora")
        
        if errores:
            QMessageBox.warning(
                self,
                "Campos Requeridos",
                "Por favor complete los siguientes campos:\n\n" + "\n".join(errores)
            )
            return False
        return True
    
    def generar_pdf(self):
        """Genera el PDF de la carta de cobro."""
        if not self.validar_formulario():
            return
        
        try:
            # Crear objetos del modelo
            asegurado = Asegurado(
                razon_social=self.nombre_asegurado.text().strip(),
                nit=self.nit_asegurado.text().strip(),
                direccion=self.direccion_asegurado.text().strip() or "N/A",
                telefono=self.telefono_asegurado.text().strip() or "N/A",
                ciudad=self.ciudad_asegurado.text().strip() or "N/A"
            )
            
            # Usar la primera póliza para el modelo Documento (solo para el asunto)
            primera_poliza = self.polizas_list[0]
            poliza = Poliza(
                numero=primera_poliza['numero'],
                tipo=primera_poliza['tipo'],
                plan_poliza=primera_poliza['plan'],
                vigencia_inicio=primera_poliza['fecha_inicio'].toPyDate(),
                vigencia_fin=primera_poliza['fecha_fin'].toPyDate()
            )
            
            # Calcular montos totales sumando todas las pólizas
            total_prima = 0
            total_iva = 0
            total_otros = 0
            
            for pol in self.polizas_list:
                if pol.get('check_prima', False):
                    try:
                        total_prima += float(pol.get('prima', '0').replace(',', ''))
                    except ValueError:
                        pass
                if pol.get('check_iva', False):
                    try:
                        total_iva += float(pol.get('iva', '0').replace(',', ''))
                    except ValueError:
                        pass
                if pol.get('check_otros', False):
                    try:
                        total_otros += float(pol.get('otros', '0').replace(',', ''))
                    except ValueError:
                        pass
            
            montos = MontosCobro(
                prima=total_prima,
                impuesto=total_iva,
                otros_rubros=total_otros
            )
            
            # Información de campos activos para el PDF (al menos uno debe estar activo en alguna póliza)
            campos_activos = {
                'prima': any(pol.get('check_prima', False) for pol in self.polizas_list),
                'impuesto': any(pol.get('check_iva', False) for pol in self.polizas_list),
                'otros_rubros': any(pol.get('check_otros', False) for pol in self.polizas_list)
            }
            
            # Obtener o guardar aseguradora
            nombre_aseguradora = self.aseguradora_combo.currentText().strip()
            nit_aseguradora = self.nit_aseguradora.text().strip()
            
            # Obtener link de pago de la aseguradora seleccionada
            link_pago = ""
            payee_data = self.aseguradora_combo.currentData()
            if payee_data:
                link_pago = payee_data.get('link_pago', '')
            
            # Si es una nueva aseguradora, agregarla
            if self.aseguradora_combo.currentData() is None and nombre_aseguradora:
                try:
                    payee_manager.add_payee(nombre_aseguradora, nit_aseguradora, link_pago)
                    logger.info(f"Nueva aseguradora agregada: {nombre_aseguradora}")
                except ValueError:
                    pass  # Ya existe, continuar
            
            # Incrementar uso
            if nombre_aseguradora:
                payee_manager.increment_usage(nombre_aseguradora)
            
            documento = Documento(
                ciudad_emision=self.ciudad_emision.text().strip(),
                fecha_emision=self.fecha_emision.date().toPyDate(),
                numero_carta=self.numero_carta.text().strip(),
                mes_cobro=self.mes_cobro.currentText(),
                fecha_limite_pago=self.fecha_limite_pago.date().toPyDate(),
                asegurado=asegurado,
                poliza=poliza,
                montos=montos,
                payee_company_name=nombre_aseguradora,
                payee_company_nit=nit_aseguradora,
                firmante_nombre=self.nombre_firmante.text().strip(),
                firmante_cargo=self.cargo_firmante.text().strip(),
                firmante_iniciales=self.iniciales.text().strip()
            )
            
            # Generar nombre de archivo
            nombre_archivo = f"carta_cobro_{documento.numero_carta.replace(' - ', '-')}_{documento.asegurado.nit.replace('-', '')}.pdf"
            
            # Crear carpeta si no existe
            self.output_folder.mkdir(parents=True, exist_ok=True)
            
            # Generar PDF - El backend necesita dict, filename y campos activos
            generator = CartaCobroGenerator()
            pdf_data = documento.to_pdf_data()
            pdf_data['campos_activos'] = campos_activos
            pdf_data['payee_link_pago'] = link_pago  # Agregar link de pago
            
            # Agregar lista completa de pólizas con montos (sin fechas de vigencia)
            pdf_data['polizas'] = []
            for pol in self.polizas_list:
                poliza_data = {
                    'numero': pol['numero'],
                    'tipo': pol['tipo'],
                    'plan': pol['plan'],
                    'prima': float(pol.get('prima', '0').replace(',', '')) if pol.get('check_prima', False) else 0,
                    'iva': float(pol.get('iva', '0').replace(',', '')) if pol.get('check_iva', False) else 0,
                    'otros': float(pol.get('otros', '0').replace(',', '')) if pol.get('check_otros', False) else 0,
                    'check_prima': pol.get('check_prima', False),
                    'check_iva': pol.get('check_iva', False),
                    'check_otros': pol.get('check_otros', False),
                    'check_plan': pol.get('check_plan', True)
                }
                pdf_data['polizas'].append(poliza_data)
            
            output_file = generator.generate(
                data=pdf_data,
                output_filename=nombre_archivo
            )
            
            # Mover archivo a carpeta seleccionada si no está ahí
            if output_file.parent != self.output_folder:
                import shutil
                destino = self.output_folder / output_file.name
                shutil.move(str(output_file), str(destino))
                output_file = destino
            
            respuesta = QMessageBox.question(
                self,
                "✅ Éxito",
                f"Carta generada correctamente:\n\n{output_file.name}\n\nGuardada en:\n{output_file.parent}\n\n¿Desea crear otra carta?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if respuesta == QMessageBox.StandardButton.No:
                # Abrir el PDF
                import os
                import platform
                if platform.system() == "Windows":
                    os.startfile(output_file)
                elif platform.system() == "Darwin":  # macOS
                    os.system(f'open "{output_file}"')
                else:  # Linux
                    os.system(f'xdg-open "{output_file}"')
            
            # Recargar aseguradoras
            self.cargar_aseguradoras()
            
            logger.info(f"PDF generado: {output_file}")
            
        except Exception as e:
            logger.error(f"Error al generar PDF: {e}", exc_info=True)
            QMessageBox.critical(
                self,
                "❌ Error",
                f"Error al generar el PDF:\n\n{str(e)}"
            )
    
    def agregar_aseguradora(self):
        """Abre diálogo para agregar aseguradora."""
        dialog = AseguradoraDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data['nombre'] and data['nit']:
                try:
                    payee_manager.add_payee(data['nombre'], data['nit'], data.get('link_pago', ''))
                    self.cargar_aseguradoras()
                    QMessageBox.information(self, "✅ Éxito", "Aseguradora agregada correctamente")
                except ValueError as e:
                    QMessageBox.warning(self, "⚠️ Advertencia", str(e))
            else:
                QMessageBox.warning(self, "⚠️ Advertencia", "Complete todos los campos")
    
    def editar_aseguradora(self):
        """Edita la aseguradora seleccionada."""
        row = self.tabla_aseguradoras.currentRow()
        if row < 0:
            QMessageBox.warning(self, "⚠️ Advertencia", "Seleccione una aseguradora")
            return
        
        nombre_actual = self.tabla_aseguradoras.item(row, 0).text()
        nit_actual = self.tabla_aseguradoras.item(row, 1).text()
        link_pago_actual = self.tabla_aseguradoras.item(row, 2).text()
        
        dialog = AseguradoraDialog(self, nombre_actual, nit_actual, link_pago_actual)
        if dialog.exec():
            data = dialog.get_data()
            if data['nombre'] and data['nit']:
                try:
                    payee_manager.update_payee(nombre_actual, data['nombre'], data['nit'], data.get('link_pago', ''))
                    self.cargar_aseguradoras()
                    QMessageBox.information(self, "✅ Éxito", "Aseguradora actualizada correctamente")
                except ValueError as e:
                    QMessageBox.warning(self, "⚠️ Advertencia", str(e))
    
    def agregar_poliza(self):
        """Abre diálogo para agregar una póliza a la lista."""
        dialog = PolizaDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data['numero']:
                # Agregar a la lista interna
                self.polizas_list.append(data)
                
                # Actualizar tabla y total
                self.actualizar_tabla_polizas()
                self.calcular_total_general()
                QMessageBox.information(self, "✅ Éxito", "Póliza agregada correctamente")
            else:
                QMessageBox.warning(self, "⚠️ Advertencia", "El número de póliza es obligatorio")
    
    def eliminar_poliza(self):
        """Elimina la póliza seleccionada de la lista."""
        row = self.tabla_polizas.currentRow()
        if row < 0:
            QMessageBox.warning(self, "⚠️ Advertencia", "Seleccione una póliza para eliminar")
            return
        
        numero_poliza = self.tabla_polizas.item(row, 0).text()
        
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar la póliza:\n\n{numero_poliza}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            # Eliminar de la lista interna
            del self.polizas_list[row]
            
            # Actualizar tabla y total
            self.actualizar_tabla_polizas()
            self.calcular_total_general()
            QMessageBox.information(self, "✅ Éxito", "Póliza eliminada correctamente")
    
    def actualizar_tabla_polizas(self):
        """Actualiza la tabla de pólizas con los datos de la lista (sin fechas de vigencia)."""
        self.tabla_polizas.setRowCount(len(self.polizas_list))
        for i, poliza in enumerate(self.polizas_list):
            # Datos básicos (sin fechas)
            self.tabla_polizas.setItem(i, 0, QTableWidgetItem(poliza['numero']))
            self.tabla_polizas.setItem(i, 1, QTableWidgetItem(poliza['tipo']))
            
            # Descripción (mostrar solo si checkbox está activo)
            plan_text = poliza['plan'] if poliza.get('check_plan', True) else "-"
            self.tabla_polizas.setItem(i, 2, QTableWidgetItem(plan_text))
            
            # Montos
            prima_val = float(poliza.get('prima', '0').replace(',', '')) if poliza.get('check_prima', False) else 0
            iva_val = float(poliza.get('iva', '0').replace(',', '')) if poliza.get('check_iva', False) else 0
            otros_val = float(poliza.get('otros', '0').replace(',', '')) if poliza.get('check_otros', False) else 0
            total_poliza = prima_val + iva_val + otros_val
            
            prima_text = f"${prima_val:,.2f}" if poliza.get('check_prima', False) else "-"
            iva_text = f"${iva_val:,.2f}" if poliza.get('check_iva', False) else "-"
            otros_text = f"${otros_val:,.2f}" if poliza.get('check_otros', False) else "-"
            
            self.tabla_polizas.setItem(i, 3, QTableWidgetItem(prima_text))
            self.tabla_polizas.setItem(i, 4, QTableWidgetItem(iva_text))
            self.tabla_polizas.setItem(i, 5, QTableWidgetItem(otros_text))
            self.tabla_polizas.setItem(i, 6, QTableWidgetItem(f"${total_poliza:,.2f}"))
    
    def calcular_total_general(self):
        """Calcula el total general sumando todas las pólizas."""
        total = 0
        for poliza in self.polizas_list:
            try:
                prima_val = float(poliza.get('prima', '0').replace(',', '')) if poliza.get('check_prima', False) else 0
                iva_val = float(poliza.get('iva', '0').replace(',', '')) if poliza.get('check_iva', False) else 0
                otros_val = float(poliza.get('otros', '0').replace(',', '')) if poliza.get('check_otros', False) else 0
                total += prima_val + iva_val + otros_val
            except (ValueError, AttributeError):
                pass
        
        self.total_general.setText(f"${total:,.2f}")
    
    def eliminar_aseguradora(self):
        """Elimina la aseguradora seleccionada."""
        row = self.tabla_aseguradoras.currentRow()
        if row < 0:
            QMessageBox.warning(self, "⚠️ Advertencia", "Seleccione una aseguradora")
            return
        
        nombre = self.tabla_aseguradoras.item(row, 0).text()
        
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar la aseguradora:\n\n{nombre}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                payee_manager.delete_payee(nombre)
                self.cargar_aseguradoras()
                QMessageBox.information(self, "✅ Éxito", "Aseguradora eliminada correctamente")
            except ValueError as e:
                QMessageBox.warning(self, "⚠️ Advertencia", str(e))


def main():
    """Función principal."""
    app = QApplication(sys.argv)
    
    # Estilo básico
    app.setStyle("Fusion")
    
    ventana = GeneradorCartasGUI()
    ventana.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
