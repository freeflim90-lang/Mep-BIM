# -*- coding: utf-8 -*-
"""
lib/ui_theme.py
---------------
Paleta de cores, helpers de brush e sistema de ícones Unicode
para scripts WPF no pyRevit.

Temas disponíveis:
    "dark"  — escuro padrão (default ao importar)
    "clean" — claro, inversão do dark

Como usar (num script ou em ui_components.py):
    from ui_theme import set_theme
    set_theme("dark")          # antes de qualquer import de ui_components
    from ui_components import *
"""

import clr
clr.AddReference("PresentationCore")
clr.AddReference("PresentationFramework")

from System.Windows.Media import SolidColorBrush, Color, FontFamily
from System.Windows.Controls import TextBlock
from System.Windows import FontWeights

# =============================================================================
# HELPERS DE COR
# =============================================================================

def rgb(r, g, b):
    """Cria um SolidColorBrush opaco a partir de valores RGB (0-255)."""
    return SolidColorBrush(Color.FromRgb(r, g, b))

def rgba(a, r, g, b):
    """Cria um SolidColorBrush com alpha (0=transparente, 255=opaco)."""
    return SolidColorBrush(Color.FromArgb(a, r, g, b))

def semi(brush, alpha=0x30):
    """
    Cria uma versão semi-transparente de um SolidColorBrush existente.

    Args:
        brush (SolidColorBrush): Brush de origem.
        alpha (int): Valor de opacidade 0-255 (padrão: 0x30 ≈ 19%).

    Returns:
        SolidColorBrush com o mesmo RGB mas com alpha aplicado.
    """
    c = brush.Color
    return SolidColorBrush(Color.FromArgb(alpha, c.R, c.G, c.B))

# =============================================================================
# CENTRALIZED ICON SYSTEM
# =============================================================================
# All Unicode icon codepoints are defined here as constants.
# Rendered with "Segoe UI Symbol" to guarantee glyph availability
# across all Windows / Revit environments.

ICONS = {
    "search":       u"\U0001F50D",   # 🔍
    "hash":         "#",              # #
    "edit":         u"\u270F",       # ✏
    "bolt":         u"\u26A1",       # ⚡
    "refresh":      u"\u27F3",       # ⟳
    "revert":       u"\u21A9",       # ↩
    "arrow_right":  u"\u2192",       # →
    "bullet":       u"\u2022",       # •
    "check":        u"\u2714",       # ✔
    "cross":        u"\u2718",       # ✘
    "save":         u"\U0001F4BE",   # 💾
    "warn":         u"\u26A0",       # ⚠
    "info":         u"\u2139",       # ℹ
    "eye":          u"\U0001F441",   # 👁
    "folder":       u"\U0001F4C2",   # 📂
    "doc":          u"\U0001F4C4",   # 📄
}

SYMBOL_FONT = FontFamily("Segoe UI Symbol")


def icon(name):
    """Return the Unicode string for a named icon.

    Args:
        name (str): Icon key from the ICONS dictionary.

    Returns:
        str: Unicode character, or "?" if not found.
    """
    return ICONS.get(name, "?")


def icon_tb(name, color=None, size=14, bold=True):
    """Create a TextBlock pre-configured for icon rendering.

    Uses Segoe UI Symbol font to guarantee glyph availability.

    Args:
        name  (str): Icon key from ICONS.
        color      : SolidColorBrush foreground (defaults: caller sets).
        size  (int): Font size. Defaults to 14.
        bold  (bool): Apply SemiBold weight.

    Returns:
        TextBlock
    """
    tb = TextBlock()
    tb.Text = ICONS.get(name, "?")
    tb.FontFamily = SYMBOL_FONT
    tb.FontSize = size
    if bold:
        tb.FontWeight = FontWeights.SemiBold
    if color:
        tb.Foreground = color
    return tb


def icon_with_text(name, text, color=None, size=14):
    """Create a horizontal StackPanel with an icon followed by text.

    Both icon and text use Segoe UI Symbol for consistent glyph rendering.

    Args:
        name  (str): Icon key from ICONS.
        text  (str): Label text displayed after the icon.
        color      : SolidColorBrush for both icon and text.
        size  (int): Font size. Defaults to 14.

    Returns:
        StackPanel
    """
    from System.Windows.Controls import StackPanel
    from System.Windows import Thickness, VerticalAlignment, Orientation
    panel = StackPanel()
    panel.Orientation = Orientation.Horizontal
    panel.Children.Add(icon_tb(name, color, size))
    tb = TextBlock()
    tb.Text = " " + text
    tb.FontFamily = SYMBOL_FONT
    tb.FontSize = size
    tb.VerticalAlignment = VerticalAlignment.Center
    if color:
        tb.Foreground = color
    panel.Children.Add(tb)
    return panel

# =============================================================================
# VARIÁVEIS GLOBAIS — preenchidas por set_theme()
# =============================================================================

C_BG        = None
C_HEADER    = None
C_PANEL     = None
C_INPUT     = None
C_BORDER    = None
C_HOV       = None   # hover state for interactive rows/items

