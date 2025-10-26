# Chess Game - Interactive Guide

---

## 📚 Overview

### Project Architecture

This chess game is built with three core modules:

**• ChessMain.py - User Interface & Game Loop**
  Handles rendering, user input, animations, themes, and all visual elements using Pygame

**• ChessEngine.py - Game Logic & Rules**
  Manages board state, move validation, special moves (castling, en passant, promotion)

**• ChessAI.py - Artificial Intelligence**
  Implements minimax with alpha-beta pruning, evaluation functions, and move ordering

### Technology Stack

• Python 3.x - Core programming language
• Pygame - Graphics and game framework
• Algorithm: Alpha-Beta Pruning Minimax
• Data Structures: 2D arrays, hash tables
• Design Pattern: Model-View separation

---

## ♟ Chess Pieces

### Pawn (p) - Value: 1

**Movement:** Forward one square (two on first move)
**Capture:** Diagonally forward
**Special:** En passant, Promotion to Q/R/B/N

**Strategic Value:**
• Pawn structure controls space
• Advanced pawns (passed pawns) are powerful
• Doubled/isolated pawns are weaknesses

**AI Considerations:**
• Center pawns worth more (position tables)
• Advanced pawns get bonus evaluation
• Pawn promotion prioritized in move ordering

### Knight (N) - Value: 3.2

**Movement:** L-shape (2+1 squares)
**Unique:** Only piece that can jump over others

**Strategic Value:**
• Most effective in closed positions
• Controls up to 8 squares from center
• Knights on rim are dim (edge penalties)

**AI Evaluation:**
• Strong central knights (+1.5 to +2 bonus)
• Edge/corner knights penalized (-5 to -3)
• Rewarded for development (not on back rank)

### Bishop (B) - Value: 3.3

**Movement:** Any number of squares diagonally
**Constraint:** Stays on same color squares

**Strategic Value:**
• Powerful in open positions
• Bishop pair is strong (controls all squares)
• Long diagonal bishops are dangerous

**AI Evaluation:**
• Central positions highly valued (+1 bonus)
• Diagonal control rewarded
• Slightly more valuable than knight

### Rook (R) - Value: 5

**Movement:** Any number of squares horizontally/vertically
**Special:** Participates in castling

**Strategic Value:**
• Dominates open files and ranks
• Connected rooks (7th rank) are powerful
• Best in endgame positions

**AI Evaluation:**
• Prefers 7th/2nd ranks (+0.5 to +1)
• Open file control rewarded
• Castling rights affect king safety score

### Queen (Q) - Value: 9

**Movement:** Combines Rook + Bishop
**Most powerful piece on the board**

**Strategic Value:**
• Can control up to 27 squares
• Early queen moves often risky
• Devastating in open positions

**AI Evaluation:**
• Central position slightly preferred
• Heavy penalty if lost (9 points)
• Queen trades only when ahead

### King (K) - Value: ∞

**Movement:** One square in any direction
**Special:** Castling (kingside/queenside)
**Objective:** Protect at all costs!

**Strategic Value:**
• Middlegame: Stay safe, castle early
• Endgame: Become active, centralize

**AI Evaluation:**
• Middlegame: Prefers back rank safety
• Endgame: Central king (+4 bonus)
• King safety function counts shield pieces
• Exposed king heavily penalized

---

## 🤖 AI Algorithm

### Minimax with Alpha-Beta Pruning

**Core Concept:**
The AI searches through possible future positions to find the best move. It assumes both players play optimally.

**How it works:**
1. Generate all possible moves
2. For each move, simulate opponent's responses
3. Evaluate positions at search depth
4. Choose move leading to best evaluation

**Alpha-Beta Pruning:**
Optimization that skips branches that can't affect the final decision, reducing computation by up to 75%!

**Depth Levels:**
• Easy (1): Looks 1 move ahead
• Medium (2): Looks 2 moves ahead (1 full turn)
• Hard (3): Looks 3 moves ahead
• Expert (4): Looks 4 moves ahead (2 full turns)

### Evaluation Function

The AI scores positions using multiple factors:

**Material (70% weight):**
  Sum of piece values on board

**Position Tables (10% weight):**
  Rewards pieces on strong squares
  Example: Central knights > edge knights

