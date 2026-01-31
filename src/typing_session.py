"""
Typing session management with WPM and accuracy tracking.
"""
from PySide6.QtCore import QObject, Signal
import time


class TypingSession(QObject):
    """Manages typing session state, statistics, and progression."""

    # Signals
    char_changed = Signal(str, str)  # current_char, next_char
    stats_updated = Signal(float, float, int)  # wpm, accuracy, char_count
    session_complete = Signal(bool)  # passed

    def __init__(self, text, target_wpm):
        super().__init__()
        self.text = text
        self.target_wpm = target_wpm
        self.current_index = 0
        self.correct_chars = 0
        self.total_keystrokes = 0
        self.start_time = None
        self.errors = []

    def start(self):
        """Start the typing session."""
        self.start_time = time.time()
        self.current_index = 0
        self.correct_chars = 0
        self.total_keystrokes = 0
        self.errors = []
        self._emit_current_char()

    def process_keystroke(self, char):
        """
        Process a keystroke and update statistics.

        Args:
            char: Character typed by the user
        """
        if self.start_time is None:
            self.start()

        self.total_keystrokes += 1
        expected_char = self.text[self.current_index]

        if char == expected_char:
            self.correct_chars += 1
            self.current_index += 1

            # Check if session is complete
            if self.current_index >= len(self.text):
                self._finish_session()
                return

            self._emit_current_char()
        else:
            # Track error but don't advance
            self.errors.append({
                'position': self.current_index,
                'expected': expected_char,
                'typed': char
            })

        self._update_stats()

    def _emit_current_char(self):
        """Emit signal for current and next character."""
        current = self.text[self.current_index] if self.current_index < len(self.text) else ''
        next_char = self.text[self.current_index + 1] if self.current_index + 1 < len(self.text) else ''
        self.char_changed.emit(current, next_char)

    def _update_stats(self):
        """Calculate and emit current statistics."""
        wpm = self.calculate_wpm()
        accuracy = self.calculate_accuracy()
        self.stats_updated.emit(wpm, accuracy, self.current_index)

    def calculate_wpm(self):
        """
        Calculate words per minute.

        Returns:
            float: Current WPM (0 if no time elapsed)
        """
        if self.start_time is None:
            return 0.0

        elapsed_minutes = (time.time() - self.start_time) / 60.0
        if elapsed_minutes == 0:
            return 0.0

        # Standard WPM: characters / 5 / minutes
        return (self.correct_chars / 5.0) / elapsed_minutes

    def calculate_accuracy(self):
        """
        Calculate typing accuracy.

        Returns:
            float: Accuracy percentage (100 if no keystrokes)
        """
        if self.total_keystrokes == 0:
            return 100.0

        return (self.correct_chars / self.total_keystrokes) * 100.0

    def _finish_session(self):
        """Complete the session and check if user passed."""
        wpm = self.calculate_wpm()
        accuracy = self.calculate_accuracy()

        # Pass criteria: target WPM + 95% accuracy
        passed = wpm >= self.target_wpm and accuracy >= 95.0

        self.session_complete.emit(passed)

    def get_current_char(self):
        """Get the current character to type."""
        if self.current_index < len(self.text):
            return self.text[self.current_index]
        return ''

    def get_next_char(self):
        """Get the next character after current."""
        if self.current_index + 1 < len(self.text):
            return self.text[self.current_index + 1]
        return ''
