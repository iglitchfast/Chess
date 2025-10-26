import pygame as p


WIDTH = 920
HEIGHT = 640
CARD_WIDTH = 380
CARD_PADDING = 20


DARK_MODE = {
    "enabled": True,
    "colors": {
        "bg_primary": (30, 30, 30),
        "bg_secondary": (37, 37, 37),
        "text_primary": (230, 230, 230),
        "text_secondary": (189, 189, 189),
        "accent": (78, 160, 237),
        "accent_hover": (100, 180, 255),
        "border": (51, 51, 51),
        "button_bg": (50, 50, 50),
        "button_hover": (60, 60, 60),
        "success": (89, 186, 124),
        "danger": (244, 71, 71),
        "warning": (214, 112, 214),
        "code_bg": (45, 45, 45),
        "card_bg": (42, 42, 46),
    }
}


CONTENT = {
    "Overview": {
        "icon": "📚",
        "sections": [
            {
                "title": "Project Architecture",
                "content": [
                    "This chess game is built with three core modules:",
                    "",
                    "• ChessMain.py - User Interface & Game Loop",
                    "  Handles rendering, user input, animations, themes,",
                    "  and all visual elements using Pygame",
                    "",
                    "• ChessEngine.py - Game Logic & Rules",
                    "  Manages board state, move validation, special",
                    "  moves (castling, en passant, promotion)",
                    "",
                    "• ChessAI.py - Artificial Intelligence",
                    "  Implements minimax with alpha-beta pruning,",
                    "  evaluation functions, and move ordering"
                ]
            },
            {
                "title": "Technology Stack",
                "content": [
                    "• Python 3.x - Core programming language",
                    "• Pygame - Graphics and game framework",
                    "• Algorithm: Alpha-Beta Pruning Minimax",
                    "• Data Structures: 2D arrays, hash tables",
                    "• Design Pattern: Model-View separation"
                ]
            }
        ]
    },
    "Chess Pieces": {
        "icon": "♟",
        "sections": [
            {
                "title": "Pawn (p) - Value: 1",
                "content": [
                    "Movement: Forward one square (two on first move)",
                    "Capture: Diagonally forward",
                    "Special: En passant, Promotion to Q/R/B/N",
                    "",
                    "Strategic Value:",
                    "• Pawn structure controls space",
                    "• Advanced pawns (passed pawns) are powerful",
                    "• Doubled/isolated pawns are weaknesses",
                    "",
                    "AI Considerations:",
                    "• Center pawns worth more (position tables)",
                    "• Advanced pawns get bonus evaluation",
                    "• Pawn promotion prioritized in move ordering"
                ]
            },
            {
                "title": "Knight (N) - Value: 3.2",
                "content": [
                    "Movement: L-shape (2+1 squares)",
                    "Unique: Only piece that can jump over others",
                    "",
                    "Strategic Value:",
                    "• Most effective in closed positions",
                    "• Controls up to 8 squares from center",
                    "• Knights on rim are dim (edge penalties)",
                    "",
                    "AI Evaluation:",
                    "• Strong central knights (+1.5 to +2 bonus)",
                    "• Edge/corner knights penalized (-5 to -3)",
                    "• Rewarded for development (not on back rank)"
                ]
            },
            {
                "title": "Bishop (B) - Value: 3.3",
                "content": [
                    "Movement: Any number of squares diagonally",
                    "Constraint: Stays on same color squares",
                    "",
                    "Strategic Value:",
                    "• Powerful in open positions",
                    "• Bishop pair is strong (controls all squares)",
                    "• Long diagonal bishops are dangerous",
                    "",
                    "AI Evaluation:",
                    "• Central positions highly valued (+1 bonus)",
                    "• Diagonal control rewarded",
                    "• Slightly more valuable than knight"
                ]
            },
            {
                "title": "Rook (R) - Value: 5",
                "content": [
                    "Movement: Any number of squares horizontally/vertically",
                    "Special: Participates in castling",
                    "",
                    "Strategic Value:",
                    "• Dominates open files and ranks",
                    "• Connected rooks (7th rank) are powerful",
                    "• Best in endgame positions",
                    "",
                    "AI Evaluation:",
                    "• Prefers 7th/2nd ranks (+0.5 to +1)",
                    "• Open file control rewarded",
                    "• Castling rights affect king safety score"
                ]
            },
            {
                "title": "Queen (Q) - Value: 9",
                "content": [
                    "Movement: Combines Rook + Bishop",
                    "Most powerful piece on the board",
                    "",
                    "Strategic Value:",
                    "• Can control up to 27 squares",
                    "• Early queen moves often risky",
                    "• Devastating in open positions",
                    "",
                    "AI Evaluation:",
                    "• Central position slightly preferred",
                    "• Heavy penalty if lost (9 points)",
                    "• Queen trades only when ahead"
                ]
            },
            {
                "title": "King (K) - Value: ∞",
                "content": [
                    "Movement: One square in any direction",
                    "Special: Castling (kingside/queenside)",
                    "Objective: Protect at all costs!",
                    "",
                    "Strategic Value:",
                    "• Middlegame: Stay safe, castle early",
                    "• Endgame: Become active, centralize",
                    "",
                    "AI Evaluation:",
                    "• Middlegame: Prefers back rank safety",
                    "• Endgame: Central king (+4 bonus)",
                    "• King safety function counts shield pieces",
                    "• Exposed king heavily penalized"
                ]
            }
        ]
    },
    "AI Algorithm": {
        "icon": "🤖",
        "sections": [
            {
                "title": "Minimax with Alpha-Beta Pruning",
                "content": [
                    "Core Concept:",
                    "The AI searches through possible future positions",
                    "to find the best move. It assumes both players",
                    "play optimally.",
                    "",
                    "How it works:",
                    "1. Generate all possible moves",
                    "2. For each move, simulate opponent's responses",
                    "3. Evaluate positions at search depth",
                    "4. Choose move leading to best evaluation",
                    "",
                    "Alpha-Beta Pruning:",
                    "Optimization that skips branches that can't",
                    "affect the final decision, reducing computation",
                    "by up to 75%!",
                    "",
                    "Depth Levels:",
                    "• Easy (1): Looks 1 move ahead",
                    "• Medium (2): Looks 2 moves ahead (1 full turn)",
                    "• Hard (3): Looks 3 moves ahead",
                    "• Expert (4): Looks 4 moves ahead (2 full turns)"
                ]
            },
            {
                "title": "Evaluation Function",
                "content": [
                    "The AI scores positions using multiple factors:",
                    "",
                    "Material (70% weight):",
                    "  Sum of piece values on board",
                    "",
                    "Position Tables (10% weight):",
                    "  Rewards pieces on strong squares",
                    "  Example: Central knights > edge knights",
                    "",
                    "King Safety (50% weight):",
                    "  Counts friendly pieces near king",
                    "  Penalties for exposed king",
                    "",
                    "Mobility (5% weight):",
                    "  Number of legal moves available",
                    "  More moves = more options",
                    "",
                    "Center Control (30% weight):",
                    "  Occupying central squares (d4,e4,d5,e5)",
                    "",
                    "Pawn Structure (20% weight):",
                    "  Penalties: doubled, isolated pawns",
                    "  Bonuses: passed pawns",
                    "",
                    "Piece Activity (10% weight):",
                    "  Developed pieces, advanced pawns"
                ]
            },
            {
                "title": "Move Ordering Optimization",
                "content": [
                    "The AI examines promising moves first to enable",
                    "better pruning. Move priority:",
                    "",
                    "1. Captures (especially valuable pieces)",
                    "   Score: 10 × (captured) - (attacker)",
                    "",
                    "2. Pawn Promotions",
                    "   Score: +8",
                    "",
                    "3. Castling",
                    "   Score: +2",
                    "",
                    "4. Center Control",
                    "   Score: +0.5",
                    "",
                    "This ordering can reduce search time by 3-5x!"
                ]
            },
            {
                "title": "Transposition Table",
                "content": [
                    "A hash table that remembers evaluated positions",
                    "to avoid recalculating them.",
                    "",
                    "How it works:",
                    "• Each board position gets a unique hash",
                    "• Hash = board state + whose turn",
                    "• Stores: position score + search depth",
                    "• Retrieves score if depth >= current depth",
                    "",
                    "Benefits:",
                    "• Speeds up searches by ~40%",
                    "• Handles transpositions (same position",
                    "  reached via different move orders)",
                    "• Memory efficient (clears each search)"
                ]
            }
        ]
    },
    "Game Features": {
        "icon": "⚙️",
        "sections": [
            {
                "title": "Move Validation System",
                "content": [
                    "The engine ensures all moves are legal:",
                    "",
                    "1. Generate Pseudo-Legal Moves",
                    "   • Based on piece movement rules",
                    "   • Includes captures, special moves",
                    "",
                    "2. Filter Illegal Moves",
                    "   • Simulate each move",
                    "   • Check if king is in check",
                    "   • Remove if king becomes attacked",
                    "",
                    "3. Special Move Detection",
                    "   • Castling: King/rook unmoved, path clear",
                    "   • En Passant: Pawn moved 2 squares last turn",
                    "   • Promotion: Pawn reaches opposite end",
                    "",
                    "4. Game End Conditions",
                    "   • Checkmate: No legal moves, king in check",
                    "   • Stalemate: No legal moves, king safe",
                    "   • Timer: Time runs out (if enabled)"
                ]
            },
            {
                "title": "Visual System",
                "content": [
                    "UI Components:",
                    "",
                    "Board Rendering:",
                    "  • 6 color themes (Classic, Blue, Brown, etc.)",
                    "  • 3 piece styles (Classic, Bold, Modern)",
                    "  • Coordinate labels (a-h, 1-8)",
                    "",
                    "Move Highlights:",
                    "  • Selected piece (blue highlight)",
                    "  • Last move (yellow highlight)",
                    "  • Check warning (red overlay + border)",
                    "  • Valid moves (gray circles)",
                    "  • Capture moves (red circles)",
                    "",
                    "Animations:",
                    "  • Smooth piece sliding (3 frames/square)",
                    "  • Promotion menu with piece images",
                    "  • Gradient backgrounds",
                    "  • Button hover effects",
                    "",
                    "Side Panel:",
                    "  • Turn indicator with icons",
                    "  • Move history log (scrolling)",
                    "  • Game timer (if enabled)",
                    "  • Control buttons (Home/Undo/Reset)"
                ]
            },
            {
                "title": "Sound System",
                "content": [
                    "Audio feedback for different game events:",
                    "",
                    "• move-normal.mp3 - Regular piece moves",
                    "• capture.mp3 - Capturing opponent pieces",
                    "• castle.mp3 - Castling king-side or queen-side",
                    "• move-check.mp3 - Putting opponent in check",
                    "• promote.mp3 - Pawn promotion",
                    "• game-start.mp3 - Starting new game",
                    "• game-end.mp3 - Checkmate or stalemate",
                    "• illegal.mp3 - Attempting invalid move",
                    "",
                    "Sounds enhance user experience and provide",
                    "immediate feedback for actions."
                ]
            },
            {
                "title": "Settings & Customization",
                "content": [
                    "Board Themes: 6 color schemes",
                    "  Classic, Blue, Brown, Green, Purple, Ocean",
                    "",
                    "Piece Sets: 3 visual styles",
                    "  Classic, Bold, Modern",
                    "",
                    "AI Difficulty: 4 levels",
                    "  Easy (1), Medium (2), Hard (3), Expert (4)",
                    "  Higher = deeper search, stronger play",
                    "",
                    "Timer Options: 4 time controls",
                    "  3min, 5min, 10min, 15min",
                    "  Can toggle timer on/off",
                    "",
                    "Dark Mode: Toggle UI appearance",
                    "  Light theme or dark theme",
                    "",
                    "Undo Settings: Per-game choice",
                    "  Enable/disable before starting",
                    "  Prevents accidental undos in serious play"
                ]
            }
        ]
    },
    "Code Structure": {
        "icon": "💻",
        "sections": [
            {
                "title": "ChessMain.py - UI Layer",
                "content": [
                    "Key Functions:",
                    "",
                    "main()",
                    "  Game loop and state management",
                    "  Handles menu/settings/game states",
                    "",
                    "drawGameState()",
                    "  Renders board, pieces, highlights",
                    "",
                    "highlightSquares()",
                    "  Shows legal moves, check warnings",
                    "  Last move highlighting",
                    "",
                    "animateMove()",
                    "  Smooth piece movement animation",
                    "",
                    "drawMenu() / drawSettingsMain()",
                    "  Menu systems with button interactions",
                    "",
                    "drawMoveLog()",
                    "  Scrolling move history display",
                    "",
                    "drawTimer()",
                    "  Real-time clock countdown",
                    "",
                    "Data Structures:",
                    "  • IMAGES{} - Loaded piece sprites",
                    "  • THEMES{} - Color scheme definitions",
                    "  • DARK_MODE{} - UI color palette"
                ]
            },
            {
                "title": "ChessEngine.py - Game Logic",
                "content": [
                    "Classes:",
                    "",
                    "GameState",
                    "  • board[8][8] - 2D array of pieces",
                    "  • moveLog[] - History of moves",
                    "  • whiteToMove - Turn tracker",
                    "  • King locations, castling rights",
                    "",
                    "  Methods:",
                    "  • makeMove() - Execute move on board",
                    "  • undoMove() - Reverse last move",
                    "  • getValidMoves() - Legal moves only",
                    "  • getAllPossibleMoves() - All piece moves",
                    "  • inCheck() - King under attack?",
                    "  • getPawnMoves(), getRookMoves(), etc.",
                    "",
                    "Move",
                    "  • Start/end coordinates",
                    "  • Piece moved/captured",
                    "  • Special flags (promotion, castle, etc.)",
                    "  • moveID for equality checking",
                    "",
                    "CastleRights",
                    "  • Tracks white/black king/queen side rights"
                ]
            },
            {
                "title": "ChessAI.py - Intelligence",
                "content": [
                    "Key Functions:",
                    "",
                    "findBestMove(gs, validMoves)",
                    "  Entry point, returns best move",
                    "  Clears transposition table",
                    "",
                    "alphaBeta(gs, depth, alpha, beta, turn)",
                    "  Recursive minimax with pruning",
                    "  Returns position evaluation score",
                    "",
                    "evaluateBoard(gs)",
                    "  Master evaluation function",
                    "  Combines all scoring factors",
                    "",
                    "orderMoves(gs, moves)",
                    "  Sorts moves for better pruning",
                    "",
                    "kingSafety(gs)",
                    "  Evaluates king protection",
                    "",
                    "mobility(gs)",
                    "  Counts available moves",
                    "",
                    "centerControl(gs)",
                    "  Scores center square occupation",
                    "",
                    "pawnStructure(gs)",
                    "  Analyzes pawn formation quality",
                    "",
                    "pieceActivity(gs)",
                    "  Rewards developed pieces",
                    "",
                    "Data:",
                    "  • pieceScore{} - Material values",
                    "  • pst{} - Position-square tables",
                    "  • transpositionTable{} - Memoization"
                ]
            },
            {
                "title": "Performance Optimizations",
                "content": [
                    "1. Transposition Table",
                    "   Caches evaluated positions",
                    "   Avoids redundant calculations",
                    "",
                    "2. Move Ordering",
                    "   Examines best moves first",
                    "   Enables earlier alpha-beta cutoffs",
                    "",
                    "3. Alpha-Beta Pruning",
                    "   Skips unpromising branches",
                    "   Reduces nodes by ~75%",
                    "",
                    "4. Incremental Updates",
                    "   makeMove/undoMove are O(1)",
                    "   No board copying",
                    "",
                    "5. Move Validation Caching",
                    "   getValidMoves() only on move made",
                    "   Stores result until next move",
                    "",
                    "6. Early Termination",
                    "   Returns immediately on checkmate",
                    "   Doesn't search further",
                    "",
                    "Result: Expert AI responds in < 3 seconds!"
                ]
            }
        ]
    },
    "Tips & Strategy": {
        "icon": "🎯",
        "sections": [
            {
                "title": "Opening Principles",
                "content": [
                    "1. Control the Center",
                    "   Move e4, d4, Nf3, Nc3 early",
                    "   Center pawns and pieces are powerful",
                    "",
                    "2. Develop Pieces Quickly",
                    "   Get knights and bishops out",
                    "   Don't move the same piece twice",
                    "",
                    "3. Castle Early",
                    "   Protects your king",
                    "   Connects your rooks",
                    "",
                    "4. Don't Bring Queen Out Too Early",
                    "   Enemy pieces can attack it",
                    "   You'll waste time retreating",
                    "",
                    "5. Connect Your Rooks",
                    "   Clear pieces between them",
                    "   They support each other"
                ]
            },
            {
                "title": "Tactical Patterns",
                "content": [
                    "Fork:",
                    "  One piece attacks two+ enemy pieces",
                    "  Knights are excellent forkers",
                    "",
                    "Pin:",
                    "  Attack piece that shields valuable piece",
                    "  Pinned piece can't/shouldn't move",
                    "",
                    "Skewer:",
                    "  Attack valuable piece, revealing another",
                    "  Opposite of pin (valuable piece in front)",
                    "",
                    "Discovered Attack:",
                    "  Moving one piece reveals another's attack",
                    "  Very powerful if unexpected",
                    "",
                    "Double Check:",
                    "  Two pieces give check simultaneously",
                    "  King MUST move (can't block/capture)",
                    "",
                    "Back Rank Mate:",
                    "  Checkmate on 8th/1st rank",
                    "  King trapped by own pawns"
                ]
            },
            {
                "title": "Beating the AI",
                "content": [
                    "On Easy/Medium:",
                    "  • Control center aggressively",
                    "  • Develop pieces fast",
                    "  • Look for tactical shots (forks, pins)",
                    "",
                    "On Hard:",
                    "  • Play solid, avoid blunders",
                    "  • Build strong pawn structure",
                    "  • Calculate trades carefully",
                    "  • Look 3-4 moves ahead",
                    "",
                    "On Expert:",
                    "  • Study opening theory",
                    "  • Avoid weaknesses in position",
                    "  • Create long-term plans",
                    "  • Endgame knowledge crucial",
                    "  • AI struggles with:",
                    "    - Long-term strategic plans",
                    "    - Sacrifices for initiative",
                    "    - Complex endgames",
                    "",
                    "General Tips:",
                    "  • Take your time, don't rush",
                    "  • Check every move for tactics",
                    "  • Use the undo feature to learn!",
                    "  • Practice endgames (K+P vs K, etc.)"
                ]
            }
        ]
    }
}