**King Safety (50% weight):**
  Counts friendly pieces near king
  Penalties for exposed king

**Mobility (5% weight):**
  Number of legal moves available
  More moves = more options

**Center Control (30% weight):**
  Occupying central squares (d4,e4,d5,e5)

**Pawn Structure (20% weight):**
  Penalties: doubled, isolated pawns
  Bonuses: passed pawns

**Piece Activity (10% weight):**
  Developed pieces, advanced pawns

### Move Ordering Optimization

The AI examines promising moves first to enable better pruning. Move priority:

1. **Captures** (especially valuable pieces)
   Score: 10 × (captured) - (attacker)

2. **Pawn Promotions**
   Score: +8

3. **Castling**
   Score: +2

4. **Center Control**
   Score: +0.5

This ordering can reduce search time by 3-5x!

### Transposition Table

A hash table that remembers evaluated positions to avoid recalculating them.

**How it works:**
• Each board position gets a unique hash
• Hash = board state + whose turn
• Stores: position score + search depth
• Retrieves score if depth >= current depth

**Benefits:**
• Speeds up searches by ~40%
• Handles transpositions (same position reached via different move orders)
• Memory efficient (clears each search)

---

## ⚙️ Game Features

### Move Validation System

The engine ensures all moves are legal:

**1. Generate Pseudo-Legal Moves**
   • Based on piece movement rules
   • Includes captures, special moves

**2. Filter Illegal Moves**
   • Simulate each move
   • Check if king is in check
   • Remove if king becomes attacked

**3. Special Move Detection**
   • Castling: King/rook unmoved, path clear
   • En Passant: Pawn moved 2 squares last turn
   • Promotion: Pawn reaches opposite end

**4. Game End Conditions**
   • Checkmate: No legal moves, king in check
   • Stalemate: No legal moves, king safe
   • Timer: Time runs out (if enabled)

### Visual System

**UI Components:**

**Board Rendering:**
  • 6 color themes (Classic, Blue, Brown, etc.)
  • 3 piece styles (Classic, Bold, Modern)
  • Coordinate labels (a-h, 1-8)

**Move Highlights:**
  • Selected piece (blue highlight)
  • Last move (yellow highlight)
  • Check warning (red overlay + border)
  • Valid moves (gray circles)
  • Capture moves (red circles)

**Animations:**
  • Smooth piece sliding (3 frames/square)
  • Promotion menu with piece images
  • Gradient backgrounds
  • Button hover effects

**Side Panel:**
  • Turn indicator with icons
  • Move history log (scrolling)
  • Game timer (if enabled)
  • Control buttons (Home/Undo/Reset)

### Sound System

Audio feedback for different game events:

• move-normal.mp3 - Regular piece moves
• capture.mp3 - Capturing opponent pieces
• castle.mp3 - Castling king-side or queen-side
• move-check.mp3 - Putting opponent in check
• promote.mp3 - Pawn promotion
• game-start.mp3 - Starting new game
• game-end.mp3 - Checkmate or stalemate
• illegal.mp3 - Attempting invalid move

Sounds enhance user experience and provide immediate feedback for actions.

### Settings & Customization

**Board Themes:** 6 color schemes
  Classic, Blue, Brown, Green, Purple, Ocean

**Piece Sets:** 3 visual styles
  Classic, Bold, Modern

**AI Difficulty:** 4 levels
  Easy (1), Medium (2), Hard (3), Expert (4)
  Higher = deeper search, stronger play

**Timer Options:** 4 time controls
  3min, 5min, 10min, 15min
  Can toggle timer on/off

**Dark Mode:** Toggle UI appearance
  Light theme or dark theme

**Undo Settings:** Per-game choice
  Enable/disable before starting
  Prevents accidental undos in serious play

---

## 💻 Code Structure

### ChessMain.py - UI Layer

**Key Functions:**

**main()**
  Game loop and state management
  Handles menu/settings/game states

**drawGameState()**
  Renders board, pieces, highlights

**highlightSquares()**
  Shows legal moves, check warnings
  Last move highlighting

**animateMove()**
  Smooth piece movement animation

**drawMenu() / drawSettingsMain()**
  Menu systems with button interactions

**drawMoveLog()**
  Scrolling move history display