C_TEXT      = None
C_LABEL     = None
C_MUTED     = None

C_PRIMARY   = None
C_SUCCESS   = None
C_WARNING   = None
C_ERROR     = None

C_DARK_TEXT     = None

# Button state colours — single source of truth for all button styling
C_BTN_BG        = None   # neutral button background (default / disabled visual)
C_BTN_FG        = None   # neutral button text (dark on light themes)
C_BTN_ACTIVE_FG = None   # text on coloured/active buttons — always white

# =============================================================================
# set_theme — único ponto de entrada para escolha de tema
# =============================================================================

def set_theme(name="dark"):
    """
    Define o tema activo reatribuindo todas as variáveis globais de cor.

    Deve ser chamado UMA VEZ, antes de qualquer import de ui_components,
    para que o 'from ui_theme import *' nos outros módulos apanhe os valores
    correctos.

    Args:
        name (str): "dark" (padrão) ou "clean".

    Exemplo:
        from ui_theme import set_theme
        set_theme("clean")
        from ui_components import *
    """
    global C_BG, C_HEADER, C_PANEL, C_INPUT, C_BORDER, C_HOV
    global C_TEXT, C_LABEL, C_MUTED
    global C_PRIMARY, C_SUCCESS, C_WARNING, C_ERROR
    global C_DARK_TEXT, C_BTN_BG, C_BTN_FG, C_BTN_ACTIVE_FG

    if name == "clean":
        # ── CLEAN — claro, inversão do DARK ──────────────────────────────
        C_BG        = rgb(0xED, 0xF0, 0xF7)   # azul-claro
        C_HEADER    = rgb(0xDD, 0xE3, 0xF2)   # azul suave
        C_PANEL     = rgb(0xFF, 0xFF, 0xFF)   # branco
        C_INPUT     = rgb(0xFF, 0xFF, 0xFF)   # branco
        C_BORDER    = rgb(0xC0, 0xC8, 0xDC)   # cinza-azulado
        C_HOV       = rgb(0xC5, 0xCF, 0xE3)   # hover sobre linhas

        C_TEXT      = rgb(0x1C, 0x20, 0x35)   # preto-azulado
        C_LABEL     = rgb(0x2C, 0x32, 0x4A)   # escuro
        C_MUTED     = rgb(0x6B, 0x74, 0x90)   # cinza médio

        C_PRIMARY   = rgb(0x3D, 0x7F, 0xE6)   # azul médio
        C_SUCCESS   = rgb(0x0D, 0x9E, 0x60)   # verde
        C_WARNING   = rgb(0xD4, 0x8A, 0x0A)   # laranja
        C_ERROR     = rgb(0xC8, 0x3B, 0x55)   # vermelho

        C_DARK_TEXT     = rgb(0xFF, 0xFF, 0xFF)   # branco (sobre botões coloridos)
        C_BTN_BG        = rgb(0xDD, 0xE3, 0xF2)   # fundo neutro do botão (= C_HEADER)
        C_BTN_FG        = rgb(0x1C, 0x20, 0x35)   # texto neutro do botão (= C_TEXT)
        C_BTN_ACTIVE_FG = rgb(0xFF, 0xFF, 0xFF)   # texto em botões coloridos — sempre branco

    else:
        # ── DARK (padrão) ─────────────────────────────────────────────────
        C_BG        = rgb(0x22, 0x24, 0x2B)   # cinza-escuro
        C_HEADER    = rgb(0x1B, 0x1D, 0x23)   # quase preto
        C_PANEL     = rgb(0x2B, 0x2E, 0x36)   # painel
        C_INPUT     = rgb(0x30, 0x33, 0x3C)   # cinza input
        C_BORDER    = rgb(0x4A, 0x4F, 0x5C)   # borda
        C_HOV       = rgb(0x3A, 0x3D, 0x4A)   # hover sobre linhas

        C_TEXT      = rgb(0xE6, 0xE8, 0xEE)   # branco
        C_LABEL     = rgb(0xD8, 0xDE, 0xEA)   # branco suave
        C_MUTED     = rgb(0xA9, 0xB1, 0xC1)   # cinza claro

        C_PRIMARY   = rgb(0x6E, 0xA8, 0xFE)   # azul claro
        C_SUCCESS   = rgb(0x26, 0xB3, 0x6D)   # verde
        C_WARNING   = rgb(0xE8, 0xA3, 0x17)   # laranja
        C_ERROR     = rgb(0xE3, 0x6D, 0x83)   # vermelho

        C_DARK_TEXT     = rgb(0x12, 0x14, 0x18)   # preto (sobre botões coloridos)
        C_BTN_BG        = rgb(0x2B, 0x2E, 0x36)   # fundo neutro do botão (= C_PANEL)
        C_BTN_FG        = rgb(0xE6, 0xE8, 0xEE)   # texto neutro do botão (= C_TEXT)
        C_BTN_ACTIVE_FG = rgb(0xFF, 0xFF, 0xFF)   # texto em botões coloridos — sempre branco


# Tema padrão aplicado ao importar o módulo
set_theme("dark")