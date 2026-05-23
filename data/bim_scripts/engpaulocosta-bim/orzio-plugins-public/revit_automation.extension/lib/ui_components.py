# -*- coding: utf-8 -*-
"""
lib/ui_components.py
--------------------
Reusable WPF UI building blocks for pyRevit scripts.
Requires ui_theme.py to be in the same lib/ folder.
"""

import clr
clr.AddReference("System")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("WindowsBase")

import System
import ui_theme as _t

from System.Windows import (
    Thickness, VerticalAlignment, HorizontalAlignment,
    GridLength, GridUnitType, FontWeights, CornerRadius
)
from System.Windows.Controls import (
    StackPanel, TextBlock, TextBox, ComboBox, ComboBoxItem,
    Button, Border, RowDefinition, ColumnDefinition, Orientation
)
from System.Windows.Media import FontFamily, SolidColorBrush, Color
from System.Windows.Input import Cursors
from System.Windows.Markup import XamlReader

# =============================================================================
# GRID HELPERS
# =============================================================================

GL_AUTO = GridLength(1.0, GridUnitType.Auto)
GL_STAR = GridLength(1.0, GridUnitType.Star)

def auto_row():
    rd = RowDefinition()
    rd.Height = GL_AUTO
    return rd

def star_row():
    rd = RowDefinition()
    rd.Height = GL_STAR
    return rd

def auto_col():
    cd = ColumnDefinition()
    cd.Width = GL_AUTO
    return cd

def star_col():
    cd = ColumnDefinition()
    cd.Width = GL_STAR
    return cd

# =============================================================================
# TEXT HELPERS
# =============================================================================

def default_font():
    return FontFamily("Segoe UI")

def lbl(text, color=None, size=13, bold=False, margin=None, width=None):
    """
    Creates a themed TextBlock label.

    Args:
        text   (str)  : Display text.
        color        : SolidColorBrush. Defaults to _t.C_TEXT.
        size   (int)  : Font size. Defaults to 13.
        bold   (bool) : Apply SemiBold weight.
        margin (tuple): (left, top, right, bottom) margin values.
        width  (int)  : Optional fixed width.

    Returns:
        TextBlock
    """
    tb = TextBlock()
    tb.Text = text
    tb.Foreground = color if color else _t.C_TEXT
    tb.FontSize = size
    tb.TextWrapping = System.Windows.TextWrapping.Wrap
    tb.VerticalAlignment = VerticalAlignment.Center
    if bold:
        tb.FontWeight = FontWeights.SemiBold
    if margin:
        tb.Margin = Thickness(margin[0], margin[1], margin[2], margin[3])
    if width:
        tb.Width = width
    return tb

def sec_lbl(text):
    """Creates a section title label (primary color, semibold)."""
    t = lbl(text, _t.C_PRIMARY, 13, bold=True)
    t.Margin = Thickness(0, 14, 0, 4)
    return t

def desc_lbl(text):
    """Creates a small descriptive label (muted color)."""
    t = lbl(text, _t.C_LABEL, 11)
    t.Margin = Thickness(0, 2, 0, 6)
    return t

# =============================================================================
# INPUT HELPERS
# =============================================================================

_INP_STYLE_XAML = (
    '<Style xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"'
    ' TargetType="TextBox">'
    '<Setter Property="Template">'
    '<Setter.Value>'
    '<ControlTemplate TargetType="TextBox">'
    '<Border Name="Bd"'
    ' Background="{TemplateBinding Background}"'
    ' BorderBrush="{TemplateBinding BorderBrush}"'
    ' BorderThickness="{TemplateBinding BorderThickness}">'
    '<ScrollViewer Name="PART_ContentHost" Margin="0"/>'
    '</Border>'
    '</ControlTemplate>'
    '</Setter.Value>'
    '</Setter>'
    '</Style>'
)

def inp(default="", width=110):
    """
    Creates a themed single-line TextBox.
    Focus glow suppressed via custom ControlTemplate.

    Args:
        default (str): Initial text value.
        width   (int): Fixed width in pixels.

    Returns:
        TextBox
    """
    tb = TextBox()
    tb.Text              = str(default)
    tb.Width             = width
    tb.FontSize          = 13
    tb.Padding           = Thickness(8, 6, 8, 6)
    tb.Background        = _t.C_INPUT
    tb.Foreground        = _t.C_TEXT
    tb.BorderBrush       = _t.C_BORDER
    tb.BorderThickness   = Thickness(1)
    tb.VerticalAlignment = VerticalAlignment.Center
    tb.CaretBrush        = _t.C_TEXT
    tb.Style             = XamlReader.Parse(_INP_STYLE_XAML)
    return tb

# =============================================================================
# COMBOBOX — construído via API WPF (sem XAML dinâmico)
# =============================================================================

