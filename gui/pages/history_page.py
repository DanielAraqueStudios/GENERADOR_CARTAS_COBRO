"""
Document history page.
"""
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

from gui.theme import Spacing
from gui.widgets.toast import show_toast
from utils.versioning import version_manager
from utils.config import config
from utils.logger import get_logger

logger = get_logger(__name__)


class HistoryPage(QWidget):
    """
    Page showing history of generated documents.
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
        header_layout = QHBoxLayout()
        
        title = QLabel("Historial de Documentos")
        title.setProperty("styleClass", "title")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.clicked.connect(self._load_statistics)
        header_layout.addWidget(refresh_btn)
        
        open_folder_btn = QPushButton("📁 Abrir Carpeta")
        open_folder_btn.clicked.connect(self._open_output_folder)
        header_layout.addWidget(open_folder_btn)
        
        layout.addLayout(header_layout)
        
        # Statistics
        self.stats_label = QLabel()
        self.stats_label.setProperty("styleClass", "section-header")
        layout.addWidget(self.stats_label)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Año", "Documentos Generados"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        # Load data
        self._load_statistics()
    
    def _load_statistics(self):
        """Load statistics."""
        stats = version_manager.get_statistics()
        
        if not stats:
            self.stats_label.setText("No hay documentos generados")
            self.table.setRowCount(0)
            return
        
        # Calculate totals
        total_docs = sum(data['total_documents'] for data in stats.values())
        self.stats_label.setText(f"Total de documentos generados: {total_docs}")
        
        # Populate table
        self.table.setRowCount(len(stats))
        
        for row, (year, data) in enumerate(sorted(stats.items(), reverse=True)):
            year_item = QTableWidgetItem(str(data['year']))
            year_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, year_item)
            
            count_item = QTableWidgetItem(str(data['total_documents']))
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, count_item)
    
    def _open_output_folder(self):
        """Open output folder in file explorer."""
        output_dir = config.OUTPUT_DIR / 'cartas'
        
        if not output_dir.exists():
            show_toast(self, "Carpeta de salida no existe aún", "warning")
            return
        
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(output_dir)))
        show_toast(self, "Carpeta abierta en el explorador", "info")