class ExplainSystem:
    def __init__(self):
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        p.display.set_caption("Chess Game - Interactive Guide")
        self.clock = p.time.Clock()
        
        self.titleFont = p.font.SysFont("Arial", 32, True)
        self.headerFont = p.font.SysFont("Arial", 20, True)
        self.textFont = p.font.SysFont("Arial", 14)
        self.codeFont = p.font.SysFont("Courier New", 13)
        
        self.categories = list(CONTENT.keys())
        self.selectedCategory = 0
        self.scrollOffset = 0
        self.maxScroll = 0
        
    def drawGradientBg(self):
        """Draw gradient background"""
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(DARK_MODE["colors"]["bg_primary"][0] * (1 - ratio) + 
                   DARK_MODE["colors"]["bg_secondary"][0] * ratio)
            g = int(DARK_MODE["colors"]["bg_primary"][1] * (1 - ratio) + 
                   DARK_MODE["colors"]["bg_secondary"][1] * ratio)
            b = int(DARK_MODE["colors"]["bg_primary"][2] * (1 - ratio) + 
                   DARK_MODE["colors"]["bg_secondary"][2] * ratio)
            p.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
    
    def drawSidebar(self):
        """Draw category sidebar"""
        sidebarWidth = 200
        sidebarRect = p.Rect(0, 0, sidebarWidth, HEIGHT)
        
        
        p.draw.rect(self.screen, DARK_MODE["colors"]["card_bg"], sidebarRect)
        p.draw.line(self.screen, DARK_MODE["colors"]["border"], 
                   (sidebarWidth, 0), (sidebarWidth, HEIGHT), 2)
        
        
        title = self.titleFont.render("Guide", True, DARK_MODE["colors"]["text_primary"])
        self.screen.blit(title, (sidebarWidth//2 - title.get_width()//2, 20))
        
        
        y = 80
        mousePos = p.mouse.get_pos()
        
        for i, category in enumerate(self.categories):
            rect = p.Rect(10, y, sidebarWidth - 20, 50)
            
            isSelected = i == self.selectedCategory
            isHover = rect.collidepoint(mousePos) and not isSelected
            
            if isSelected:
                color = DARK_MODE["colors"]["accent"]
            elif isHover:
                color = DARK_MODE["colors"]["button_hover"]
            else:
                color = DARK_MODE["colors"]["button_bg"]
            
            p.draw.rect(self.screen, color, rect, border_radius=8)
            p.draw.rect(self.screen, DARK_MODE["colors"]["border"], rect, 2, border_radius=8)
            
            
            icon = CONTENT[category]["icon"]
            iconText = self.headerFont.render(icon, True, DARK_MODE["colors"]["text_primary"])
            self.screen.blit(iconText, (rect.x + 10, rect.y + 12))
            
            categoryText = self.textFont.render(category, True, DARK_MODE["colors"]["text_primary"])
            self.screen.blit(categoryText, (rect.x + 45, rect.y + 17))
            
            y += 60
        
        return sidebarWidth
    
    def drawContent(self, sidebarWidth):
        """Draw main content area with cards"""
        contentX = sidebarWidth + 30
        contentWidth = WIDTH - sidebarWidth - 60
        
        category = self.categories[self.selectedCategory]
        sections = CONTENT[category]["sections"]
        
        
        totalHeight = 0
        for section in sections:
            totalHeight += self.calculateSectionHeight(section, contentWidth) + 30
        
        self.maxScroll = max(0, totalHeight - (HEIGHT - 100))
        
        
        clipRect = p.Rect(contentX, 60, contentWidth, HEIGHT - 80)
        self.screen.set_clip(clipRect)
        
        
        y = 70 - self.scrollOffset
        
        for section in sections:
            y = self.drawSection(section, contentX, y, contentWidth)
            y += 30
        
        self.screen.set_clip(None)
        
        
        if self.maxScroll > 0:
            self.drawScrollbar(contentX + contentWidth + 10, 60, HEIGHT - 80)
    
    def calculateSectionHeight(self, section, width):
        """Calculate height needed for a section"""
        height = 50  # Header
        
        lineHeight = 20
        maxLineWidth = width - 60
        
        for line in section["content"]:
            if line.startswith("•") or line.startswith("  "):
                
                wrappedLines = self.wrapText(line, self.textFont, maxLineWidth - 20)
            else:
                wrappedLines = self.wrapText(line, self.textFont, maxLineWidth)
            
            height += len(wrappedLines) * lineHeight
        
        return height + 40
    
    def drawSection(self, section, x, y, width):
        """Draw a content section card"""
        cardHeight = self.calculateSectionHeight(section, width)
        
        
        cardRect = p.Rect(x, y, width, cardHeight)
        p.draw.rect(self.screen, DARK_MODE["colors"]["card_bg"], cardRect, border_radius=12)
        p.draw.rect(self.screen, DARK_MODE["colors"]["border"], cardRect, 2, border_radius=12)
        
        
        titleText = self.headerFont.render(section["title"], True, DARK_MODE["colors"]["accent"])
        self.screen.blit(titleText, (x + 20, y + 15))
        
        
        contentY = y + 50
        lineHeight = 20
        
        for line in section["content"]:
            if not line:
                contentY += lineHeight // 2
                continue
            
            indent = 0
            font = self.textFont
            color = DARK_MODE["colors"]["text_primary"]
            
            
            if any(keyword in line for keyword in ["def ", "class ", "import ", "return ", "()", "[]", "{}"]):
                font = self.codeFont
                color = DARK_MODE["colors"]["success"]
            
            
            if line.startswith("  "):
                indent = 40
                line = line.strip()
            elif line.startswith("•"):
                indent = 20
            
            
            maxLineWidth = width - 60 - indent
            wrappedLines = self.wrapText(line, font, maxLineWidth)
            
            for wrappedLine in wrappedLines:
                text = font.render(wrappedLine, True, color)
                self.screen.blit(text, (x + 30 + indent, contentY))
                contentY += lineHeight
        
        return contentY + 20
    
    def wrapText(self, text, font, maxWidth):
        """Word wrap text to fit width"""
        words = text.split(' ')
        lines = []
        currentLine = []
        
        for word in words:
            testLine = ' '.join(currentLine + [word])
            if font.size(testLine)[0] <= maxWidth:
                currentLine.append(word)
            else:
                if currentLine:
                    lines.append(' '.join(currentLine))
                currentLine = [word]
        
        if currentLine:
            lines.append(' '.join(currentLine))
        
        return lines if lines else [text]
    
    def drawScrollbar(self, x, y, height):
        """Draw scrollbar indicator"""
        if self.maxScroll == 0:
            return
        
        
        trackRect = p.Rect(x, y, 8, height)
        p.draw.rect(self.screen, DARK_MODE["colors"]["button_bg"], trackRect, border_radius=4)
        
        
        thumbHeight = max(30, height * (height / (height + self.maxScroll)))
        thumbY = y + (self.scrollOffset / self.maxScroll) * (height - thumbHeight)
        thumbRect = p.Rect(x, thumbY, 8, thumbHeight)
        p.draw.rect(self.screen, DARK_MODE["colors"]["accent"], thumbRect, border_radius=4)
    
    def handleClick(self, pos, sidebarWidth):
        """Handle mouse clicks"""
        
        if pos[0] < sidebarWidth:
            y = 80
            for i in range(len(self.categories)):
                rect = p.Rect(10, y, sidebarWidth - 20, 50)
                if rect.collidepoint(pos):
                    self.selectedCategory = i
                    self.scrollOffset = 0
                    return True
                y += 60
        
        return False
    
    def handleScroll(self, amount):
        """Handle mouse wheel scrolling"""
        self.scrollOffset = max(0, min(self.maxScroll, self.scrollOffset - amount * 30))
    
    def run(self):
        """Main loop for the explain system"""
        running = True
        
        while running:
            self.drawGradientBg()
            sidebarWidth = self.drawSidebar()
            self.drawContent(sidebarWidth)
            
           
            backRect = p.Rect(WIDTH - 120, 20, 100, 40)
            mousePos = p.mouse.get_pos()
            isHover = backRect.collidepoint(mousePos)
            
            color = DARK_MODE["colors"]["danger"] if isHover else DARK_MODE["colors"]["button_bg"]
            p.draw.rect(self.screen, color, backRect, border_radius=8)
            p.draw.rect(self.screen, DARK_MODE["colors"]["border"], backRect, 2, border_radius=8)
            
            backText = self.textFont.render("< Back", True, DARK_MODE["colors"]["text_primary"])
            self.screen.blit(backText, (backRect.centerx - backText.get_width()//2, 
                                    backRect.centery - backText.get_height()//2))
            
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                elif event.type == p.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if backRect.collidepoint(event.pos):
                            running = False
                        else:
                            self.handleClick(event.pos, sidebarWidth)
                    elif event.button == 4:  # Scroll up
                        self.handleScroll(1)
                    elif event.button == 5:  # Scroll down
                        self.handleScroll(-1)
                elif event.type == p.KEYDOWN:
                    if event.key == p.K_ESCAPE:
                        running = False
                    elif event.key == p.K_UP:
                        self.handleScroll(1)
                    elif event.key == p.K_DOWN:
                        self.handleScroll(-1)
                    elif event.key == p.K_HOME:
                        self.scrollOffset = 0
                    elif event.key == p.K_END:
                        self.scrollOffset = self.maxScroll
            
            p.display.flip()
            self.clock.tick(60)