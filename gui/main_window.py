"""
Main application window with navigation.
"""
from typing import Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel, QStatusBar, QSizePolicy, QFrame
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QKeySequence

from gui.theme import get_stylesheet, ColorScheme, Spacing, Typography
from gui.pages.new_document_page import NewDocumentPage
from gui.pages.payee_management_page import PayeeManagementPage
from gui.pages.history_page import HistoryPage
from gui.pages.settings_page import SettingsPage
from utils.logger import get_logger
from utils.config import config

logger = get_logger(__name__)


class NavigationButton(QPushButton):
    """Custom navigation button with icon and text."""
    
    def __init__(self, text: str, icon_text: str = "", parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(48)
        self.setProperty("styleClass", "nav-button")
        
        # If icon_text provided, use it as emoji/unicode icon
        if icon_text:
            self.setText(f"{icon_text}  {text}")


class MainWindow(QMainWindow):
    """
    Main application window.
    
    Provides navigation between different pages and global actions.
    """
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(f"{config.APP_NAME} - v{config.APP_VERSION}")
        self.setMinimumSize(1200, 800)
        
        # Apply global stylesheet
        self.setStyleSheet(get_stylesheet() + self._get_custom_styles())
        
        # Initialize pages
        self._init_pages()
        
        # Build UI
        self._build_ui()
        
        # Set up menu bar
        self._setup_menu_bar()
        
        # Set up status bar
        self._setup_status_bar()
        
        # Show initial page
        self.navigate_to_page(0)
        
        logger.info("Main window initialized")
    
    def _init_pages(self):
        """Initialize all pages."""
        self.new_document_page = NewDocumentPage(self)
        self.payee_management_page = PayeeManagementPage(self)
        self.history_page = HistoryPage(self)
        self.settings_page = SettingsPage(self)
        
        # Connect signals
        self.new_document_page.document_created.connect(self._on_document_created)
    
    def _build_ui(self):
        """Build the main UI layout."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left navigation panel
        nav_panel = self._create_nav_panel()
        main_layout.addWidget(nav_panel)
        
        # Main content area
        content_area = self._create_content_area()
        main_layout.addWidget(content_area)
    
    def _create_nav_panel(self) -> QWidget:
        """Create left navigation panel."""
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)
        panel.setFixedWidth(220)
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorScheme.SURFACE.value};
                border-right: 1px solid {ColorScheme.BORDER.value};
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(Spacing.MD, Spacing.XL, Spacing.MD, Spacing.MD)
        layout.setSpacing(Spacing.SM)
        
        # App title
        title = QLabel(config.APP_NAME)
        title.setProperty("styleClass", "subtitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        version = QLabel(f"v{config.APP_VERSION}")
        version.setProperty("styleClass", "muted")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        layout.addSpacing(Spacing.XL)
        
        # Navigation buttons
        self.nav_buttons = []
        
        nav_items = [
            ("📄", "Nueva Carta", 0),
            ("🏢", "Aseguradoras", 1),
            ("📚", "Historial", 2),
            ("⚙️", "Configuración", 3),
        ]
        
        for icon, text, page_index in nav_items:
            btn = NavigationButton(text, icon)
            btn.clicked.connect(lambda checked, idx=page_index: self.navigate_to_page(idx))
            self.nav_buttons.append(btn)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # About button at bottom
        about_btn = QPushButton("❓ Acerca de")
        about_btn.clicked.connect(self._show_about)
        layout.addWidget(about_btn)
        
        return panel
    
    def _create_content_area(self) -> QWidget:
        """Create main content area with stacked pages."""
        container = QWidget()
        container.setStyleSheet(f"background-color: {ColorScheme.BACKGROUND.value};")
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Stacked widget for pages
        self.stack = QStackedWidget()
        self.stack.addWidget(self.new_document_page)
        self.stack.addWidget(self.payee_management_page)
        self.stack.addWidget(self.history_page)
        self.stack.addWidget(self.settings_page)
        
        layout.addWidget(self.stack)
        
        return container
    
    def _setup_menu_bar(self):
        """Set up menu bar with keyboard shortcuts."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&Archivo")
        
        new_action = QAction("&Nueva Carta", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(lambda: self.navigate_to_page(0))
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("&Salir", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Herramientas")
        
        payees_action = QAction("Gestionar &Aseguradoras", self)
        payees_action.setShortcut(QKeySequence("Ctrl+M"))
        payees_action.triggered.connect(lambda: self.navigate_to_page(1))
        tools_menu.addAction(payees_action)
        
        history_action = QAction("Ver &Historial", self)
        history_action.setShortcut(QKeySequence("Ctrl+H"))
        history_action.triggered.connect(lambda: self.navigate_to_page(2))
        tools_menu.addAction(history_action)
        
        # Help menu
        help_menu = menubar.addMenu("A&yuda")
        
        about_action = QAction("&Acerca de", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_status_bar(self):
        """Set up status bar."""
        status = QStatusBar()
        self.setStatusBar(status)
        
        # Initial message
        status.showMessage("Listo")
    
    def navigate_to_page(self, page_index: int):
        """
        Navigate to a specific page.
        
        Args:
            page_index: Index of page in stack
        """
        self.stack.setCurrentIndex(page_index)
        
        # Update navigation buttons
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == page_index)
        
        # Update status bar
        page_names = ["Nueva Carta", "Aseguradoras", "Historial", "Configuración"]
        if 0 <= page_index < len(page_names):
            self.statusBar().showMessage(f"Vista: {page_names[page_index]}")
    
    def _on_document_created(self, file_path: str):
        """Handle document creation."""
        from gui.widgets.toast import show_toast
        show_toast(self, f"Carta generada: {file_path}", "success", 5000)
        self.statusBar().showMessage(f"Carta generada: {file_path}", 5000)
    
    def _show_about(self):
        """Show about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        
        QMessageBox.about(
            self,
            "Acerca de",
            f"""
            <h2>{config.APP_NAME}</h2>
            <p>Versión: {config.APP_VERSION}</p>
            <p>Sistema profesional para generación de cartas de cobro para el sector asegurador colombiano.</p>
            <p><b>Características:</b></p>
            <ul>
                <li>Validación automática de NITs colombianos (DIAN)</li>
                <li>Formato de moneda colombiana</li>
                <li>Gestión de aseguradoras beneficiarias</li>
                <li>Numeración consecutiva automática</li>
                <li>Generación de PDFs profesionales</li>
            </ul>
            <p><small>© 2026 SEGUROS UNIÓN</small></p>
            """
        )
    
    def _get_custom_styles(self) -> str:
        """Additional custom styles."""
        return f"""
            QPushButton[styleClass="nav-button"] {{
                text-align: left;
                padding-left: {Spacing.LG}px;
                border: none;
                border-radius: 6px;
                background-color: transparent;
                color: {ColorScheme.TEXT_PRIMARY.value};
                font-size: {Typography.SIZE_BASE};
            }}
            
            QPushButton[styleClass="nav-button"]:hover {{
                background-color: {ColorScheme.BORDER.value};
            }}
            
            QPushButton[styleClass="nav-button"]:checked {{
                background-color: {ColorScheme.PRIMARY.value};
                color: white;
                font-weight: {Typography.WEIGHT_SEMIBOLD};
            }}
        """
