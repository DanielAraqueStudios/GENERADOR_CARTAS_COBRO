"""
Validated input widgets with real-time feedback.
"""
from typing import Optional, Tuple, Callable
from PyQt6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QValidator
from gui.theme import Spacing


class ValidatedLineEdit(QWidget):
    """
    Line edit with validation feedback and error message display.
    """
    
    textChanged = pyqtSignal(str)
    validationChanged = pyqtSignal(bool)  # True if valid
    
    def __init__(
        self,
        label: str = "",
        placeholder: str = "",
        validator_func: Optional[Callable[[str], Tuple[bool, Optional[str]]]] = None,
        parent=None
    ):
        """
        Initialize validated input.
        
        Args:
            label: Label text
            placeholder: Placeholder text
            validator_func: Function that takes text and returns (is_valid, error_message)
            parent: Parent widget
        """
        super().__init__(parent)
        self.validator_func = validator_func
        self._is_valid = True
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Spacing.SM)
        
        # Label
        if label:
            self.label = QLabel(label)
            self.label.setProperty("styleClass", "form-label")
            layout.addWidget(self.label)
        else:
            self.label = None
        
        # Input field
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.line_edit)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setProperty("styleClass", "error")
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        layout.addWidget(self.error_label)
    
    def _on_text_changed(self, text: str):
        """Handle text change and validate."""
        self.textChanged.emit(text)
        self.validate()
    
    def validate(self) -> bool:
        """
        Validate current text.
        
        Returns:
            bool: True if valid
        """
        if not self.validator_func:
            self._is_valid = True
            self._clear_error()
            return True
        
        text = self.line_edit.text().strip()
        if not text:  # Empty is valid (use required=True in form validation)
            self._is_valid = True
            self._clear_error()
            self.validationChanged.emit(True)
            return True
        
        is_valid, error_msg = self.validator_func(text)
        self._is_valid = is_valid
        
        if is_valid:
            self._clear_error()
        else:
            self._show_error(error_msg or "Invalid input")
        
        self.validationChanged.emit(is_valid)
        return is_valid
    
    def _show_error(self, message: str):
        """Show error message."""
        self.line_edit.setProperty("hasError", True)
        self.line_edit.style().unpolish(self.line_edit)
        self.line_edit.style().polish(self.line_edit)
        
        self.error_label.setText(message)
        self.error_label.show()
    
    def _clear_error(self):
        """Clear error state."""
        self.line_edit.setProperty("hasError", False)
        self.line_edit.style().unpolish(self.line_edit)
        self.line_edit.style().polish(self.line_edit)
        
        self.error_label.hide()
    
    def text(self) -> str:
        """Get current text."""
        return self.line_edit.text()
    
    def setText(self, text: str):
        """Set text."""
        self.line_edit.setText(text)
    
    def setPlaceholderText(self, text: str):
        """Set placeholder."""
        self.line_edit.setPlaceholderText(text)
    
    def setReadOnly(self, read_only: bool):
        """Set read-only state."""
        self.line_edit.setReadOnly(read_only)
    
    def setEnabled(self, enabled: bool):
        """Enable/disable input."""
        self.line_edit.setEnabled(enabled)
        if self.label:
            self.label.setEnabled(enabled)
    
    def is_valid(self) -> bool:
        """Check if current value is valid."""
        return self._is_valid
    
    def setFocus(self):
        """Set focus to input field."""
        self.line_edit.setFocus()


class NITInput(ValidatedLineEdit):
    """Specialized input for Colombian NIT with validation."""
    
    def __init__(self, label: str = "NIT", parent=None):
        from validators.field_validators import FieldValidator
        
        super().__init__(
            label=label,
            placeholder="123456789-0",
            validator_func=FieldValidator.validate_nit_colombiano,
            parent=parent
        )
        
        # Set input mask for NIT format
        # Allow only digits and hyphen
        self.line_edit.setInputMask("999999999-9;_")
        self.line_edit.setMaxLength(12)


class PhoneInput(ValidatedLineEdit):
    """Specialized input for Colombian phone numbers."""
    
    def __init__(self, label: str = "Teléfono", parent=None):
        from validators.field_validators import FieldValidator
        
        super().__init__(
            label=label,
            placeholder="6071234567",
            validator_func=FieldValidator.validate_telefono_colombiano,
            parent=parent
        )
        
        # Only digits - use QRegularExpressionValidator instead of QIntValidator to avoid overflow
        from PyQt6.QtGui import QRegularExpressionValidator
        from PyQt6.QtCore import QRegularExpression
        phone_regex = QRegularExpression("^[0-9]{0,10}$")
        self.line_edit.setValidator(QRegularExpressionValidator(phone_regex))
        self.line_edit.setMaxLength(10)


class CurrencyInput(QWidget):
    """
    Colombian currency input with proper formatting.
    """
    
    valueChanged = pyqtSignal(float)  # Emits normalized value
    
    def __init__(self, label: str = "Monto (COP)", parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Spacing.SM)
        
        # Label
        if label:
            self.label = QLabel(label)
            layout.addWidget(self.label)
        
        # Input
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("1.000.000,00")
        self.line_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.line_edit.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.line_edit)
        
        self._last_valid_value = 0.0
    
    def _on_text_changed(self, text: str):
        """Handle text change and format."""
        # Remove formatting to get raw number
        from validators.field_validators import CurrencyFormatter
        
        cleaned = text.replace('.', '').replace(',', '').replace(' ', '')
        
        if not cleaned or cleaned == '-':
            self._last_valid_value = 0.0
            self.valueChanged.emit(0.0)
            return
        
        try:
            # Parse as integer cents
            value = float(cleaned) / 100.0 if len(cleaned) > 2 else float(cleaned)
            self._last_valid_value = value
            self.valueChanged.emit(value)
        except ValueError:
            pass
    
    def setValue(self, value: float):
        """Set value with Colombian formatting."""
        from validators.field_validators import CurrencyFormatter
        formatted = CurrencyFormatter.to_colombian_format(value)
        self.line_edit.setText(formatted)
        self._last_valid_value = value
    
    def value(self) -> float:
        """Get current value as float."""
        return self._last_valid_value
    
    def setReadOnly(self, read_only: bool):
        """Set read-only state."""
        self.line_edit.setReadOnly(read_only)
    
    def setEnabled(self, enabled: bool):
        """Enable/disable input."""
        self.line_edit.setEnabled(enabled)
        if hasattr(self, 'label') and self.label:
            self.label.setEnabled(enabled)
