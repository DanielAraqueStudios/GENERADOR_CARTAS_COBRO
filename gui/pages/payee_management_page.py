"""
Payee (insurance company) management page.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QDialog,
    QFormLayout, QDialogButtonBox, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt

from gui.theme import Spacing
from gui.widgets.toast import show_toast
from gui.widgets.validated_input import NITInput
from utils.payee_manager import payee_manager
from utils.logger import get_logger

logger = get_logger(__name__)


class PayeeDialog(QDialog):
    """Dialog for adding/editing payees."""
    
    def __init__(self, payee=None, parent=None):
        super().__init__(parent)
        self.payee = payee
        self.setWindowTitle("Editar Aseguradora" if payee else "Nueva Aseguradora")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Form
        form = QFormLayout()
        form.setSpacing(Spacing.MD)
        
        self.name_input = QLineEdit()
        if payee:
            self.name_input.setText(payee['name'])
        form.addRow("Nombre:", self.name_input)
        
        self.nit_input = NITInput()
        if payee:
            self.nit_input.setText(payee['nit'])
        form.addRow("NIT:", self.nit_input)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_data(self):
        """Get form data."""
        return {
            'name': self.name_input.text().strip().upper(),
            'nit': self.nit_input.text().strip()
        }


class PayeeManagementPage(QWidget):
    """
    Page for managing insurance companies (payees).
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._load_data()
    
    def _build_ui(self):
        """Build UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        layout.setSpacing(Spacing.LG)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Gestión de Aseguradoras")
        title.setProperty("styleClass", "title")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        add_btn = QPushButton("+ Nueva Aseguradora")
        add_btn.setProperty("styleClass", "primary")
        add_btn.clicked.connect(self._add_payee)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre", "NIT", "Veces Usada", "Acciones"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
    
    def _load_data(self):
        """Load payees into table."""
        payees = payee_manager.get_all_payees()
        self.table.setRowCount(len(payees))
        
        for row, payee in enumerate(payees):
            # Name
            self.table.setItem(row, 0, QTableWidgetItem(payee['name']))
            
            # NIT
            self.table.setItem(row, 1, QTableWidgetItem(payee['nit']))
            
            # Usage count
            count_item = QTableWidgetItem(str(payee['usage_count']))
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, count_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(Spacing.SM, 0, Spacing.SM, 0)
            actions_layout.setSpacing(Spacing.SM)
            
            edit_btn = QPushButton("Editar")
            edit_btn.clicked.connect(lambda checked, p=payee: self._edit_payee(p))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("Eliminar")
            delete_btn.setProperty("styleClass", "danger")
            delete_btn.clicked.connect(lambda checked, p=payee: self._delete_payee(p))
            actions_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 3, actions_widget)
    
    def _add_payee(self):
        """Add new payee."""
        dialog = PayeeDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            if not data['name'] or not data['nit']:
                show_toast(self, "Nombre y NIT son requeridos", "error")
                return
            
            payee_manager.add_payee(data['name'], data['nit'])
            self._load_data()
            show_toast(self, f"Aseguradora '{data['name']}' agregada", "success")
    
    def _edit_payee(self, payee):
        """Edit existing payee."""
        dialog = PayeeDialog(payee, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            if not data['name'] or not data['nit']:
                show_toast(self, "Nombre y NIT son requeridos", "error")
                return
            
            payee_manager.update_payee(payee['name'], data['name'], data['nit'])
            self._load_data()
            show_toast(self, f"Aseguradora actualizada", "success")
    
    def _delete_payee(self, payee):
        """Delete payee."""
        from PyQt6.QtWidgets import QMessageBox
        
        response = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar '{payee['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if response == QMessageBox.StandardButton.Yes:
            payee_manager.delete_payee(payee['name'])
            self._load_data()
            show_toast(self, f"Aseguradora eliminada", "success")
