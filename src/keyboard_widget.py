"""
Custom keyboard visualization widget with vintage Compaq aesthetic.
"""
import json
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QBrush
from level_manager import get_resource_path


class KeyboardWidget(QWidget):
    """Custom widget for rendering vintage keyboard with real-time highlighting."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_data = self._load_layout()
        self.current_key = None
        self.next_key = None
        self.shift_pressed = False

        # Calculate widget size
        self._calculate_size()

        self.setMinimumHeight(self.widget_height)

    def _load_layout(self):
        """Load keyboard layout from JSON file."""
        layout_path = get_resource_path('data/keyboard_layout.json')
        try:
            with open(layout_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading keyboard layout: {e}")
            return self._get_default_layout()

    def _get_default_layout(self):
        """Return a minimal default layout if file not found."""
        return {
            "key_size": 50,
            "spacing": 4,
            "colors": {
                "base": "#E8E4D9",
                "current": "#4CAF50",
                "next": "#2196F3",
                "border": "#8C8676",
                "text": "#000000"
            },
            "rows": []
        }

    def _calculate_size(self):
        """Calculate required widget dimensions."""
        key_size = self.layout_data['key_size']
        spacing = self.layout_data['spacing']

        max_width = 0
        max_height = 0

        for row in self.layout_data['rows']:
            row_y = row['y']
            for key in row['keys']:
                key_right = (key['x'] + key['width']) * (key_size + spacing)
                max_width = max(max_width, key_right)

            max_height = max(max_height, (row_y + 1) * (key_size + spacing))

        self.widget_width = int(max_width + spacing)
        self.widget_height = int(max_height + spacing)

    def set_current_char(self, char, next_char=''):
        """
        Set the current character to highlight.

        Args:
            char: Current character to type
            next_char: Next character (for preview)
        """
        self.current_key = self._char_to_key_code(char)
        self.next_key = self._char_to_key_code(next_char)
        self.shift_pressed = char.isupper() or char in '~!@#$%^&*()_+{}|:"<>?'
        self.update()

    def _char_to_key_code(self, char):
        """
        Map character to keyboard key code.

        Args:
            char: Character to map

        Returns:
            str: Key code or None
        """
        if not char:
            return None

        # Character mapping
        char_map = {
            # Letters
            'a': 'KeyA', 'b': 'KeyB', 'c': 'KeyC', 'd': 'KeyD',
            'e': 'KeyE', 'f': 'KeyF', 'g': 'KeyG', 'h': 'KeyH',
            'i': 'KeyI', 'j': 'KeyJ', 'k': 'KeyK', 'l': 'KeyL',
            'm': 'KeyM', 'n': 'KeyN', 'o': 'KeyO', 'p': 'KeyP',
            'q': 'KeyQ', 'r': 'KeyR', 's': 'KeyS', 't': 'KeyT',
            'u': 'KeyU', 'v': 'KeyV', 'w': 'KeyW', 'x': 'KeyX',
            'y': 'KeyY', 'z': 'KeyZ',
            # Numbers (unshifted)
            '0': 'Digit0', '1': 'Digit1', '2': 'Digit2', '3': 'Digit3',
            '4': 'Digit4', '5': 'Digit5', '6': 'Digit6', '7': 'Digit7',
            '8': 'Digit8', '9': 'Digit9',
            # Shifted numbers
            ')': 'Digit0', '!': 'Digit1', '@': 'Digit2', '#': 'Digit3',
            '$': 'Digit4', '%': 'Digit5', '^': 'Digit6', '&': 'Digit7',
            '*': 'Digit8', '(': 'Digit9',
            # Special characters
            ' ': 'Space', '\n': 'Enter', '\t': 'Tab',
            '-': 'Minus', '_': 'Minus',
            '=': 'Equal', '+': 'Equal',
            '[': 'BracketLeft', '{': 'BracketLeft',
            ']': 'BracketRight', '}': 'BracketRight',
            '\\': 'Backslash', '|': 'Backslash',
            ';': 'Semicolon', ':': 'Semicolon',
            "'": 'Quote', '"': 'Quote',
            ',': 'Comma', '<': 'Comma',
            '.': 'Period', '>': 'Period',
            '/': 'Slash', '?': 'Slash',
            '`': 'Backquote', '~': 'Backquote',
        }

        # Handle uppercase letters
        if char.isupper():
            return char_map.get(char.lower())

        return char_map.get(char)

    def paintEvent(self, event):
        """Paint the keyboard."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        painter.fillRect(self.rect(), QColor("#2C2C2C"))

        # Get layout settings
        key_size = self.layout_data['key_size']
        spacing = self.layout_data['spacing']
        colors = self.layout_data['colors']

        # Draw keys
        for row in self.layout_data['rows']:
            row_y = row['y']
            for key in row['keys']:
                self._draw_key(painter, key, row_y, key_size, spacing, colors)

    def _draw_key(self, painter, key, row_y, key_size, spacing, colors):
        """
        Draw a single key.

        Args:
            painter: QPainter instance
            key: Key data dictionary
            row_y: Row index
            key_size: Size of standard key
            spacing: Spacing between keys
            colors: Color scheme
        """
        # Calculate position and size
        x = key['x'] * (key_size + spacing) + spacing
        y = row_y * (key_size + spacing) + spacing
        width = key['width'] * key_size + (key['width'] - 1) * spacing
        height = key_size

        # Determine key color
        key_code = key['code']
        if key_code == self.current_key:
            bg_color = QColor(colors['current'])
        elif key_code in ['ShiftLeft', 'ShiftRight'] and self.shift_pressed:
            bg_color = QColor(colors['current'])  # Highlight shift when needed
        else:
            bg_color = QColor(colors['base'])

        # Draw key background with rounded corners
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(QColor(colors['border']), 2))

        rect = QRectF(x, y, width, height)
        painter.drawRoundedRect(rect, 6, 6)

        # Draw key label
        painter.setPen(QColor(colors['text']))
        font = QFont("Arial", 10, QFont.Bold)
        painter.setFont(font)

        # Draw main label
        label = key['label']
        painter.drawText(rect, Qt.AlignCenter, label)

        # Draw shift label if exists (smaller, in top-right)
        if 'shift_label' in key:
            small_font = QFont("Arial", 8)
            painter.setFont(small_font)
            shift_rect = QRectF(x + width * 0.6, y + 5, width * 0.35, height * 0.3)
            painter.drawText(shift_rect, Qt.AlignCenter, key['shift_label'])

    def sizeHint(self):
        """Return preferred size."""
        from PySide6.QtCore import QSize
        return QSize(self.widget_width, self.widget_height)
