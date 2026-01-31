"""
Main application window.
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QComboBox, QTextEdit, QLabel, QPushButton,
                                QMessageBox, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QTextCharFormat, QColor, QTextCursor
from keyboard_widget import KeyboardWidget


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, level_manager):
        super().__init__()
        self.level_manager = level_manager
        self.current_session = None

        # Text chunking variables
        self.full_text = ""
        self.text_lines = []
        self.current_chunk_start_line = 0
        self.lines_per_chunk = 10
        self.chunk_char_offset = 0  # Character offset of current chunk in full text

        self.setWindowTitle("Typing Tutor - Vintage Compaq Edition")
        self.setMinimumSize(800, 600)

        # Enable keyboard focus for the main window
        self.setFocusPolicy(Qt.StrongFocus)

        self._setup_ui()
        self._load_level(1)  # Start with level 1

        # Grab keyboard focus immediately
        self.setFocus()

    def _setup_ui(self):
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Level selector
        level_layout = QHBoxLayout()
        level_label = QLabel("Level:")
        self.level_combo = QComboBox()

        for level_num, level_info in self.level_manager.get_all_levels():
            progress = self.level_manager.get_level_progress(level_num)
            completed_mark = "✓ " if progress["completed"] else ""
            label = f"{completed_mark}Level {level_num}: {level_info['name']} ({level_info['target_wpm']} WPM)"
            self.level_combo.addItem(label, level_num)

        self.level_combo.currentIndexChanged.connect(self._on_level_changed)

        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_combo, 1)
        layout.addLayout(level_layout)

        # Practice text display
        text_label = QLabel("Practice Text:")
        layout.addWidget(text_label)

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Courier New", 12))
        self.text_display.setMinimumHeight(200)
        # Disable scrollbars - we'll show text in chunks
        self.text_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Prevent text display from accepting keyboard focus or events
        self.text_display.setFocusPolicy(Qt.NoFocus)
        self.text_display.setTextInteractionFlags(Qt.NoTextInteraction)
        layout.addWidget(self.text_display)

        # Keyboard widget
        keyboard_label = QLabel("Keyboard Visualization:")
        layout.addWidget(keyboard_label)

        # Create keyboard widget with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(False)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.keyboard_widget = KeyboardWidget()
        scroll_area.setWidget(self.keyboard_widget)
        scroll_area.setMinimumHeight(300)
        layout.addWidget(scroll_area)

        # Stats display
        stats_layout = QHBoxLayout()
        self.wpm_label = QLabel("WPM: 0")
        self.wpm_label.setFont(QFont("Arial", 14, QFont.Bold))

        self.accuracy_label = QLabel("Accuracy: 100%")
        self.accuracy_label.setFont(QFont("Arial", 14, QFont.Bold))

        self.progress_label = QLabel("Progress: 0/0")
        self.progress_label.setFont(QFont("Arial", 14, QFont.Bold))

        stats_layout.addWidget(self.wpm_label)
        stats_layout.addWidget(QLabel(" | "))
        stats_layout.addWidget(self.accuracy_label)
        stats_layout.addWidget(QLabel(" | "))
        stats_layout.addWidget(self.progress_label)
        stats_layout.addStretch()

        # Reset button
        self.reset_button = QPushButton("Reset Level")
        self.reset_button.clicked.connect(self._reset_session)
        stats_layout.addWidget(self.reset_button)

        layout.addLayout(stats_layout)

    def _load_level(self, level_num):
        """Load a specific level."""
        try:
            level_info = self.level_manager.get_level_info(level_num)
            text = self.level_manager.get_level_text(level_num)

            # Import here to avoid circular dependency
            from typing_session import TypingSession

            self.current_session = TypingSession(text, level_info['target_wpm'])
            self.current_session.char_changed.connect(self._on_char_changed)
            self.current_session.stats_updated.connect(self._on_stats_updated)
            self.current_session.session_complete.connect(self._on_session_complete)

            # Initialize text chunking
            self.full_text = text
            self.text_lines = text.split('\n')
            self.current_chunk_start_line = 0
            self.chunk_char_offset = 0

            # Display first chunk
            self._update_text_chunk()
            self._highlight_text(0)

            # Update keyboard to show first character
            if len(text) > 0:
                first_char = text[0]
                next_char = text[1] if len(text) > 1 else ''
                self.keyboard_widget.set_current_char(first_char, next_char)

            # Update stats
            self.wpm_label.setText("WPM: 0")
            self.accuracy_label.setText("Accuracy: 100%")
            self.progress_label.setText(f"Progress: 0/{len(text)}")

            # Set window title
            self.setWindowTitle(f"Typing Tutor - {level_info['name']}")

            # Grab focus so typing works immediately
            self.setFocus()

        except (ValueError, FileNotFoundError) as e:
            QMessageBox.critical(self, "Error", f"Failed to load level: {e}")

    def _on_level_changed(self, index):
        """Handle level selection change."""
        level_num = self.level_combo.itemData(index)
        self._load_level(level_num)

    def _reset_session(self):
        """Reset the current session."""
        current_index = self.level_combo.currentIndex()
        level_num = self.level_combo.itemData(current_index)
        self._load_level(level_num)

    def _update_text_chunk(self):
        """Update the displayed text chunk based on current position."""
        # Get lines for current chunk
        end_line = min(self.current_chunk_start_line + self.lines_per_chunk, len(self.text_lines))
        chunk_lines = self.text_lines[self.current_chunk_start_line:end_line]
        chunk_text = '\n'.join(chunk_lines)

        # Calculate character offset of this chunk in full text
        if self.current_chunk_start_line > 0:
            preceding_lines = self.text_lines[:self.current_chunk_start_line]
            # +1 for each newline character
            self.chunk_char_offset = sum(len(line) + 1 for line in preceding_lines)
        else:
            self.chunk_char_offset = 0

        # Display the chunk
        self.text_display.setPlainText(chunk_text)

    def _get_position_in_chunk(self, absolute_position):
        """Convert absolute text position to position within current chunk."""
        return absolute_position - self.chunk_char_offset

    def _on_char_changed(self, current_char, next_char):
        """Handle character change signal."""
        # Update keyboard highlighting
        self.keyboard_widget.set_current_char(current_char, next_char)

    def _on_stats_updated(self, wpm, accuracy, char_count):
        """Handle statistics update."""
        self.wpm_label.setText(f"WPM: {wpm:.1f}")
        self.accuracy_label.setText(f"Accuracy: {accuracy:.1f}%")
        self.progress_label.setText(f"Progress: {char_count}/{len(self.current_session.text)}")

        # Check if we need to advance to next chunk
        chunk_end_offset = self.chunk_char_offset + len(self.text_display.toPlainText())

        # If we're past 80% of current chunk, load next chunk
        chunk_progress = char_count - self.chunk_char_offset
        chunk_length = len(self.text_display.toPlainText())

        if chunk_length > 0 and chunk_progress > chunk_length * 0.8:
            # Check if there are more lines to show
            if self.current_chunk_start_line + self.lines_per_chunk < len(self.text_lines):
                self.current_chunk_start_line += self.lines_per_chunk
                self._update_text_chunk()

        # Update text highlighting with position relative to current chunk
        position_in_chunk = self._get_position_in_chunk(char_count)
        self._highlight_text(position_in_chunk)

    def _on_session_complete(self, passed):
        """Handle session completion."""
        wpm = self.current_session.calculate_wpm()
        accuracy = self.current_session.calculate_accuracy()

        # Save progress
        current_index = self.level_combo.currentIndex()
        level_num = self.level_combo.itemData(current_index)
        self.level_manager.save_progress(level_num, wpm, accuracy, passed)

        # Show completion message
        if passed:
            message = f"Congratulations! You passed!\n\nWPM: {wpm:.1f}\nAccuracy: {accuracy:.1f}%"
            QMessageBox.information(self, "Level Complete", message)
        else:
            level_info = self.level_manager.get_level_info(level_num)
            target = level_info['target_wpm']
            message = f"Good effort! Keep practicing.\n\nWPM: {wpm:.1f} (Target: {target})\nAccuracy: {accuracy:.1f}% (Target: 95%)"
            QMessageBox.information(self, "Level Complete", message)

        # Refresh level combo to show completion status
        self._refresh_level_combo()

    def _refresh_level_combo(self):
        """Refresh the level combo box to show updated completion status."""
        current_index = self.level_combo.currentIndex()
        self.level_combo.clear()

        for level_num, level_info in self.level_manager.get_all_levels():
            progress = self.level_manager.get_level_progress(level_num)
            completed_mark = "✓ " if progress["completed"] else ""
            label = f"{completed_mark}Level {level_num}: {level_info['name']} ({level_info['target_wpm']} WPM)"
            self.level_combo.addItem(label, level_num)

        self.level_combo.setCurrentIndex(current_index)

    def _highlight_text(self, position):
        """
        Highlight the current character in the text display.

        Args:
            position: Current character position within the chunk
        """
        # Get current chunk text length
        chunk_text = self.text_display.toPlainText()
        chunk_length = len(chunk_text)

        cursor = self.text_display.textCursor()
        cursor.select(QTextCursor.Document)

        # Reset formatting
        normal_format = QTextCharFormat()
        cursor.setCharFormat(normal_format)

        # Highlight completed text (blue background, white text) within this chunk
        if position > 0 and position <= chunk_length:
            cursor.setPosition(0)
            cursor.setPosition(min(position, chunk_length), QTextCursor.KeepAnchor)
            completed_format = QTextCharFormat()
            completed_format.setBackground(QColor("#2196F3"))  # Blue
            completed_format.setForeground(QColor("#FFFFFF"))  # White text
            cursor.setCharFormat(completed_format)

        # Highlight current character (white background, blue text)
        if position >= 0 and position < chunk_length:
            cursor.setPosition(position)
            cursor.setPosition(position + 1, QTextCursor.KeepAnchor)
            current_format = QTextCharFormat()
            current_format.setBackground(QColor("#FFFFFF"))  # White background
            current_format.setForeground(QColor("#2196F3"))  # Blue text
            cursor.setCharFormat(current_format)

        # Reset cursor to beginning (no selection)
        cursor.setPosition(0)
        cursor.clearSelection()
        self.text_display.setTextCursor(cursor)

    def keyPressEvent(self, event):
        """Handle key press events."""
        if self.current_session is None:
            return

        # Get the typed character
        text = event.text()

        # Handle special keys
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            text = '\n'
        elif event.key() == Qt.Key_Tab:
            text = '\t'
        elif not text:
            # Ignore other special keys (arrows, etc.)
            return

        # Process the keystroke
        self.current_session.process_keystroke(text)