def combo(items, width=None):
    """
    Creates a themed ComboBox using direct WPF API — no dynamic XAML.
    Colors are read from ui_theme at call time.

    Args:
        items (list): List of (display_label, tag_value) tuples.
        width (int) : Optional fixed width.

    Returns:
        ComboBox
    """
    cb = ComboBox()
    cb.HorizontalAlignment = HorizontalAlignment.Stretch
    cb.Margin              = Thickness(0, 4, 0, 0)
    cb.FontSize            = 13
    cb.Padding             = Thickness(8, 6, 8, 6)
    cb.Background          = _t.C_INPUT
    cb.Foreground          = _t.C_TEXT
    cb.BorderBrush         = _t.C_BORDER
    cb.BorderThickness     = Thickness(1)

    if width:
        cb.Width = width

    for label, tag in items:
        ci            = ComboBoxItem()
        ci.Content    = label
        ci.Tag        = tag
        ci.Background = _t.C_PANEL
        ci.Foreground = _t.C_TEXT
        ci.Padding    = Thickness(8, 5, 8, 5)
        cb.Items.Add(ci)

    if cb.Items.Count > 0:
        cb.SelectedIndex = 0

    return cb

# =============================================================================
# BUTTON HELPER
# =============================================================================

def _is_colored_bg(brush):
    """
    Heuristic: returns True if a SolidColorBrush is a 'colored' background
    (i.e. not a neutral/theme surface).  Used to decide text colour.

    Neutral backgrounds share the same RGB as C_HEADER, C_PANEL, or C_BTN_BG.
    Anything else is treated as coloured/saturated.
    """
    if brush is None:
        return False
    c = brush.Color
    for ref in (_t.C_HEADER, _t.C_PANEL, _t.C_BTN_BG):
        if ref is None:
            continue
        rc = ref.Color
        if c.R == rc.R and c.G == rc.G and c.B == rc.B:
            return False
    return True


def make_btn(text, bg=None, fg=None, handler=None):
    """
    Creates a themed action button with automatic foreground selection.

    Rules (enforced):
    - Neutral buttons (bg == C_BTN_BG / C_PANEL / C_HEADER) → C_BTN_FG
      (dark text on clean theme, light text on dark theme).
    - Coloured/saturated buttons                           → C_BTN_ACTIVE_FG
      (always white for readability).
    - Explicit fg overrides both rules.

    Args:
        text (str): Button label.
        bg        : Background SolidColorBrush. Defaults to C_PRIMARY.
        fg        : Foreground SolidColorBrush (optional override).
        handler   : Click event handler function.

    Returns:
        Button
    """
    b = Button()
    b.Content = text

    bg_brush = bg if bg else _t.C_PRIMARY
    b.Background = bg_brush

    if fg is not None:
        b.Foreground = fg
    elif _is_colored_bg(bg_brush):
        b.Foreground = _t.C_BTN_ACTIVE_FG
    else:
        b.Foreground = _t.C_BTN_FG

    b.FontSize        = 12
    b.FontWeight      = FontWeights.SemiBold
    b.Padding         = Thickness(14, 8, 14, 8)
    b.BorderThickness = Thickness(0)
    b.Cursor          = Cursors.Hand
    if handler:
        b.Click += handler
    return b


def small_btn(text, bg=None, fg=None, handler=None):
    """
    Creates a compact secondary button for toolbars and filter bars.

    Defaults to C_BTN_BG background with automatic text colour.

    Args:
        text (str): Button label.
        bg        : Background SolidColorBrush. Defaults to C_BTN_BG.
        fg        : Foreground SolidColorBrush (optional override).
        handler   : Click event handler function.

    Returns:
        Button
    """
    bg = bg if bg else _t.C_BTN_BG
    b = make_btn(text, bg=bg, fg=fg, handler=handler)
    b.FontSize = 11
    b.Padding  = Thickness(10, 4, 10, 4)
    return b

# =============================================================================
# CONTAINER HELPERS
# =============================================================================

def card(child, padding=(16, 14), margin=(0, 0, 0, 12)):
    """
    Wraps a child element in a styled rounded-card Border.

    Args:
        child         : The WPF element to wrap.
        padding (tuple): (horizontal, vertical) inner padding.
        margin  (tuple): (left, top, right, bottom) outer margin.

    Returns:
        Border
    """
    b = Border()
    b.Background      = _t.C_HEADER
    b.CornerRadius    = CornerRadius(10)
    b.BorderBrush     = _t.C_BORDER
    b.BorderThickness = Thickness(1)
    b.Padding         = Thickness(padding[0], padding[1], padding[0], padding[1])
    b.Margin          = Thickness(margin[0], margin[1], margin[2], margin[3])
    b.Child           = child
    return b


