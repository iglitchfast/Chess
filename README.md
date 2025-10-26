# Chess Game - Enhanced Edition

A feature-rich chess game built with Python and Pygame, featuring an AI opponent with multiple difficulty levels, beautiful themes, and comprehensive gameplay features.

![Chess Game](https://img.shields.io/badge/Python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎮 Features

### Game Modes
- **Player vs AI** - Challenge the computer at 4 difficulty levels
- **Player vs Player** - Play against a friend on the same device
- **Undo/Redo Options** - Enable or disable move takebacks per game

### AI Intelligence
- **Alpha-Beta Pruning Algorithm** - Efficient move search
- **4 Difficulty Levels**: Easy, Medium, Hard, Expert (searches 1-4 moves ahead)
- **Advanced Evaluation Function** with:
  - Material counting
  - Position-square tables
  - King safety analysis
  - Pawn structure evaluation
  - Center control assessment
  - Piece mobility scoring
- **Move Ordering Optimization** for faster searches
- **Transposition Table** for position caching

### Visual Customization
- **6 Beautiful Board Themes**: Classic, Blue, Brown, Green, Purple, Ocean
- **3 Piece Styles**: Classic, Bold, Modern
- **Dark Mode Support** for UI elements
- **Move Highlights**: Selected pieces, valid moves, captures, check warnings
- **Smooth Animations** for piece movements

### Gameplay Features
- **Complete Chess Rules Implementation**:
  - Castling (kingside and queenside)
  - En passant captures
  - Pawn promotion (Queen, Rook, Bishop, Knight)
  - Check and checkmate detection
  - Stalemate detection
- **Timer System** with 4 time controls (3, 5, 10, 15 minutes)
- **Move History Log** with scrolling
- **Sound Effects** for moves, captures, checks, and game events
- **Interactive Guide** - Built-in documentation system

## 📦 Installation

### Prerequisites
- Python 3.x
- Pygame library

### Setup

1. Clone the repository:
```bash
git clone https://github.com/iglitchfast/Chess.git
cd Chess
```

2. Install dependencies:
```bash
pip install pygame
```

3. Run the game:
```bash
python ChessMain.py
```

## 🎯 How to Play

### Starting a Game
1. Launch the game with `python ChessMain.py`
2. Choose your game mode:
   - **Play vs AI** - Play against the computer
   - **Player vs Player** - Play with a friend
3. Select whether to enable undo functionality
4. Start playing!

### Making Moves
- Click on a piece to select it
- Valid moves will be highlighted
- Click on a highlighted square to move
- For pawn promotion, select your desired piece from the menu

### Keyboard Shortcuts
- **ESC** - Quit the game
- **Z** - Undo last move (if enabled)
- **R** - Reset the game

### Settings
Access the settings menu to customize:
- Board theme colors
- Piece visual style
- AI difficulty level
- Game timer settings
- Dark mode toggle
- Interactive guide

## 🏗️ Project Structure

```
Chess/
├── ChessMain.py          # Main game loop and UI
├── ChessEngine.py        # Game logic and move validation
├── ChessAI.py           # AI algorithm implementation
├── ChessExplain.py      # Interactive documentation system
├── images/              # Classic piece set
├── images_bold/         # Bold piece set
├── images_site/         # Modern piece set
├── sounds/              # Game sound effects
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── LICENSE             # MIT License
```

## 🤖 AI Implementation Details

The AI uses a minimax algorithm with alpha-beta pruning to search the game tree efficiently:

### Algorithm Features
- **Alpha-Beta Pruning**: Reduces search space by ~75%
- **Move Ordering**: Examines promising moves first (captures, promotions, castling)
- **Transposition Table**: Caches evaluated positions
- **Iterative Deepening**: Searches to configurable depth (1-4 plies)

### Evaluation Function Components
- **Material Balance** (70% weight): Sum of piece values
- **Position Tables** (10% weight): Rewards pieces on strong squares
- **King Safety** (50% weight): Evaluates king protection
- **Mobility** (5% weight): Number of legal moves
- **Center Control** (30% weight): Occupation of central squares
- **Pawn Structure** (20% weight): Detects doubled/isolated pawns
- **Piece Activity** (10% weight): Rewards developed pieces

## 🎨 Themes

### Available Board Themes
1. **Classic** - Traditional green and cream
2. **Blue** - Cool blue tones
3. **Brown** - Warm wooden appearance
4. **Green** - Forest green variant
5. **Purple** - Royal purple accent
6. **Ocean** - Deep blue sea colors

### Piece Sets
1. **Classic** - Traditional chess piece designs
2. **Bold** - High contrast, thick outlined pieces
3. **Modern** - Contemporary minimalist style

## 🔊 Sound Effects

The game includes audio feedback for:
- Regular moves
- Captures
- Castling
- Check announcements
- Pawn promotions
- Game start/end
- Illegal move attempts

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. Report bugs or suggest features via GitHub Issues
2. Submit pull requests for bug fixes or new features
3. Improve documentation
4. Add new piece sets or board themes
5. Enhance the AI evaluation function

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Add comments for complex algorithms
- Test your changes thoroughly
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Chess piece images from various open-source chess projects
- Sound effects from freesound.org
- Inspired by classic chess engines and modern chess applications

## 📧 Contact

**Developer**: iglitchfast  
**GitHub**: [@iglitchfast](https://github.com/iglitchfast)  
**Repository**: [Chess](https://github.com/iglitchfast/Chess)

## 🚀 Future Enhancements

Potential features for future versions:
- Online multiplayer support
- Opening book integration
- Position analysis mode
- Game save/load functionality
- PGN import/export
- Chess puzzle mode
- ELO rating system
- More AI difficulty levels
- Additional themes and piece sets
- Mobile version

---

**Enjoy the game! ♟️**