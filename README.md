# TypeTutor - Vintage Keyboard Typing Trainer

A beautiful typing tutor application with a vintage Compaq Presario keyboard aesthetic, real-time feedback, and progressive difficulty levels covering both business writing and coding skills.

![TypeTutor Interface](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🎨 **Vintage Keyboard Visualization** - Real-time blue highlighting with classic beige Compaq aesthetic
- 📊 **5 Progressive Difficulty Levels** - From beginner business writing to advanced coding
- 📝 **25 Unique Lessons** - 5 random variations per level for variety
- ⚡ **Real-time Statistics** - Live WPM, accuracy, and progress tracking
- 💾 **Progress Persistence** - Your best scores are automatically saved
- 🎯 **Smart Text Display** - Chunked display prevents scrolling, shows 10 lines at a time
- 🔵 **Clear Visual Feedback** - Blue keyboard highlights and contrasting text colors

## Levels

| Level | Type | Target WPM | Description |
|-------|------|------------|-------------|
| 1 | Business - Beginner | 50 WPM | Professional emails and documents |
| 2 | Business - Advanced | 80 WPM | Fast-paced business communication |
| 3 | Code - Beginner | 20 WPM | Python basics with special characters |
| 4 | Code - Advanced | 50 WPM | Complex Python with type hints and async |
| 5 | Mixed - Master | 40 WPM | Markdown documentation with code blocks |

## Installation

### Prerequisites

- Python 3.9 or higher
- Windows 10 or later (for PyInstaller builds)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/typetutor.git
   cd typetutor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running from Source

**Windows:**
```bash
run.bat
```

**Or manually:**
```bash
venv\Scripts\python src\main.py
```

**macOS/Linux:**
```bash
python src/main.py
```

### Building a Standalone Executable (Windows)

```bash
build.bat
```

The executable will be created at `dist\TypingTutor.exe` and can be distributed as a single file.

## How to Use

1. **Launch the application** - The window will be ready to accept typing immediately
2. **Select a level** - Choose from the dropdown menu (1-5)
3. **Start typing** - Match the displayed text exactly
4. **Watch your progress** - Real-time WPM and accuracy updates
5. **Complete the level** - Achieve target WPM with 95%+ accuracy to pass
6. **Try again** - Each level has 5 random lesson variations

### Keyboard Shortcuts

- **Type normally** - All standard keys work
- **Enter** - For newlines in text
- **Tab** - For indentation in code
- **Reset Level** button - Restart current lesson (gets a new random variation)

## Visual Guide

### Color Coding

- **Blue background, white text** - Completed text you've already typed
- **White background, blue text** - Current character to type
- **Blue keyboard key** - Next key you need to press
- **Beige keyboard keys** - Standard keys (vintage Compaq style)

### Text Display

The practice text shows 10 lines at a time. When you complete 80% of the visible text, it automatically advances to the next chunk. This prevents scrolling issues and keeps you focused.

## Progress Tracking

Your progress is automatically saved to:
```
C:\Users\<YourName>\.typing_tutor\progress.json
```

This includes:
- Best WPM per level
- Best accuracy per level
- Completion status (✓ marks in level selector)

## Project Structure

```
typetutor/
├── src/
│   ├── main.py              # Application entry point
│   ├── typing_session.py    # WPM/accuracy calculation engine
│   ├── level_manager.py     # Level system and random lesson selection
│   ├── keyboard_widget.py   # Custom keyboard visualization
│   └── ui/
│       ├── __init__.py
│       └── main_window.py   # Main application window
├── data/
│   ├── keyboard_layout.json # Keyboard geometry and colors
│   └── levels/              # 25 practice lesson files (5 per level)
│       ├── level1_business_1.txt through level1_business_5.txt
│       ├── level2_business_1.txt through level2_business_5.txt
│       ├── level3_code_1.py through level3_code_5.py
│       ├── level4_code_1.py through level4_code_5.py
│       └── level5_mixed_1.md through level5_mixed_5.md
├── assets/                  # Application assets (icons, etc.)
├── requirements.txt         # Python dependencies
├── typing_tutor.spec       # PyInstaller build configuration
├── build.bat               # Windows build script
├── run.bat                 # Windows run script
└── README.md               # This file
```

## Dependencies

- **PySide6** (6.8.0.2+) - Qt for Python GUI framework
- **PyInstaller** (6.18+) - Executable packaging tool

All dependencies are listed in `requirements.txt`.

## Development

### Running Tests

Currently, testing is manual. Launch the app and verify:
- All 5 levels load with random lessons
- Keyboard highlights the correct key in blue
- Text colors are readable (blue/white completed, white/blue current)
- WPM and accuracy calculate correctly
- Progress saves and persists across sessions

### Adding New Lessons

1. Create a new text file in `data/levels/`
2. Follow the naming convention: `level{N}_{type}_{variation}.{ext}`
3. Update `level_manager.py` LEVELS dictionary to include the new file
4. Test by selecting the level

### Customizing Colors

Edit `data/keyboard_layout.json` to change:
- `base`: Keyboard background color (default: beige #E8E4D9)
- `current`: Highlighted key color (default: blue #2196F3)
- `border`: Key border color (default: gray #8C8676)

## Building for Distribution

### Windows Executable

```bash
# Activate virtual environment
venv\Scripts\activate

# Build single-file executable
pyinstaller typing_tutor.spec

# Executable will be at: dist\TypingTutor.exe
```

### macOS/Linux

PyInstaller works on macOS and Linux too:
```bash
pyinstaller --name="TypeTutor" \
            --windowed \
            --onefile \
            --add-data="data:data" \
            src/main.py
```

## Troubleshooting

### App won't start
- Ensure Python 3.9+ is installed: `python --version`
- Verify virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Keyboard not showing
- Check that `data/keyboard_layout.json` exists
- Verify file permissions allow reading

### Progress not saving
- Ensure write permissions in your user folder
- Check for errors in console output

### Random lesson not working
- Verify all 5 lesson files exist for the level
- Check file naming matches pattern in `level_manager.py`

## Contributing

Contributions are welcome! Feel free to:
- Add new lesson content
- Improve the UI design
- Add new features (sound effects, themes, statistics charts)
- Fix bugs
- Improve documentation

## License

MIT License - Feel free to use, modify, and distribute.

## Credits

- Inspired by vintage Compaq Presario keyboards
- Built with PySide6 (Qt for Python)
- Created as a modern typing practice tool for developers and professionals

## Future Enhancements

Potential features for future versions:
- [ ] Historical WPM charts
- [ ] Multiple color themes
- [ ] Sound effects for keystrokes
- [ ] Export statistics to CSV
- [ ] Custom lesson creation interface
- [ ] Online leaderboards
- [ ] Dark mode
- [ ] More language support

---

**Happy Typing!** 🎯⌨️

For issues or questions, please open an issue on GitHub.
