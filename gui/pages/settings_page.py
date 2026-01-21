"""
Settings page.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox, QFormLayout,
    QLineEdit, QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt

from gui.theme import Spacing
from gui.widgets.toast import show_toast
from utils.config import config
from utils.logger import get_logger

logger = get_logger(__name__)


class SettingsPage(QWidget):
    """
    Settings and configuration page.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
    
    def _build_ui(self):
        """Build UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        layout.setSpacing(Spacing.LG)
        
        # Header
        title = QLabel("Configuración")
        title.setProperty("styleClass", "title")
        layout.addWidget(title)
        
        # Company info
        company_group = QGroupBox("Información de la Empresa")
        company_layout = QFormLayout()
        company_layout.setSpacing(Spacing.MD)
        
        name_input = QLineEdit("SEGUROS UNIÓN")
        name_input.setReadOnly(True)
        company_layout.addRow("Nombre:", name_input)
        
        email_input = QLineEdit("gerencia@segurosunion.com")
        email_input.setReadOnly(True)
        company_layout.addRow("Email:", email_input)
        
        address_input = QLineEdit("Carrera 77 A # 49 - 37 .Sector Estadio - Medellín")
        address_input.setReadOnly(True)
        company_layout.addRow("Dirección:", address_input)
        
        company_group.setLayout(company_layout)
        layout.addWidget(company_group)
        
        # Paths
        paths_group = QGroupBox("Rutas")
        paths_layout = QFormLayout()
        paths_layout.setSpacing(Spacing.MD)
        
        self.output_path = QLineEdit(str(config.OUTPUT_DIR))
        self.output_path.setReadOnly(True)
        
        output_layout = QVBoxLayout()
        output_layout.setSpacing(Spacing.SM)
        output_layout.addWidget(self.output_path)
        
        open_btn = QPushButton("Abrir Carpeta")
        open_btn.clicked.connect(self._open_output_folder)
        output_layout.addWidget(open_btn)
        
        paths_layout.addRow("Carpeta de salida:", output_layout)
        
        paths_group.setLayout(paths_layout)
        layout.addWidget(paths_group)
        
        # Application info
        app_group = QGroupBox("Información de la Aplicación")
        app_layout = QFormLayout()
        app_layout.setSpacing(Spacing.MD)
        
        version_input = QLineEdit(config.APP_VERSION)
        version_input.setReadOnly(True)
        app_layout.addRow("Versión:", version_input)
        
        app_group.setLayout(app_layout)
        layout.addWidget(app_group)
        
        layout.addStretch()
    
    def _open_output_folder(self):
        """Open output folder."""
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl
        
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(config.OUTPUT_DIR)))
        show_toast(self, "Carpeta abierta", "info")
