"""
Design system and theming for the application.

Provides consistent colors, spacing, typography, and QSS stylesheets.
"""
from typing import Dict
from enum import Enum


class ColorScheme(Enum):
    """Application color palette."""
    # Primary colors
    PRIMARY = "#0066CC"
    PRIMARY_HOVER = "#0052A3"
    PRIMARY_PRESSED = "#003D7A"
    
    # Secondary colors
    SECONDARY = "#6C757D"
    SECONDARY_HOVER = "#5A6268"
    
    # Semantic colors
    SUCCESS = "#28A745"
    WARNING = "#FFC107"
    DANGER = "#DC3545"
    INFO = "#17A2B8"
    
    # Neutral colors
    BACKGROUND = "#FFFFFF"
    SURFACE = "#F8F9FA"
    BORDER = "#DEE2E6"
    TEXT_PRIMARY = "#212529"
    TEXT_SECONDARY = "#6C757D"
    TEXT_DISABLED = "#ADB5BD"
    
    # Dark mode (optional)
    DARK_BACKGROUND = "#1E1E1E"
    DARK_SURFACE = "#2D2D2D"
    DARK_BORDER = "#404040"


class Spacing:
    """Consistent spacing scale (in pixels)."""
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 24
    XXL = 32
    XXXL = 48


class Typography:
    """Font definitions."""
    FAMILY = "Segoe UI, -apple-system, BlinkMacSystemFont, sans-serif"
    SIZE_SM = "11px"
    SIZE_BASE = "13px"
    SIZE_LG = "15px"
    SIZE_XL = "18px"
    SIZE_XXL = "24px"
    
    WEIGHT_NORMAL = "normal"
    WEIGHT_MEDIUM = "500"
    WEIGHT_SEMIBOLD = "600"
    WEIGHT_BOLD = "bold"


class BorderRadius:
    """Border radius values."""
    SM = "3px"
    MD = "6px"
    LG = "8px"
    PILL = "999px"