def dot(color=None, size=8, margin=(0, 0, 8, 0)):
    """
    Creates a small circular colour indicator (Ellipse).

    Args:
        color       : Fill SolidColorBrush. Defaults to C_PRIMARY.
        size  (int) : Diameter in pixels. Defaults to 8.
        margin (tuple): (left, top, right, bottom).

    Returns:
        Ellipse
    """
    from System.Windows.Shapes import Ellipse
    e = Ellipse()
    e.Width  = size
    e.Height = size
    e.Fill   = color if color else _t.C_PRIMARY
    e.Margin = Thickness(margin[0], margin[1], margin[2], margin[3])
    e.VerticalAlignment = VerticalAlignment.Center
    return e


def section_header(icon_name, title, subtitle="", icon_color=None):
    """
    Creates a section header row: icon badge + title + optional subtitle.

    The icon is rendered via ui_theme.icon_tb (Segoe UI Symbol) to
    guarantee consistent glyph rendering.

    Args:
        icon_name (str): Key from ui_theme.ICONS.
        title   (str): Section title text.
        subtitle (str): Optional subtitle (smaller, muted).
        icon_color    : Badge background colour. Defaults to semi-primary.

    Returns:
        StackPanel (horizontal)
    """
    panel = StackPanel()
    panel.Orientation = Orientation.Horizontal
    panel.Margin = Thickness(0, 0, 0, 10)

    badge_border = Border()
    badge_border.Width           = 32
    badge_border.Height          = 32
    badge_border.CornerRadius    = CornerRadius(8)
    badge_border.Background      = icon_color if icon_color else _t.semi(_t.C_PRIMARY, 0x33)
    badge_border.Margin          = Thickness(0, 0, 10, 0)
    badge_border.VerticalAlignment = VerticalAlignment.Center

    ic = _t.icon_tb(icon_name, _t.C_PRIMARY, 15, bold=True)
    ic.HorizontalAlignment = HorizontalAlignment.Center
    ic.VerticalAlignment   = VerticalAlignment.Center
    badge_border.Child = ic

    texts = StackPanel()
    texts.Orientation       = Orientation.Vertical
    texts.VerticalAlignment = VerticalAlignment.Center
    texts.Children.Add(lbl(title, size=14, bold=True))
    if subtitle:
        texts.Children.Add(lbl(subtitle, color=_t.C_MUTED, size=11))

    panel.Children.Add(badge_border)
    panel.Children.Add(texts)
    return panel


def warn_box(text, color=None):
    """
    Creates a rounded warning/info box.

    Args:
        text  (str): Warning message text.
        color      : Background brush. Defaults to semi-transparent C_WARNING.

    Returns:
        Border
    """
    b = Border()
    b.Background   = color if color else _t.rgba(55, 0xE8, 0xA3, 0x17)
    b.CornerRadius = CornerRadius(6)
    b.Padding      = Thickness(12, 8, 12, 10)
    b.Margin       = Thickness(0, 4, 0, 8)
    b.Child        = lbl(text, _t.C_LABEL, 11)
    return b

def panel_box(child, padding=10, margin=(0, 4, 0, 12)):
    """
    Wraps a child element in a styled rounded border panel.

    Args:
        child         : The WPF element to wrap.
        padding (int) : Inner padding in pixels.
        margin (tuple): (left, top, right, bottom) outer margin.

    Returns:
        Border
    """
    b = Border()
    b.Background      = _t.C_HEADER
    b.CornerRadius    = CornerRadius(6)
    b.BorderBrush     = _t.C_BORDER
    b.BorderThickness = Thickness(1)
    b.Padding         = Thickness(padding)
    b.Margin          = Thickness(margin[0], margin[1], margin[2], margin[3])
    b.Child           = child
    return b

def hrow(*children):
    """
    Creates a horizontal StackPanel.

    Args:
        *children: WPF elements to arrange horizontally.

    Returns:
        StackPanel
    """
    p = StackPanel()
    p.Orientation = Orientation.Horizontal
    for c in children:
        p.Children.Add(c)
    return p

# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def _set_valid(tb, valid):
    """Marks a TextBox as valid (normal border) or invalid (red border)."""
    tb.BorderBrush     = _t.C_BORDER if valid else _t.C_ERROR
    tb.BorderThickness = Thickness(1) if valid else Thickness(2)

def attach_numeric_validator(tb, allow_zero=True):
    """
    Attaches a live validator to a TextBox.

    Args:
        tb         (TextBox): The input field to validate.
        allow_zero (bool)   : Whether zero is a valid value.
    """
    def _on_changed(sender, e):
        try:
            v  = float(str(tb.Text).strip().replace(",", "."))
            ok = (v >= 0) if allow_zero else (v > 0)
        except Exception:
            ok = False
        _set_valid(tb, ok)
    tb.TextChanged += _on_changed

# =============================================================================
# WINDOW THEME
# =============================================================================

def apply_window_theme(win):
    """
    Applies the active theme background and font to a WPF Window.

    Args:
        win (Window): The window instance to theme.
    """
    win.Background = _t.C_BG
    win.FontFamily = default_font()