**drawTimer()**
  Real-time clock countdown

**Data Structures:**
  • IMAGES{} - Loaded piece sprites
  • THEMES{} - Color scheme definitions
  • DARK_MODE{} - UI color palette

### ChessEngine.py - Game Logic

**Classes:**

**GameState**
  • board[8][8] - 2D array of pieces
  • moveLog[] - History of moves
  • whiteToMove - Turn tracker
  • King locations, castling rights

  **Methods:**
  • makeMove() - Execute move on board
  • undoMove() - Reverse last move
  • getValidMoves() - Legal moves only
  • getAllPossibleMoves() - All piece moves
  • inCheck() - King under attack?
  • getPawnMoves(), getRookMoves(), etc.

**Move**
  • Start/end coordinates
  • Piece moved/captured
  • Special flags (promotion, castle, etc.)
  • moveID for equality checking

**CastleRights**
  • Tracks white/black king/queen side rights

### ChessAI.py - Intelligence

**Key Functions:**

**findBestMove(gs, validMoves)**
  Entry point, returns best move
  Clears transposition table

**alphaBeta(gs, depth, alpha, beta, turn)**
  Recursive minimax with pruning
  Returns position evaluation score

**evaluateBoard(gs)**
  Master evaluation function
  Combines all scoring factors

**orderMoves(gs, moves)**
  Sorts moves for better pruning

**kingSafety(gs)**
  Evaluates king protection

**mobility(gs)**
  Counts available moves

**centerControl(gs)**
  Scores center square occupation

**pawnStructure(gs)**
  Analyzes pawn formation quality

**pieceActivity(gs)**
  Rewards developed pieces

**Data:**
  • pieceScore{} - Material values
  • pst{} - Position-square tables
  • transpositionTable{} - Memoization

### Performance Optimizations

**1. Transposition Table**
   Caches evaluated positions
   Avoids redundant calculations

**2. Move Ordering**
   Examines best moves first
   Enables earlier alpha-beta cutoffs

**3. Alpha-Beta Pruning**
   Skips unpromising branches
   Reduces nodes by ~75%

**4. Incremental Updates**
   makeMove/undoMove are O(1)
   No board copying

**5. Move Validation Caching**
   getValidMoves() only on move made
   Stores result until next move

**6. Early Termination**
   Returns immediately on checkmate
   Doesn't search further

**Result:** Expert AI responds in < 3 seconds!

---

## 🎯 Tips & Strategy

### Opening Principles

**1. Control the Center**
   Move e4, d4, Nf3, Nc3 early
   Center pawns and pieces are powerful

**2. Develop Pieces Quickly**
   Get knights and bishops out
   Don't move the same piece twice

**3. Castle Early**
   Protects your king
   Connects your rooks

**4. Don't Bring Queen Out Too Early**
   Enemy pieces can attack it
   You'll waste time retreating

**5. Connect Your Rooks**
   Clear pieces between them
   They support each other

### Tactical Patterns

**Fork:**
  One piece attacks two+ enemy pieces
  Knights are excellent forkers

**Pin:**
  Attack piece that shields valuable piece
  Pinned piece can't/shouldn't move

**Skewer:**
  Attack valuable piece, revealing another
  Opposite of pin (valuable piece in front)

**Discovered Attack:**
  Moving one piece reveals another's attack
  Very powerful if unexpected

**Double Check:**
  Two pieces give check simultaneously
  King MUST move (can't block/capture)

**Back Rank Mate:**
  Checkmate on 8th/1st rank
  King trapped by own pawns

### Beating the AI

**On Easy/Medium:**
  • Control center aggressively
  • Develop pieces fast
  • Look for tactical shots (forks, pins)

**On Hard:**
  • Play solid, avoid blunders
  • Build strong pawn structure
  • Calculate trades carefully
  • Look 3-4 moves ahead

**On Expert:**
  • Study opening theory
  • Avoid weaknesses in position
  • Create long-term plans
  • Endgame knowledge crucial
  • AI struggles with:
    - Long-term strategic plans
    - Sacrifices for initiative
    - Complex endgames

**General Tips:**
  • Take your time, don't rush
  • Check every move for tactics
  • Use the undo feature to learn!
  • Practice endgames (K+P vs K, etc.)

---

**End of Guide**