def get_stylesheet() -> str:
    """
    Returns the main application stylesheet.
    
    Returns:
        str: Complete QSS stylesheet
    """
    return f"""
    /* ========== GLOBAL STYLES ========== */
    * {{
        font-family: {Typography.FAMILY};
        font-size: {Typography.SIZE_BASE};
    }}
    
    QMainWindow {{
        background-color: {ColorScheme.BACKGROUND.value};
    }}
    
    /* ========== BUTTONS ========== */
    QPushButton {{
        background-color: {ColorScheme.SURFACE.value};
        border: 1px solid {ColorScheme.BORDER.value};
        border-radius: {BorderRadius.MD};
        padding: {Spacing.SM}px {Spacing.LG}px;
        color: {ColorScheme.TEXT_PRIMARY.value};
        font-weight: {Typography.WEIGHT_MEDIUM};
    }}
    
    QPushButton:hover {{
        background-color: {ColorScheme.BORDER.value};
        border-color: {ColorScheme.SECONDARY.value};
    }}
    
    QPushButton:pressed {{
        background-color: {ColorScheme.BORDER.value};
    }}
    
    QPushButton:disabled {{
        background-color: {ColorScheme.SURFACE.value};
        color: {ColorScheme.TEXT_DISABLED.value};
        border-color: {ColorScheme.BORDER.value};
    }}
    
    QPushButton[styleClass="primary"] {{
        background-color: {ColorScheme.PRIMARY.value};
        border: none;
        color: white;
    }}
    
    QPushButton[styleClass="primary"]:hover {{
        background-color: {ColorScheme.PRIMARY_HOVER.value};
    }}
    
    QPushButton[styleClass="primary"]:pressed {{
        background-color: {ColorScheme.PRIMARY_PRESSED.value};
    }}
    
    QPushButton[styleClass="danger"] {{
        background-color: {ColorScheme.DANGER.value};
        border: none;
        color: white;
    }}
    
    QPushButton[styleClass="danger"]:hover {{
        background-color: #C82333;
    }}
    
    QPushButton[styleClass="success"] {{
        background-color: {ColorScheme.SUCCESS.value};
        border: none;
        color: white;
    }}
    
    QPushButton[styleClass="icon"] {{
        border: none;
        background: transparent;
        padding: {Spacing.SM}px;
    }}
    
    QPushButton[styleClass="icon"]:hover {{
        background-color: {ColorScheme.SURFACE.value};
        border-radius: {BorderRadius.SM};
    }}
    
    /* ========== INPUTS ========== */
    QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox {{
        border: 1px solid {ColorScheme.BORDER.value};
        border-radius: {BorderRadius.SM};
        padding: {Spacing.SM}px {Spacing.MD}px;
        background-color: white;
        selection-background-color: {ColorScheme.PRIMARY.value};
    }}
    
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, 
    QDateEdit:focus, QComboBox:focus {{
        border-color: {ColorScheme.PRIMARY.value};
        border-width: 2px;
    }}
    
    QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled,
    QDateEdit:disabled, QComboBox:disabled {{
        background-color: {ColorScheme.SURFACE.value};
        color: {ColorScheme.TEXT_DISABLED.value};
    }}
    
    QLineEdit[hasError="true"] {{
        border-color: {ColorScheme.DANGER.value};
        border-width: 2px;
    }}
    
    /* ========== COMBOBOX ========== */
    QComboBox {{
        padding-right: {Spacing.XL}px;
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: {Spacing.XL}px;
    }}
    
    QComboBox::down-arrow {{
        image: url(none);
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {ColorScheme.TEXT_SECONDARY.value};
        margin-right: {Spacing.SM}px;
    }}
    
    QComboBox QAbstractItemView {{
        border: 1px solid {ColorScheme.BORDER.value};
        selection-background-color: {ColorScheme.PRIMARY.value};
        selection-color: white;
        background-color: white;
        outline: none;
    }}
    
    /* ========== TEXT AREAS ========== */
    QTextEdit, QPlainTextEdit {{
        border: 1px solid {ColorScheme.BORDER.value};
        border-radius: {BorderRadius.SM};
        padding: {Spacing.SM}px;
        background-color: white;
    }}
    
    /* ========== TABLES ========== */
    QTableView {{
        border: 1px solid {ColorScheme.BORDER.value};
        border-radius: {BorderRadius.SM};
        background-color: white;
        gridline-color: {ColorScheme.BORDER.value};
        selection-background-color: {ColorScheme.PRIMARY.value};
        selection-color: white;
    }}
    
    QTableView::item {{
        padding: {Spacing.SM}px;
    }}
    
    QTableView::item:alternate {{
        background-color: {ColorScheme.SURFACE.value};
    }}
    
    QHeaderView::section {{
        background-color: {ColorScheme.SURFACE.value};
        border: none;
        border-bottom: 2px solid {ColorScheme.BORDER.value};
        border-right: 1px solid {ColorScheme.BORDER.value};
        padding: {Spacing.SM}px {Spacing.MD}px;
        font-weight: {Typography.WEIGHT_SEMIBOLD};
    }}
    
    QHeaderView::section:last {{
        border-right: none;
    }}
    
    /* ========== TABS ========== */
    QTabWidget::pane {{
        border: 1px solid {ColorScheme.BORDER.value};
        border-radius: {BorderRadius.SM};
        top: -1px;
    }}
    
    QTabBar::tab {{
        background-color: {ColorScheme.SURFACE.value};
        border: 1px solid {ColorScheme.BORDER.value};
        border-bottom: none;
        border-top-left-radius: {BorderRadius.SM};
        border-top-right-radius: {BorderRadius.SM};
        padding: {Spacing.SM}px {Spacing.LG}px;
        margin-right: 2px;
    }}
    
    QTabBar::tab:selected {{
        background-color: white;
        border-bottom: 2px solid {ColorScheme.PRIMARY.value};
    }}
    
    QTabBar::tab:hover {{
        background-color: {ColorScheme.BORDER.value};
    }}
    
    /* ========== SCROLLBARS ========== */
    QScrollBar:vertical {{
        border: none;
        background: {ColorScheme.SURFACE.value};
        width: 12px;
        margin: 0;
    }}
    
    QScrollBar::handle:vertical {{
        background: {ColorScheme.BORDER.value};
        min-height: 20px;
        border-radius: 6px;
        margin: 2px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {ColorScheme.SECONDARY.value};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        border: none;
        background: {ColorScheme.SURFACE.value};
        height: 12px;
        margin: 0;
    }}
    
    QScrollBar::handle:horizontal {{
        background: {ColorScheme.BORDER.value};
        min-width: 20px;
        border-radius: 6px;
        margin: 2px;
    }}
    
    /* ========== PROGRESS BAR ========== */
    QProgressBar {{
        border: 1px solid {ColorScheme.BORDER.value};
        border-radius: {BorderRadius.SM};
        text-align: center;
        background-color: {ColorScheme.SURFACE.value};
    }}
    
    QProgressBar::chunk {{
        background-color: {ColorScheme.PRIMARY.value};
        border-radius: {BorderRadius.SM};
    }}
    
    /* ========== LABELS ========== */
    QLabel[styleClass="title"] {{
        font-size: {Typography.SIZE_XXL};
        font-weight: {Typography.WEIGHT_BOLD};
        color: {ColorScheme.TEXT_PRIMARY.value};
    }}
    
    QLabel[styleClass="subtitle"] {{
        font-size: {Typography.SIZE_XL};
        font-weight: {Typography.WEIGHT_SEMIBOLD};
        color: {ColorScheme.TEXT_PRIMARY.value};
    }}
    
    QLabel[styleClass="section-header"] {{
        font-size: {Typography.SIZE_LG};
        font-weight: {Typography.WEIGHT_SEMIBOLD};
        color: {ColorScheme.TEXT_PRIMARY.value};
        padding: {Spacing.MD}px 0;
    }}
    
    QLabel[styleClass="muted"] {{
        color: {ColorScheme.TEXT_SECONDARY.value};
        font-size: {Typography.SIZE_SM};
    }}
    
    QLabel[styleClass="error"] {{
        color: {ColorScheme.DANGER.value};
        font-size: {Typography.SIZE_SM};
    }}
    
    QLabel[styleClass="success"] {{
        color: {ColorScheme.SUCCESS.value};
        font-size: {Typography.SIZE_SM};
    }}
    
    /* ========== GROUP BOX ========== */
    QGroupBox {{
        border: 1px solid {ColorScheme.BORDER.value};
        border-radius: {BorderRadius.MD};
        margin-top: {Spacing.LG}px;
        padding-top: {Spacing.LG}px;
        font-weight: {Typography.WEIGHT_SEMIBOLD};
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: {Spacing.MD}px;
        padding: 0 {Spacing.SM}px;
        background-color: {ColorScheme.BACKGROUND.value};
    }}
    
    /* ========== STATUS BAR ========== */
    QStatusBar {{
        background-color: {ColorScheme.SURFACE.value};
        border-top: 1px solid {ColorScheme.BORDER.value};
    }}
    
    QStatusBar::item {{
        border: none;
    }}
    
    /* ========== MENU BAR ========== */
    QMenuBar {{
        background-color: {ColorScheme.BACKGROUND.value};
        border-bottom: 1px solid {ColorScheme.BORDER.value};
    }}
    
    QMenuBar::item {{
        padding: {Spacing.SM}px {Spacing.MD}px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {ColorScheme.SURFACE.value};
    }}
    
    QMenu {{
        background-color: white;
        border: 1px solid {ColorScheme.BORDER.value};
    }}
    
    QMenu::item {{
        padding: {Spacing.SM}px {Spacing.XL}px;
    }}
    
    QMenu::item:selected {{
        background-color: {ColorScheme.PRIMARY.value};
        color: white;
    }}
    
    /* ========== CHECKBOXES & RADIO BUTTONS ========== */
    QCheckBox, QRadioButton {{
        spacing: {Spacing.SM}px;
    }}
    
    QCheckBox::indicator, QRadioButton::indicator {{
        width: 18px;
        height: 18px;
    }}
    
    QCheckBox::indicator {{
        border: 2px solid {ColorScheme.BORDER.value};
        border-radius: {BorderRadius.SM};
        background: white;
    }}
    
    QCheckBox::indicator:checked {{
        background: {ColorScheme.PRIMARY.value};
        border-color: {ColorScheme.PRIMARY.value};
    }}
    
    /* ========== SPLITTER ========== */
    QSplitter::handle {{
        background-color: {ColorScheme.BORDER.value};
    }}
    
    QSplitter::handle:horizontal {{
        width: 1px;
    }}
    
    QSplitter::handle:vertical {{
        height: 1px;
    }}
    """


def get_card_style() -> str:
    """Returns CSS for card-like containers."""
    return f"""
        background-color: white;
        border: 1px solid {ColorScheme.BORDER.value};
        border-radius: {BorderRadius.MD};
        padding: {Spacing.LG}px;
    """


def get_form_layout_spacing() -> Dict[str, int]:
    """Returns standard spacing for form layouts."""
    return {
        'horizontal_spacing': Spacing.LG,
        'vertical_spacing': Spacing.MD,
        'label_spacing': Spacing.SM,
    }
