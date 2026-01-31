"""
Typing Tutor Application - Main Entry Point
"""
import sys
from PySide6.QtWidgets import QApplication
from level_manager import LevelManager
from ui.main_window import MainWindow


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Create level manager
    level_manager = LevelManager()

    # Create and show main window
    window = MainWindow(level_manager)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
