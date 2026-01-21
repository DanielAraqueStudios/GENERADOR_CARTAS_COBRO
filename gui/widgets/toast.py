"""
Toast notification widget for displaying temporary messages.
"""
from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt, pyqtSignal
from PyQt6.QtGui import QPalette
from gui.theme import ColorScheme, Spacing, BorderRadius, Typography


class Toast(QLabel):
    """
    Toast notification that auto-dismisses.
    
    Shows at the bottom-right of parent widget.
    """
    
    closed = pyqtSignal()
    
    def __init__(self, message: str, toast_type: str = 'info', parent=None, duration: int = 3000):
        """
        Initialize toast notification.
        
        Args:
            message: Text to display
            toast_type: 'success', 'error', 'warning', 'info'
            parent: Parent widget
            duration: How long to show (milliseconds)
        """
        super().__init__(message, parent)
        self.duration = duration
        self.toast_type = toast_type
        
        self.setWordWrap(True)
        self.setMaximumWidth(400)
        self.setMinimumWidth(250)
        
        # Style based on type
        self._apply_style()
        
        # Set up fade animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(200)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out_animation.setDuration(200)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out_animation.finished.connect(self._on_fade_out_finished)
        
        # Auto-dismiss timer
        self.dismiss_timer = QTimer(self)
        self.dismiss_timer.setSingleShot(True)
        self.dismiss_timer.timeout.connect(self.dismiss)
        
        # Position at bottom-right
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
    def _apply_style(self):
        """Apply styling based on toast type."""
        colors = {
            'success': (ColorScheme.SUCCESS.value, 'white'),
            'error': (ColorScheme.DANGER.value, 'white'),
            'warning': (ColorScheme.WARNING.value, ColorScheme.TEXT_PRIMARY.value),
            'info': (ColorScheme.INFO.value, 'white'),
        }
        
        bg_color, text_color = colors.get(self.toast_type, colors['info'])
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: {BorderRadius.MD};
                padding: {Spacing.MD}px {Spacing.LG}px;
                font-size: {Typography.SIZE_BASE};
                font-weight: {Typography.WEIGHT_MEDIUM};
            }}
        """)
    
    def show_toast(self):
        """Show the toast with animation."""
        self.show()
        self.raise_()
        
        # Position at bottom-right of parent
        if self.parent():
            parent_rect = self.parent().rect()
            x = parent_rect.right() - self.width() - Spacing.XL
            y = parent_rect.bottom() - self.height() - Spacing.XL
            self.move(x, y)
        
        # Fade in
        self.fade_in_animation.start()
        
        # Start dismiss timer
        self.dismiss_timer.start(self.duration)
    
    def dismiss(self):
        """Dismiss the toast with fade-out animation."""
        self.dismiss_timer.stop()
        self.fade_out_animation.start()
    
    def _on_fade_out_finished(self):
        """Handle fade-out completion."""
        self.closed.emit()
        self.deleteLater()


def show_toast(parent, message: str, toast_type: str = 'info', duration: int = 3000):
    """
    Convenience function to show a toast notification.
    
    Args:
        parent: Parent widget to attach toast to
        message: Message to display
        toast_type: 'success', 'error', 'warning', 'info'
        duration: Duration in milliseconds
    
    Returns:
        Toast: The toast widget (usually not needed)
    """
    toast = Toast(message, toast_type, parent, duration)
    toast.show_toast()
    return toast
