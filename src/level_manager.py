"""
Level definitions and text corpus management.
"""
import os
import sys
import json
import random


def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and PyInstaller.

    Args:
        relative_path: Path relative to project root

    Returns:
        str: Absolute path to resource
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        # Running in development
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class LevelManager:
    """Manages typing levels and progression."""

    LEVELS = {
        1: {
            "name": "Business - Beginner",
            "target_wpm": 50,
            "files": [f"level1_business_{i}.txt" for i in range(1, 6)],
            "description": "Professional emails and documents"
        },
        2: {
            "name": "Business - Advanced",
            "target_wpm": 80,
            "files": [f"level2_business_{i}.txt" for i in range(1, 6)],
            "description": "Fast-paced business communication"
        },
        3: {
            "name": "Code - Beginner",
            "target_wpm": 20,
            "files": [f"level3_code_{i}.py" for i in range(1, 6)],
            "description": "Python basics with special characters"
        },
        4: {
            "name": "Code - Advanced",
            "target_wpm": 50,
            "files": [f"level4_code_{i}.py" for i in range(1, 6)],
            "description": "Complex code with symbols"
        },
        5: {
            "name": "Mixed - Master",
            "target_wpm": 40,
            "files": [f"level5_mixed_{i}.md" for i in range(1, 6)],
            "description": "Markdown with inline code blocks"
        }
    }

    def __init__(self):
        self.progress = self._load_progress()

    def get_level_info(self, level_num):
        """
        Get information about a specific level.

        Args:
            level_num: Level number (1-5)

        Returns:
            dict: Level information or None
        """
        return self.LEVELS.get(level_num)

    def get_level_text(self, level_num):
        """
        Load the practice text for a level (randomly chooses from available files).

        Args:
            level_num: Level number (1-5)

        Returns:
            str: Practice text content

        Raises:
            ValueError: If level doesn't exist
            FileNotFoundError: If level file not found
        """
        level_info = self.get_level_info(level_num)
        if not level_info:
            raise ValueError(f"Invalid level number: {level_num}")

        # Randomly choose one of the lesson files
        chosen_file = random.choice(level_info['files'])
        file_path = get_resource_path(os.path.join('data', 'levels', chosen_file))

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Level file not found: {file_path}")

    def get_all_levels(self):
        """
        Get list of all levels with their info.

        Returns:
            list: List of tuples (level_num, level_info)
        """
        return sorted(self.LEVELS.items())

    def _get_progress_path(self):
        """Get path to progress file."""
        home = os.path.expanduser('~')
        progress_dir = os.path.join(home, '.typing_tutor')
        os.makedirs(progress_dir, exist_ok=True)
        return os.path.join(progress_dir, 'progress.json')

    def _load_progress(self):
        """
        Load user progress from file.

        Returns:
            dict: Progress data
        """
        progress_path = self._get_progress_path()
        if os.path.exists(progress_path):
            try:
                with open(progress_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        # Default progress structure
        return {level: {"best_wpm": 0, "best_accuracy": 0, "completed": False}
                for level in self.LEVELS.keys()}

    def save_progress(self, level_num, wpm, accuracy, passed):
        """
        Save progress for a level.

        Args:
            level_num: Level number
            wpm: Words per minute achieved
            accuracy: Accuracy percentage
            passed: Whether the level was passed
        """
        if level_num not in self.progress:
            self.progress[level_num] = {"best_wpm": 0, "best_accuracy": 0, "completed": False}

        level_progress = self.progress[level_num]

        # Update best scores
        if wpm > level_progress["best_wpm"]:
            level_progress["best_wpm"] = wpm

        if accuracy > level_progress["best_accuracy"]:
            level_progress["best_accuracy"] = accuracy

        if passed:
            level_progress["completed"] = True

        # Save to file
        try:
            with open(self._get_progress_path(), 'w') as f:
                json.dump(self.progress, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save progress: {e}")

    def get_level_progress(self, level_num):
        """
        Get progress for a specific level.

        Args:
            level_num: Level number

        Returns:
            dict: Progress data
        """
        return self.progress.get(level_num, {"best_wpm": 0, "best_accuracy": 0, "completed": False})
