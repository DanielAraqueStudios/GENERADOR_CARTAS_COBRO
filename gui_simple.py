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
    QFormLayout, QHeaderView, QDialog, QDialogButtonBox, QScrollArea
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
    
    def __init__(self, parent=None, nombre="", nit=""):
        super().__init__(parent)
        self.setWindowTitle("Aseguradora")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QFormLayout(self)
        
        # Campos
        self.nombre_input = QLineEdit(nombre)
        self.nit_input = QLineEdit(nit)
        
        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("NIT:", self.nit_input)
        
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
            'nit': self.nit_input.text().strip()
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
        
        # === DATOS DE LA PÓLIZA ===
        group_poliza = QGroupBox("📋 Datos de la Póliza")
        group_poliza.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        form_poliza = QFormLayout()
        form_poliza.setSpacing(10)
        
        self.numero_poliza = QLineEdit()
        self.numero_poliza.setMinimumHeight(35)
        self.numero_poliza.setPlaceholderText("Número de póliza")
        
        self.tipo_poliza = QComboBox()
        self.tipo_poliza.setMinimumHeight(35)
        self.tipo_poliza.addItems([
            "VIDA GRUPO",
            "SOAT",
            "ACCIDENTES PERSONALES",
            "SALUD",
            "VIDA INDIVIDUAL",
            "OTRO"
        ])
        
        self.plan_poliza = QLineEdit()
        self.plan_poliza.setMinimumHeight(35)
        self.plan_poliza.setPlaceholderText("Plan o descripción")
        
        self.fecha_inicio_vigencia = QDateEdit()
        self.fecha_inicio_vigencia.setCalendarPopup(True)
        self.fecha_inicio_vigencia.setDate(QDate.currentDate())
        self.fecha_inicio_vigencia.setMinimumHeight(35)
        
        self.fecha_fin_vigencia = QDateEdit()
        self.fecha_fin_vigencia.setCalendarPopup(True)
        self.fecha_fin_vigencia.setDate(QDate.currentDate().addYears(1))
        self.fecha_fin_vigencia.setMinimumHeight(35)
        
        form_poliza.addRow("Número de Póliza:", self.numero_poliza)
        form_poliza.addRow("Tipo de Seguro:", self.tipo_poliza)
        form_poliza.addRow("Plan/Descripción:", self.plan_poliza)
        form_poliza.addRow("Inicio de Vigencia:", self.fecha_inicio_vigencia)
        form_poliza.addRow("Fin de Vigencia:", self.fecha_fin_vigencia)
        group_poliza.setLayout(form_poliza)
        layout.addWidget(group_poliza)
        
        # === MONTOS ===
        group_montos = QGroupBox("💰 Montos a Cobrar")
        group_montos.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        form_montos = QFormLayout()
        form_montos.setSpacing(10)
        
        self.prima = QLineEdit("0")
        self.prima.setMinimumHeight(35)
        self.prima.setPlaceholderText("0.00")
        
        self.iva = QLineEdit("0")
        self.iva.setMinimumHeight(35)
        self.iva.setPlaceholderText("0.00")
        
        self.otros = QLineEdit("0")
        self.otros.setMinimumHeight(35)
        self.otros.setPlaceholderText("0.00")
        
        self.total = QLineEdit("0")
        self.total.setMinimumHeight(40)
        self.total.setReadOnly(True)
        self.total.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2e7d32, stop:1 #1b5e20);
                font-weight: bold; 
                font-size: 18px;
                color: #a5d6a7;
                border: 3px solid #66bb6a;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        # Conectar para cálculo automático
        self.prima.textChanged.connect(self.calcular_total)
        self.iva.textChanged.connect(self.calcular_total)
        self.otros.textChanged.connect(self.calcular_total)
        
        form_montos.addRow("Prima ($):", self.prima)
        form_montos.addRow("IVA ($):", self.iva)
        form_montos.addRow("Otros Conceptos ($):", self.otros)
        form_montos.addRow("TOTAL A PAGAR ($):", self.total)
        group_montos.setLayout(form_montos)
        layout.addWidget(group_montos)
        
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
        
        # === FIRMA ===
        group_firma = QGroupBox("✍️ Datos de Firma")
        group_firma.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        form_firma = QFormLayout()
        form_firma.setSpacing(10)
        
        self.nombre_firmante = QLineEdit("DANIEL ANTONIO VELEZ PELAEZ")
        self.nombre_firmante.setMinimumHeight(35)
        
        self.cargo_firmante = QLineEdit("GERENTE")
        self.cargo_firmante.setMinimumHeight(35)
        
        self.iniciales = QLineEdit("DAVP")
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
        self.tabla_aseguradoras.setColumnCount(3)
        self.tabla_aseguradoras.setHorizontalHeaderLabels(["Nombre", "NIT", "Veces Usado"])
        self.tabla_aseguradoras.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tabla_aseguradoras.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_aseguradoras.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
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
            self.tabla_aseguradoras.setItem(i, 2, QTableWidgetItem(str(payee.get('usage_count', 0))))
    
    def on_aseguradora_changed(self):
        """Se ejecuta cuando cambia la aseguradora seleccionada."""
        data = self.aseguradora_combo.currentData()
        if data:
            self.nit_aseguradora.setText(data['nit'])
        else:
            self.nit_aseguradora.clear()
    
    def calcular_total(self):
        """Calcula el total automáticamente."""
        try:
            prima = float(self.prima.text() or 0)
            iva = float(self.iva.text() or 0)
            otros = float(self.otros.text() or 0)
            total = prima + iva + otros
            self.total.setText(f"{total:.2f}")
        except ValueError:
            self.total.setText("0")
    
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
            
            self.numero_poliza.clear()
            self.tipo_poliza.setCurrentIndex(0)
            self.plan_poliza.clear()
            self.fecha_inicio_vigencia.setDate(QDate.currentDate())
            self.fecha_fin_vigencia.setDate(QDate.currentDate().addYears(1))
            
            self.prima.setText("0")
            self.iva.setText("0")
            self.otros.setText("0")
            
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
        
        # Datos de la póliza
        self.numero_poliza.setText("VG-2026-0001")
        self.tipo_poliza.setCurrentText("VIDA GRUPO")
        self.plan_poliza.setText("Plan Empresarial Plus")
        self.fecha_inicio_vigencia.setDate(QDate.currentDate())
        self.fecha_fin_vigencia.setDate(QDate.currentDate().addYears(1))
        
        # Montos
        self.prima.setText("1500000")
        self.iva.setText("285000")
        self.otros.setText("50000")
        
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
            "Se han llenado todos los campos con datos de ejemplo.\n\n"
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
        if not self.numero_poliza.text().strip():
            errores.append("- Número de póliza")
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
            
            poliza = Poliza(
                numero=self.numero_poliza.text().strip(),
                tipo=self.tipo_poliza.currentText(),
                plan_poliza=self.plan_poliza.text().strip() or "N/A",
                vigencia_inicio=self.fecha_inicio_vigencia.date().toPyDate(),
                vigencia_fin=self.fecha_fin_vigencia.date().toPyDate()
            )
            
            montos = MontosCobro(
                prima=float(self.prima.text() or 0),
                impuesto=float(self.iva.text() or 0),
                otros_rubros=float(self.otros.text() or 0)
            )
            
            # Obtener o guardar aseguradora
            nombre_aseguradora = self.aseguradora_combo.currentText().strip()
            nit_aseguradora = self.nit_aseguradora.text().strip()
            
            # Si es una nueva aseguradora, agregarla
            if self.aseguradora_combo.currentData() is None and nombre_aseguradora:
                try:
                    payee_manager.add_payee(nombre_aseguradora, nit_aseguradora)
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
            
            # Generar PDF - El backend necesita dict y filename
            generator = CartaCobroGenerator()
            output_file = generator.generate(
                data=documento.to_pdf_data(),
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
                    payee_manager.add_payee(data['nombre'], data['nit'])
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
        
        dialog = AseguradoraDialog(self, nombre_actual, nit_actual)
        if dialog.exec():
            data = dialog.get_data()
            if data['nombre'] and data['nit']:
                try:
                    payee_manager.update_payee(nombre_actual, data['nombre'], data['nit'])
                    self.cargar_aseguradoras()
                    QMessageBox.information(self, "✅ Éxito", "Aseguradora actualizada correctamente")
                except ValueError as e:
                    QMessageBox.warning(self, "⚠️ Advertencia", str(e))
    
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
