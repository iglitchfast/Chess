import pygame as p
import ChessEngine, ChessAI
import time
import ChessExplain

WIDTH = HEIGHT = 640
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}
PANEL_WIDTH = 280

THEMES = {
    "Classic": {"light": (238, 238, 210), "dark": (118, 150, 86), "accent": (186, 202, 68)},
    "Blue": {"light": (222, 227, 230), "dark": (140, 162, 173), "accent": (99, 133, 153)},
    "Brown": {"light": (240, 217, 181), "dark": (181, 136, 99), "accent": (205, 170, 125)},
    "Green": {"light": (234, 240, 206), "dark": (87, 138, 52), "accent": (106, 176, 76)},
    "Purple": {"light": (230, 220, 240), "dark": (150, 100, 180), "accent": (180, 130, 210)},
    "Ocean": {"light": (200, 230, 240), "dark": (80, 130, 170), "accent": (120, 180, 210)}
}

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
    }
}

PIECE_SETS = ["images", "images_bold", "images_site"]

def load_images(piece_set="images_site"):
    global IMAGES
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        try:
            IMAGES[piece] = p.transform.scale(p.image.load(f"{piece_set}/{piece}.png"), (SQ_SIZE, SQ_SIZE))
        except:
            print(f"Warning: Could not load {piece_set}/{piece}.png")

def playMoveSound(move, gs, sounds):
    if not sounds:
        return
    if move.isCastleMove:
        sounds["castle"].play()
    elif move.pieceCaptured != "--":
        sounds["capture"].play()
    elif gs.inCheck():
        sounds["check"].play()
    else:
        sounds["move"].play()

def drawGradientBackground(screen, width, height, color1, color2):
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        p.draw.line(screen, (r, g, b), (0, y), (width, y))

def drawButton(screen, rect, text, font, base_color, hover_color, mouse_pos, border_width=3):
    isHover = rect.collidepoint(mouse_pos)
    color = hover_color if isHover else base_color
    
    shadowRect = rect.copy()
    shadowRect.x += 4
    shadowRect.y += 4
    p.draw.rect(screen, (50, 50, 50), shadowRect, border_radius=12)
    
    p.draw.rect(screen, color, rect, border_radius=12)
    p.draw.rect(screen, (0, 0, 0), rect, border_width, border_radius=12)
    
    textObj = font.render(text, True, (0, 0, 0))
    screen.blit(textObj, (rect.centerx - textObj.get_width()//2, rect.centery - textObj.get_height()//2))
    
    return isHover

def drawMenu(screen, titleFont, font):
    totalWidth = WIDTH + PANEL_WIDTH
    if DARK_MODE["enabled"]:
        drawGradientBackground(screen, totalWidth, HEIGHT, DARK_MODE["colors"]["bg_primary"], DARK_MODE["colors"]["bg_secondary"])
        title_color = DARK_MODE["colors"]["text_primary"]
        subtitle_color = DARK_MODE["colors"]["text_secondary"]
        footer_color = DARK_MODE["colors"]["text_secondary"]
    else:
        drawGradientBackground(screen, totalWidth, HEIGHT, (240, 240, 250), (200, 210, 230))
        title_color = (40, 40, 60)
        subtitle_color = (100, 100, 120)
        footer_color = (100, 100, 120)
    
    title = titleFont.render("CHESS", True, title_color)
    titleShadow = titleFont.render("CHESS", True, (150, 150, 160) if not DARK_MODE["enabled"] else (50, 50, 60))
    screen.blit(titleShadow, (totalWidth//2 - title.get_width()//2 + 4, 64))
    screen.blit(title, (totalWidth//2 - title.get_width()//2, 60))
    
    subtitleFont = p.font.SysFont("Arial", 18, False, True)
    subtitle = subtitleFont.render("Enhanced Edition", True, subtitle_color)
    screen.blit(subtitle, (totalWidth//2 - subtitle.get_width()//2, 120))
    
    mousePos = p.mouse.get_pos()
    buttonFont = p.font.SysFont("Arial", 22, True)
    
    aiRect = p.Rect(totalWidth//2 - 140, HEIGHT//2 - 100, 280, 60)
    drawButton(screen, aiRect, "Play vs AI", buttonFont, (120, 180, 255), (80, 150, 255), mousePos)
    
    pvpRect = p.Rect(totalWidth//2 - 140, HEIGHT//2 - 20, 280, 60)
    drawButton(screen, pvpRect, "Player vs Player", buttonFont, (120, 255, 180), (80, 230, 150), mousePos)
    
    settingsRect = p.Rect(totalWidth//2 - 140, HEIGHT//2 + 60, 280, 60)
    drawButton(screen, settingsRect, "Settings", buttonFont, (255, 220, 120), (255, 200, 80), mousePos)
    
    footerFont = p.font.SysFont("Arial", 13)
    footer = footerFont.render("Press ESC to quit | Z to undo | R to reset", True, footer_color)
    screen.blit(footer, (totalWidth//2 - footer.get_width()//2, HEIGHT - 40))

def drawGameModeMenu(screen, titleFont, font, totalWidth):
    """Menu to choose undo settings before starting game"""
    if DARK_MODE["enabled"]:
        drawGradientBackground(screen, totalWidth, HEIGHT, DARK_MODE["colors"]["bg_primary"], DARK_MODE["colors"]["bg_secondary"])
        title_color = DARK_MODE["colors"]["text_primary"]
    else:
        drawGradientBackground(screen, totalWidth, HEIGHT, (240, 240, 250), (200, 210, 230))
        title_color = (40, 40, 60)
    
    title = titleFont.render("GAME OPTIONS", True, title_color)
    screen.blit(title, (totalWidth//2 - title.get_width()//2, 60))
    
    mousePos = p.mouse.get_pos()
    buttonFont = p.font.SysFont("Arial", 20, True)
    
    # Undo enabled button
    undoYesRect = p.Rect(totalWidth//2 - 140, 200, 280, 60)
    drawButton(screen, undoYesRect, "Enable Undo", buttonFont, (150, 255, 150), (100, 230, 100), mousePos)
    
    # Undo disabled button
    undoNoRect = p.Rect(totalWidth//2 - 140, 280, 280, 60)
    drawButton(screen, undoNoRect, "Disable Undo", buttonFont, (255, 180, 150), (255, 140, 110), mousePos)
    
    backRect = p.Rect(30, HEIGHT - 70, 120, 45)
    drawButton(screen, backRect, "< Back", font, (255, 150, 150), (255, 100, 100), mousePos)
    
    return undoYesRect, undoNoRect, backRect

def drawSettingsMain(screen, titleFont, font, totalWidth):
    if DARK_MODE["enabled"]:
        drawGradientBackground(screen, totalWidth, HEIGHT, DARK_MODE["colors"]["bg_primary"], DARK_MODE["colors"]["bg_secondary"])
        title_color = DARK_MODE["colors"]["text_primary"]
    else:
        drawGradientBackground(screen, totalWidth, HEIGHT, (240, 240, 250), (200, 210, 230))
        title_color = (40, 40, 60)
    
    title = titleFont.render("SETTINGS", True, title_color)
    titleShadow = titleFont.render("SETTINGS", True, (150, 150, 160) if not DARK_MODE["enabled"] else (50, 50, 60))
    screen.blit(titleShadow, (totalWidth//2 - title.get_width()//2 + 4, 64))
    screen.blit(title, (totalWidth//2 - title.get_width()//2, 60))
    
    mousePos = p.mouse.get_pos()
    buttonFont = p.font.SysFont("Arial", 20, True)
    
    buttons = [
        ("Board Theme", (200, 180, 255)),
        ("Piece Style", (180, 220, 255)),
        ("AI Difficulty", (255, 200, 180)),
        ("Timer Settings", (255, 220, 180)),
        ("Dark Mode", (180, 180, 200)),
        ("Interactive Guide", (150, 255, 200))
    ]
    
    y = 150
    for text, color in buttons:
        rect = p.Rect(totalWidth//2 - 140, y, 280, 55)
        drawButton(screen, rect, text, buttonFont, color, tuple(max(0, c-40) for c in color), mousePos)
        y += 65
    
    backRect = p.Rect(30, HEIGHT - 70, 120, 45)
    drawButton(screen, backRect, "< Back", font, (255, 150, 150), (255, 100, 100), mousePos)

def drawThemeSettings(screen, titleFont, font, currentTheme, totalWidth):
    if DARK_MODE["enabled"]:
        drawGradientBackground(screen, totalWidth, HEIGHT, DARK_MODE["colors"]["bg_primary"], DARK_MODE["colors"]["bg_secondary"])
        title_color = DARK_MODE["colors"]["text_primary"]
    else:
        drawGradientBackground(screen, totalWidth, HEIGHT, (240, 240, 250), (200, 210, 230))
        title_color = (40, 40, 60)
    
    title = titleFont.render("BOARD THEMES", True, title_color)
    screen.blit(title, (totalWidth//2 - title.get_width()//2, 60))
    
    mousePos = p.mouse.get_pos()
    buttonFont = p.font.SysFont("Arial", 19, True)
    
    y = 160
    for theme in THEMES.keys():
        rect = p.Rect(totalWidth//2 - 140, y, 280, 50)
        color = (255, 215, 0) if theme == currentTheme else (220, 220, 230)
        hover = (255, 180, 0) if theme == currentTheme else (200, 200, 220)
        drawButton(screen, rect, theme, buttonFont, color, hover, mousePos, 4 if theme == currentTheme else 2)
        
        themeColors = THEMES[theme]
        colorBox1 = p.Rect(rect.x + 15, rect.centery - 12, 24, 24)
        colorBox2 = p.Rect(rect.x + 45, rect.centery - 12, 24, 24)
        p.draw.rect(screen, themeColors["light"], colorBox1, border_radius=4)
        p.draw.rect(screen, themeColors["dark"], colorBox2, border_radius=4)
        p.draw.rect(screen, (0, 0, 0), colorBox1, 2, border_radius=4)
        p.draw.rect(screen, (0, 0, 0), colorBox2, 2, border_radius=4)
        
        y += 60
    
    backRect = p.Rect(30, HEIGHT - 70, 120, 45)
    drawButton(screen, backRect, "< Back", font, (255, 150, 150), (255, 100, 100), mousePos)
    
def drawPieceSetSettings(screen, titleFont, font, currentPieceSet, totalWidth):
    if DARK_MODE["enabled"]:
        drawGradientBackground(screen, totalWidth, HEIGHT, DARK_MODE["colors"]["bg_primary"], DARK_MODE["colors"]["bg_secondary"])
        title_color = DARK_MODE["colors"]["text_primary"]
    else:
        drawGradientBackground(screen, totalWidth, HEIGHT, (240, 240, 250), (200, 210, 230))
        title_color = (40, 40, 60)
    
    title = titleFont.render("PIECE STYLE", True, title_color)
    screen.blit(title, (totalWidth//2 - title.get_width()//2, 60))
    
    mousePos = p.mouse.get_pos()
    buttonFont = p.font.SysFont("Arial", 19, True)
    
    labels = ["Classic", "Bold", "Modern"]
    y = 200
    for i, piece_set in enumerate(PIECE_SETS):
        rect = p.Rect(totalWidth//2 - 140, y, 280, 55)
        color = (255, 215, 0) if piece_set == currentPieceSet else (220, 220, 230)
        hover = (255, 180, 0) if piece_set == currentPieceSet else (200, 200, 220)
        drawButton(screen, rect, labels[i], buttonFont, color, hover, mousePos, 4 if piece_set == currentPieceSet else 2)
        y += 70
    
    backRect = p.Rect(30, HEIGHT - 70, 120, 45)
    drawButton(screen, backRect, "< Back", font, (255, 150, 150), (255, 100, 100), mousePos)

def drawDifficultySettings(screen, titleFont, font, currentDifficulty, totalWidth):
    if DARK_MODE["enabled"]:
        drawGradientBackground(screen, totalWidth, HEIGHT, DARK_MODE["colors"]["bg_primary"], DARK_MODE["colors"]["bg_secondary"])
        title_color = DARK_MODE["colors"]["text_primary"]
    else:
        drawGradientBackground(screen, totalWidth, HEIGHT, (240, 240, 250), (200, 210, 230))
        title_color = (40, 40, 60)
    
    title = titleFont.render("AI DIFFICULTY", True, title_color)
    screen.blit(title, (totalWidth//2 - title.get_width()//2, 60))
    
    mousePos = p.mouse.get_pos()
    buttonFont = p.font.SysFont("Arial", 19, True)
    
    difficulties = [("Easy", 1, (150, 255, 150)), ("Medium", 2, (255, 255, 150)), 
                   ("Hard", 3, (255, 200, 150)), ("Expert", 4, (255, 150, 150))]
    y = 200
    for name, level, base_color in difficulties:
        rect = p.Rect(totalWidth//2 - 140, y, 280, 55)
        color = (255, 215, 0) if level == currentDifficulty else base_color
        hover = (255, 180, 0) if level == currentDifficulty else tuple(max(0, c-30) for c in base_color)
        drawButton(screen, rect, name, buttonFont, color, hover, mousePos, 4 if level == currentDifficulty else 2)
        y += 70
    
    backRect = p.Rect(30, HEIGHT - 70, 120, 45)
    drawButton(screen, backRect, "< Back", font, (255, 150, 150), (255, 100, 100), mousePos)

def drawTimeSettings(screen, titleFont, font, timerEnabled, currentTime, totalWidth):
    if DARK_MODE["enabled"]:
        drawGradientBackground(screen, totalWidth, HEIGHT, DARK_MODE["colors"]["bg_primary"], DARK_MODE["colors"]["bg_secondary"])
        title_color = DARK_MODE["colors"]["text_primary"]
    else:
        drawGradientBackground(screen, totalWidth, HEIGHT, (240, 240, 250), (200, 210, 230))
        title_color = (40, 40, 60)
    
    title = titleFont.render("TIMER SETTINGS", True, title_color)
    screen.blit(title, (totalWidth//2 - title.get_width()//2, 60))
    
    mousePos = p.mouse.get_pos()
    buttonFont = p.font.SysFont("Arial", 20, True)
    
    toggleRect = p.Rect(totalWidth//2 - 140, 150, 280, 60)
    if DARK_MODE["enabled"]:
        toggleColor = DARK_MODE["colors"]["success"] if timerEnabled else DARK_MODE["colors"]["danger"]
        toggleHover = tuple(min(255, c+30) for c in toggleColor)
    else:
        toggleColor = (100, 255, 150) if timerEnabled else (255, 150, 150)
        toggleHover = (80, 230, 130) if timerEnabled else (255, 100, 100)
    
    toggleText = f"Timer: {'ON' if timerEnabled else 'OFF'}"
    drawButton(screen, toggleRect, toggleText, buttonFont, toggleColor, toggleHover, mousePos)
    
    timeOptions = [(180, "3 min"), (300, "5 min"), (600, "10 min"), (900, "15 min")]
    grid_width = 260 * 2 + 20
    start_x = totalWidth//2 - grid_width//2
    
    y = 240
    for idx, (time_val, label) in enumerate(timeOptions):
        col = idx % 2
        row = idx // 2
        x = start_x + col * (260 + 20)
        y_pos = y + row * 70
        
        rect = p.Rect(x, y_pos, 260, 55)
        
        if DARK_MODE["enabled"]:
            color = DARK_MODE["colors"]["accent"] if time_val == currentTime else DARK_MODE["colors"]["button_bg"]
            hover = DARK_MODE["colors"]["accent_hover"] if time_val == currentTime else DARK_MODE["colors"]["button_hover"]
        else:
            color = (255, 215, 0) if time_val == currentTime else (220, 220, 230)
            hover = (255, 180, 0) if time_val == currentTime else (200, 200, 220)
        
        drawButton(screen, rect, label, buttonFont, color, hover, mousePos, 4 if time_val == currentTime else 2)
    
    backRect = p.Rect(30, HEIGHT - 70, 120, 45)
    if DARK_MODE["enabled"]:
        drawButton(screen, backRect, "< Back", font, DARK_MODE["colors"]["danger"], tuple(min(255, c+40) for c in DARK_MODE["colors"]["danger"]), mousePos)
    else:
        drawButton(screen, backRect, "< Back", font, (255, 150, 150), (255, 100, 100), mousePos)

def drawDarkModeSettings(screen, titleFont, font, totalWidth):
    if DARK_MODE["enabled"]:
        drawGradientBackground(screen, totalWidth, HEIGHT, DARK_MODE["colors"]["bg_primary"], DARK_MODE["colors"]["bg_secondary"])
        title_color = DARK_MODE["colors"]["text_primary"]
    else:
        drawGradientBackground(screen, totalWidth, HEIGHT, (240, 240, 250), (200, 210, 230))
        title_color = (40, 40, 60)
    
    title = titleFont.render("DARK MODE", True, title_color)
    screen.blit(title, (totalWidth//2 - title.get_width()//2, 60))
    
    mousePos = p.mouse.get_pos()
    buttonFont = p.font.SysFont("Arial", 20, True)
    
    onRect = p.Rect(totalWidth//2 - 140, 200, 280, 60)
    onColor = (255, 215, 0) if DARK_MODE["enabled"] else (100, 100, 100)
    onHover = (255, 180, 0) if DARK_MODE["enabled"] else (80, 80, 80)
    drawButton(screen, onRect, "Dark Mode ON", buttonFont, onColor, onHover, mousePos)
    
    offRect = p.Rect(totalWidth//2 - 140, 280, 280, 60)
    offColor = (255, 215, 0) if not DARK_MODE["enabled"] else (220, 220, 220)
    offHover = (255, 180, 0) if not DARK_MODE["enabled"] else (200, 200, 200)
    drawButton(screen, offRect, "Dark Mode OFF", buttonFont, offColor, offHover, mousePos)
    
    backRect = p.Rect(30, HEIGHT - 70, 120, 45)
    drawButton(screen, backRect, "< Back", font, (255, 150, 150), (255, 100, 100), mousePos)
    
    return onRect, offRect, backRect

def drawBoard(screen, theme="Classic"):
    colors = THEMES[theme]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors["light"] if (r + c) % 2 == 0 else colors["dark"]
            rect = p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, rect)
    
    p.draw.rect(screen, p.Color('black'), p.Rect(0, 0, WIDTH, HEIGHT), 3)
    
    coordFont = p.font.SysFont("Arial", 14, True)
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
    
    for i, file in enumerate(files):
        text = coordFont.render(file, True, p.Color('black'))
        screen.blit(text, (i * SQ_SIZE + SQ_SIZE - 15, HEIGHT - 18))
    
    for i, rank in enumerate(ranks):
        text = coordFont.render(rank, True, p.Color('black'))
        screen.blit(text, (5, i * SQ_SIZE + 5))

def highlightSquares(screen, gs, validMoves, sqSelected, theme="Classic"):
    if len(gs.moveLog) > 0:
        lastMove = gs.moveLog[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(120)
        s.fill(p.Color(255, 255, 100))
        screen.blit(s, (lastMove.endCol * SQ_SIZE, lastMove.endRow * SQ_SIZE))
        s.fill(p.Color(255, 255, 150))
        screen.blit(s, (lastMove.startCol * SQ_SIZE, lastMove.startRow * SQ_SIZE))
    
    if gs.inCheck():
        kingLoc = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(180)
        s.fill(p.Color(255, 50, 50))
        screen.blit(s, (kingLoc[1] * SQ_SIZE, kingLoc[0] * SQ_SIZE))
        p.draw.rect(screen, p.Color(200, 0, 0), 
                   p.Rect(kingLoc[1] * SQ_SIZE, kingLoc[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE), 4)
    
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(130)
            s.fill(p.Color(100, 150, 255))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
            
            p.draw.rect(screen, p.Color(50, 100, 255), 
                       p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)
            
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    centerX = move.endCol * SQ_SIZE + SQ_SIZE // 2
                    centerY = move.endRow * SQ_SIZE + SQ_SIZE // 2
                    
                    if move.pieceCaptured != '--':
                        p.draw.circle(screen, p.Color(255, 80, 80), (centerX, centerY), SQ_SIZE // 3, 5)
                        p.draw.circle(screen, p.Color(255, 50, 50), (centerX, centerY), SQ_SIZE // 3 - 5, 0)
                    else:
                        p.draw.circle(screen, p.Color(100, 100, 100), (centerX, centerY), SQ_SIZE // 8)

def drawGameState(screen, gs, validMoves, sqSelected, theme="Classic"):
    drawBoard(screen, theme)
    highlightSquares(screen, gs, validMoves, sqSelected, theme)
    drawPieces(screen, gs.board)

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, moveLog, font):
    logRect = p.Rect(WIDTH, 80, PANEL_WIDTH, HEIGHT - 200)
    
    for i in range(logRect.height):
        shade = 250 - int(i / logRect.height * 20)
        p.draw.line(screen, (shade, shade, shade - 10), 
                   (logRect.x, logRect.y + i), (logRect.x + logRect.width, logRect.y + i))
    
    p.draw.rect(screen, p.Color("black"), logRect, 2)
    
    titleFont = p.font.SysFont("Arial", 18, True)
    title = titleFont.render("Move History", True, p.Color("black"))
    titleBg = p.Rect(WIDTH, 55, PANEL_WIDTH, 30)
    p.draw.rect(screen, p.Color(200, 200, 220), titleBg)
    p.draw.rect(screen, p.Color("black"), titleBg, 2)
    screen.blit(title, (WIDTH + PANEL_WIDTH//2 - title.get_width()//2, 60))
    
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        whiteMove = moveLog[i].getChessNotation()
        blackMove = moveLog[i + 1].getChessNotation() if i + 1 < len(moveLog) else ""
        moveTexts.append((i//2 + 1, whiteMove, blackMove))
    
    moveY = 90
    startIdx = max(0, len(moveTexts) - 18)
    
    for idx, (moveNum, white, black) in enumerate(moveTexts[startIdx:]):
        if idx % 2 == 0:
            rowRect = p.Rect(WIDTH + 5, moveY - 2, PANEL_WIDTH - 10, 20)
            p.draw.rect(screen, p.Color(230, 230, 240), rowRect)
        
        numText = font.render(f"{moveNum}.", True, p.Color("darkblue"))
        screen.blit(numText, (WIDTH + 10, moveY))
        
        whiteText = font.render(white, True, p.Color("black"))
        screen.blit(whiteText, (WIDTH + 45, moveY))
        
        if black:
            blackText = font.render(black, True, p.Color("dimgray"))
            screen.blit(blackText, (WIDTH + 140, moveY))
        
        moveY += 22
    
    if len(moveTexts) > 18:
        scrollText = font.render(" More moves ", True, p.Color("gray"))
        screen.blit(scrollText, (WIDTH + PANEL_WIDTH//2 - scrollText.get_width()//2, HEIGHT - 125))

def drawButtons(screen, font, undoEnabled=True):
    buttonY = HEIGHT - 100
    buttonFont = p.font.SysFont("Arial", 16, True)
    mousePos = p.mouse.get_pos()
    
    if DARK_MODE["enabled"]:
        shadow_color = (15, 15, 15)
        border_color = DARK_MODE["colors"]["border"]
        text_color = DARK_MODE["colors"]["text_primary"]
        homeColor = DARK_MODE["colors"]["accent_hover"]
        homeBaseColor = DARK_MODE["colors"]["accent"]
        undoColor = (255, 140, 80)
        undoBaseColor = (220, 100, 40)
        resetColor = DARK_MODE["colors"]["success"]
        resetBaseColor = (70, 150, 100)
    else:
        shadow_color = p.Color('gray')
        border_color = p.Color('black')
        text_color = p.Color('black')
        homeColor = p.Color(100, 180, 255)
        homeBaseColor = p.Color(140, 200, 255)
        undoColor = p.Color(255, 180, 100)
        undoBaseColor = p.Color(255, 200, 140)
        resetColor = p.Color(100, 255, 150)
        resetBaseColor = p.Color(140, 255, 180)
    
    if undoEnabled:
        # HOME BUTTON
        homeRect = p.Rect(WIDTH + 15, buttonY, 75, 35)
        homeHover = homeRect.collidepoint(mousePos)
        home_display_color = homeColor if homeHover else homeBaseColor
        
        shadowRect = homeRect.move(2, 2)
        p.draw.rect(screen, shadow_color, shadowRect, border_radius=8)
        p.draw.rect(screen, home_display_color, homeRect, border_radius=8)
        p.draw.rect(screen, border_color, homeRect, 2, border_radius=8)
        
        homeText = buttonFont.render('Home', True, text_color)
        screen.blit(homeText, (homeRect.centerx - homeText.get_width()//2, homeRect.centery - homeText.get_height()//2))
        
        # UNDO BUTTON
        undoRect = p.Rect(WIDTH + 100, buttonY, 75, 35)
        undoHover = undoRect.collidepoint(mousePos)
        undo_display_color = undoColor if undoHover else undoBaseColor
        
        shadowRect = undoRect.move(2, 2)
        p.draw.rect(screen, shadow_color, shadowRect, border_radius=8)
        p.draw.rect(screen, undo_display_color, undoRect, border_radius=8)
        p.draw.rect(screen, border_color, undoRect, 2, border_radius=8)
        
        undoText = buttonFont.render('Undo', True, text_color)
        screen.blit(undoText, (undoRect.centerx - undoText.get_width()//2, undoRect.centery - undoText.get_height()//2))
        
        # RESET BUTTON
        resetRect = p.Rect(WIDTH + 185, buttonY, 75, 35)
        resetHover = resetRect.collidepoint(mousePos)
        reset_display_color = resetColor if resetHover else resetBaseColor
        
        shadowRect = resetRect.move(2, 2)
        p.draw.rect(screen, shadow_color, shadowRect, border_radius=8)
        p.draw.rect(screen, reset_display_color, resetRect, border_radius=8)
        p.draw.rect(screen, border_color, resetRect, 2, border_radius=8)
        
        resetText = buttonFont.render('Reset', True, text_color)
        screen.blit(resetText, (resetRect.centerx - resetText.get_width()//2, resetRect.centery - resetText.get_height()//2))
        
        return homeRect, undoRect, resetRect
    else:
        # Only HOME and RESET buttons, centered
        homeRect = p.Rect(WIDTH + 50, buttonY, 75, 35)
        homeHover = homeRect.collidepoint(mousePos)
        home_display_color = homeColor if homeHover else homeBaseColor
        
        shadowRect = homeRect.move(2, 2)
        p.draw.rect(screen, shadow_color, shadowRect, border_radius=8)
        p.draw.rect(screen, home_display_color, homeRect, border_radius=8)
        p.draw.rect(screen, border_color, homeRect, 2, border_radius=8)
        
        homeText = buttonFont.render('Home', True, text_color)
        screen.blit(homeText, (homeRect.centerx - homeText.get_width()//2, homeRect.centery - homeText.get_height()//2))
        
        # RESET BUTTON
        resetRect = p.Rect(WIDTH + 145, buttonY, 75, 35)
        resetHover = resetRect.collidepoint(mousePos)
        reset_display_color = resetColor if resetHover else resetBaseColor
        
        shadowRect = resetRect.move(2, 2)
        p.draw.rect(screen, shadow_color, shadowRect, border_radius=8)
        p.draw.rect(screen, reset_display_color, resetRect, border_radius=8)
        p.draw.rect(screen, border_color, resetRect, 2, border_radius=8)
        
        resetText = buttonFont.render('Reset', True, text_color)
        screen.blit(resetText, (resetRect.centerx - resetText.get_width()//2, resetRect.centery - resetText.get_height()//2))
        
        return homeRect, None, resetRect

def drawTurnIndicator(screen, gs, font):
    turnRect = p.Rect(WIDTH + 10, 10, PANEL_WIDTH - 20, 40)
    
    if gs.whiteToMove:
        for i in range(turnRect.height):
            shade = 255 - int(i / turnRect.height * 30)
            p.draw.line(screen, (shade, shade, shade), 
                       (turnRect.x, turnRect.y + i), (turnRect.x + turnRect.width, turnRect.y + i))
    else:
        for i in range(turnRect.height):
            shade = 120 - int(i / turnRect.height * 20)
            p.draw.line(screen, (shade, shade, shade), 
                       (turnRect.x, turnRect.y + i), (turnRect.x + turnRect.width, turnRect.y + i))
    
    p.draw.rect(screen, p.Color('black'), turnRect, 3)
    
    icon = "♔" if gs.whiteToMove else "♚"
    turn_text = f"{icon} White's Turn" if gs.whiteToMove else f"{icon} Black's Turn"
    
    textFont = p.font.SysFont("Arial", 20, True)
    textColor = p.Color('black') if gs.whiteToMove else p.Color('white')
    textObj = textFont.render(turn_text, True, textColor)
    screen.blit(textObj, (turnRect.centerx - textObj.get_width()//2, turnRect.centery - textObj.get_height()//2))

def drawTimer(screen, whiteTime, blackTime, isWhiteTurn, font):
    def formatTime(seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d}"
    
    timerRect = p.Rect(WIDTH + 10, HEIGHT - 160, PANEL_WIDTH - 20, 55)
    
    # Background gradient
    for i in range(timerRect.height):
        shade = 245 - int(i / timerRect.height * 20)
        p.draw.line(screen, (shade, shade, shade + 5), 
                   (timerRect.x, timerRect.y + i), (timerRect.x + timerRect.width, timerRect.y + i))
    
    p.draw.rect(screen, p.Color('black'), timerRect, 3)
    
    # Title
    titleFont = p.font.SysFont("Arial", 14, True)
    title = titleFont.render("GAME TIMER", True, p.Color('darkblue'))
    screen.blit(title, (timerRect.centerx - title.get_width()//2, timerRect.y + 5))
    
    # White timer
    whiteRect = p.Rect(timerRect.x + 10, timerRect.y + 25, (timerRect.width - 25) // 2, 22)
    wColor = p.Color('lightgreen') if isWhiteTurn else p.Color(220, 220, 220)
    p.draw.rect(screen, wColor, whiteRect, border_radius=5)
    p.draw.rect(screen, p.Color('black'), whiteRect, 2, border_radius=5)
    
    timeFont = p.font.SysFont("Arial", 16, True)
    wText = timeFont.render(f"♔ {formatTime(whiteTime)}", True, p.Color('black'))
    screen.blit(wText, (whiteRect.x + 5, whiteRect.y + 3))
    
    # Black timer
    blackRect = p.Rect(timerRect.centerx + 5, timerRect.y + 25, (timerRect.width - 25) // 2, 22)
    bColor = p.Color('lightgreen') if not isWhiteTurn else p.Color(220, 220, 220)
    p.draw.rect(screen, bColor, blackRect, border_radius=5)
    p.draw.rect(screen, p.Color('black'), blackRect, 2, border_radius=5)
    
    bText = timeFont.render(f"♚ {formatTime(blackTime)}", True, p.Color('black'))
    screen.blit(bText, (blackRect.x + 5, blackRect.y + 3))
    
def drawPromotionMenu(screen, isWhite):
    overlay = p.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay_color = (20, 20, 20) if DARK_MODE["enabled"] else (0, 0, 0)
    overlay.fill(overlay_color)
    screen.blit(overlay, (0, 0))
    
    titleFont = p.font.SysFont("Arial", 28, True)
    title_text = titleFont.render("Promote Pawn", True, 
                                   DARK_MODE["colors"]["text_primary"] if DARK_MODE["enabled"] else (255, 255, 255))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 120))
    
    pieces = ['Q', 'R', 'B', 'N']
    boxSize = 80
    gap = 15
    total_width = (boxSize * 4) + (gap * 3)
    startX = WIDTH//2 - total_width//2
    y = HEIGHT//2 - 40
    
    for i, piece in enumerate(pieces):
        x = startX + i * (boxSize + gap)
        rect = p.Rect(x, y, boxSize, boxSize)
        
        if DARK_MODE["enabled"]:
            p.draw.rect(screen, DARK_MODE["colors"]["button_hover"], rect, border_radius=8)
            p.draw.rect(screen, DARK_MODE["colors"]["accent"], rect, 3, border_radius=8)
        else:
            p.draw.rect(screen, p.Color('white'), rect, border_radius=8)
            p.draw.rect(screen, p.Color('black'), rect, 3, border_radius=8)
        
        color = 'w' if isWhite else 'b'
        pieceImg = IMAGES[color + piece]
        # Scale down piece image to fit better
        scaledPiece = p.transform.scale(pieceImg, (boxSize - 20, boxSize - 20))
        screen.blit(scaledPiece, (x + 10, y + 10))
        
        labelFont = p.font.SysFont("Arial", 14, True)
        piece_names = {'Q': 'Queen', 'R': 'Rook', 'B': 'Bishop', 'N': 'Knight'}
        label = labelFont.render(piece_names[piece], True,
                                 DARK_MODE["colors"]["text_secondary"] if DARK_MODE["enabled"] else (200, 200, 200))
        screen.blit(label, (x + boxSize//2 - label.get_width()//2, y + boxSize + 8))

def handlePromotionClick(location):
    pieces = ['Q', 'R', 'B', 'N']
    boxSize = 80
    gap = 15
    total_width = (boxSize * 4) + (gap * 3)
    startX = WIDTH//2 - total_width//2
    y = HEIGHT//2 - 40
    
    for i, piece in enumerate(pieces):
        x = startX + i * (boxSize + gap)
        if x <= location[0] <= x + boxSize and y <= location[1] <= y + boxSize:
            return piece
    return None

def animateMove(move, screen, board, clock, theme="Classic"):
    colors = THEMES[theme]
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 3
    frameCount = int((abs(dR) + abs(dC)) * framesPerSquare)
    
    for frame in range(frameCount + 1):
        r = move.startRow + dR * frame / frameCount
        c = move.startCol + dC * frame / frameCount
        drawBoard(screen, theme)
        drawPieces(screen, board)
        
        color = colors["light"] if (move.endRow + move.endCol) % 2 == 0 else colors["dark"]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, True, p.Color('white'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - textObject.get_width() // 2, HEIGHT // 2 - textObject.get_height() // 2)
    
    overlay = p.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(p.Color('black'))
    screen.blit(overlay, (0, 0))
    screen.blit(textObject, textLocation)

def main():
    p.init()
    try:
        p.mixer.init()
        sounds = {
            "move": p.mixer.Sound("sounds/move-normal.mp3"),
            "capture": p.mixer.Sound("sounds/capture.mp3"),
            "check": p.mixer.Sound("sounds/move-check.mp3"),
            "promote": p.mixer.Sound("sounds/promote.mp3"),
            "castle": p.mixer.Sound("sounds/castle.mp3"),
            "start": p.mixer.Sound("sounds/game-start.mp3"),
            "end": p.mixer.Sound("sounds/game-end.mp3"),
            "illegal": p.mixer.Sound("sounds/illegal.mp3")
        }
    except:
        sounds = None

    screen = p.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT))
    p.display.set_caption("Chess Game - Enhanced Edition")
    clock = p.time.Clock()
    
    gs = None
    validMoves = []
    moveMade = False
    animate = False
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True
    playerTwo = False
    aiDifficulty = 3
    currentTheme = "Brown"
    currentPieceSet = "images_site"
    
    selectedTimeLimit = 600
    whiteTime = 600
    blackTime = 600
    lastTime = time.time()
    timerEnabled = False
    timerStarted = False
    undoEnabled = True
    
    gameState = "menu"
    settingsState = "main"
    gameModeState = None
    promotionPiece = None
    showingPromotion = False
    
    load_images(currentPieceSet)
    font = p.font.SysFont("Arial", 16, False, False)
    titleFont = p.font.SysFont("Arial", 38, True, False)
    running = True

    while running:
        if gameState == "menu":
            drawMenu(screen, titleFont, font)
            p.display.flip()
            
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    totalWidth = WIDTH + PANEL_WIDTH
                    
                    aiRect = p.Rect(totalWidth//2 - 140, HEIGHT//2 - 100, 280, 60)
                    if aiRect.collidepoint(location):
                        gameModeState = "ai"
                        gameState = "gamemode"
                    
                    pvpRect = p.Rect(totalWidth//2 - 140, HEIGHT//2 - 20, 280, 60)
                    if pvpRect.collidepoint(location):
                        gameModeState = "pvp"
                        gameState = "gamemode"
                    
                    settingsRect = p.Rect(totalWidth//2 - 140, HEIGHT//2 + 60, 280, 60)
                    if settingsRect.collidepoint(location):
                        gameState = "settings"
                        settingsState = "main"
        
        elif gameState == "gamemode":
            totalWidth = WIDTH + PANEL_WIDTH
            undoYesRect, undoNoRect, backRect = drawGameModeMenu(screen, titleFont, font, totalWidth)
            p.display.flip()
            
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        gameState = "menu"
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    
                    if undoYesRect.collidepoint(location):
                        undoEnabled = True
                        if gameModeState == "ai":
                            playerOne = True
                            playerTwo = False
                        else:
                            playerOne = True
                            playerTwo = True
                        
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        gameState = "game"
                        gameOver = False
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        whiteTime = selectedTimeLimit
                        blackTime = selectedTimeLimit
                        lastTime = time.time()
                        timerStarted = False
                        if sounds:
                            sounds["start"].play()
                    
                    elif undoNoRect.collidepoint(location):
                        undoEnabled = False
                        if gameModeState == "ai":
                            playerOne = True
                            playerTwo = False
                        else:
                            playerOne = True
                            playerTwo = True
                        
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        gameState = "game"
                        gameOver = False
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        whiteTime = selectedTimeLimit
                        blackTime = selectedTimeLimit
                        lastTime = time.time()
                        timerStarted = False
                        if sounds:
                            sounds["start"].play()
                    
                    elif backRect.collidepoint(location):
                        gameState = "menu"
        
        elif gameState == "settings":
            totalWidth = WIDTH + PANEL_WIDTH
            
            if settingsState == "main":
                drawSettingsMain(screen, titleFont, font, totalWidth)
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_ESCAPE:
                            gameState = "menu"
                    elif e.type == p.MOUSEBUTTONDOWN:
                        location = p.mouse.get_pos()
                        
                        y = 150
                        for i in range(6):
                            rect = p.Rect(totalWidth//2 - 140, y + i*65, 280, 55)
                            if rect.collidepoint(location):
                                if i == 0:
                                    settingsState = "theme"
                                elif i == 1:
                                    settingsState = "pieces"
                                elif i == 2:
                                    settingsState = "difficulty"
                                elif i == 3:
                                    settingsState = "time"
                                elif i == 4:
                                    settingsState = "darkmode"
                                elif i == 5:
                                     explainSys = ChessExplain.ExplainSystem()
                                     explainSys.run()
                        
                        backRect = p.Rect(30, HEIGHT - 70, 120, 45)
                        if backRect.collidepoint(location):
                            gameState = "menu"
            
            elif settingsState == "theme":
                drawThemeSettings(screen, titleFont, font, currentTheme, totalWidth)
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_ESCAPE:
                            settingsState = "main"
                    elif e.type == p.MOUSEBUTTONDOWN:
                        location = p.mouse.get_pos()
                        y_start = 160
                        for i, theme in enumerate(THEMES.keys()):
                            themeRect = p.Rect(totalWidth//2 - 140, y_start + i*60, 280, 50)
                            if themeRect.collidepoint(location):
                                currentTheme = theme
                        
                        backRect = p.Rect(30, HEIGHT - 70, 120, 45)
                        if backRect.collidepoint(location):
                            settingsState = "main"
            
            elif settingsState == "pieces":
                drawPieceSetSettings(screen, titleFont, font, currentPieceSet, totalWidth)
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_ESCAPE:
                            settingsState = "main"
                    elif e.type == p.MOUSEBUTTONDOWN:
                        location = p.mouse.get_pos()
                        y_start = 200
                        for i, piece_set in enumerate(PIECE_SETS):
                            pieceRect = p.Rect(totalWidth//2 - 140, y_start + i*70, 280, 55)
                            if pieceRect.collidepoint(location):
                                currentPieceSet = piece_set
                                load_images(currentPieceSet)
                        
                        backRect = p.Rect(30, HEIGHT - 70, 120, 45)
                        if backRect.collidepoint(location):
                            settingsState = "main"
            
            elif settingsState == "difficulty":
                drawDifficultySettings(screen, titleFont, font, aiDifficulty, totalWidth)
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_ESCAPE:
                            settingsState = "main"
                    elif e.type == p.MOUSEBUTTONDOWN:
                        location = p.mouse.get_pos()
                        y_start = 200
                        difficulties = [1, 2, 3, 4]
                        for i, level in enumerate(difficulties):
                            diffRect = p.Rect(totalWidth//2 - 140, y_start + i*70, 280, 55)
                            if diffRect.collidepoint(location):
                                aiDifficulty = level
                        
                        backRect = p.Rect(30, HEIGHT - 70, 120, 45)
                        if backRect.collidepoint(location):
                            settingsState = "main"
            
            elif settingsState == "time":
                drawTimeSettings(screen, titleFont, font, timerEnabled, selectedTimeLimit, totalWidth)
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_ESCAPE:
                            settingsState = "main"
                    elif e.type == p.MOUSEBUTTONDOWN:
                        location = p.mouse.get_pos()
                        
                        toggleRect = p.Rect(totalWidth//2 - 140, 150, 280, 60)
                        if toggleRect.collidepoint(location):
                            timerEnabled = not timerEnabled
                        
                        times = [180, 300, 600, 900]
                        grid_width = 260 * 2 + 20
                        start_x = totalWidth//2 - grid_width//2
                        y = 240
                        for idx, t in enumerate(times):
                            col = idx % 2
                            row = idx // 2
                            x = start_x + col * (260 + 20)
                            y_pos = y + row * 70
                            timeRect = p.Rect(x, y_pos, 260, 55)
                            if timeRect.collidepoint(location):
                                selectedTimeLimit = t
                        
                        backRect = p.Rect(30, HEIGHT - 70, 120, 45)
                        if backRect.collidepoint(location):
                            settingsState = "main"
            
            elif settingsState == "darkmode":
                onRect, offRect, backRect = drawDarkModeSettings(screen, titleFont, font, totalWidth)
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_ESCAPE:
                            settingsState = "main"
                    elif e.type == p.MOUSEBUTTONDOWN:
                        location = p.mouse.get_pos()
                        
                        if onRect.collidepoint(location):
                            DARK_MODE["enabled"] = True
                        elif offRect.collidepoint(location):
                            DARK_MODE["enabled"] = False
                        elif backRect.collidepoint(location):
                            settingsState = "main"
            
            p.display.flip()
        
        elif gameState == "game":
            if gs is None:
                gameState = "menu"
                continue
                
            humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
            
            # Timer logic - only start after first move
            if timerEnabled and not gameOver and timerStarted:
                currentTime = time.time()
                elapsed = currentTime - lastTime
                lastTime = currentTime
                if gs.whiteToMove:
                    whiteTime -= elapsed
                    if whiteTime <= 0:
                        gameOver = True
                        whiteTime = 0
                else:
                    blackTime -= elapsed
                    if blackTime <= 0:
                        gameOver = True
                        blackTime = 0
            
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    
                    if showingPromotion:
                        choice = handlePromotionClick(location)
                        if choice:
                            promotionPiece = choice
                            showingPromotion = False
                            if len(gs.moveLog) > 0:
                                lastMove = gs.moveLog[-1]
                                lastMove.promotionChoice = promotionPiece
                                gs.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceMoved[0] + promotionPiece
                            if sounds and promotionPiece:
                                sounds["promote"].play()
                        continue
                    
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    
                    if WIDTH <= location[0]:
                        buttonRects = drawButtons(screen, font, undoEnabled)
                        if undoEnabled:
                            homeRect, undoRect, resetRect = buttonRects
                        else:
                            homeRect, undoRect, resetRect = buttonRects
                        
                        if homeRect.collidepoint(location):
                            gameState = "menu"
                            gs = None
                            validMoves = []
                            gameOver = False
                            sqSelected = ()
                            playerClicks = []
                            moveMade = False
                            animate = False
                            timerStarted = False
                            continue
                        
                        elif undoRect and undoRect.collidepoint(location) and undoEnabled:
                            if len(gs.moveLog) > 0:
                                if not playerTwo:
                                    if len(gs.moveLog) >= 2:
                                        gs.undoMove()
                                        gs.undoMove()
                                    elif len(gs.moveLog) == 1:
                                        gs.undoMove()
                                else:
                                    gs.undoMove()
                                moveMade = True
                                animate = False
                                sqSelected = ()
                                playerClicks = []
                                gameOver = False
                                # Reset timer after undo
                                if len(gs.moveLog) == 0:
                                    timerStarted = False
                        
                        elif resetRect.collidepoint(location):
                            gs = ChessEngine.GameState()
                            validMoves = gs.getValidMoves()
                            sqSelected = ()
                            playerClicks = []
                            moveMade = False
                            animate = False
                            gameOver = False
                            whiteTime = selectedTimeLimit
                            blackTime = selectedTimeLimit
                            lastTime = time.time()
                            timerStarted = False
                    
                    elif not gameOver and humanTurn and col < 8 and row < 8:
                        if sqSelected == (row, col):
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for validMove in validMoves:
                                if move == validMove:
                                    move = validMove
                                    break
                            
                            if move in validMoves:
                                # Start timer on first move
                                if not timerStarted and timerEnabled:
                                    timerStarted = True
                                    lastTime = time.time()
                                
                                if move.isPawnPromotion:
                                    showingPromotion = True
                                    gs.makeMove(move)
                                    moveMade = True
                                else:
                                    gs.makeMove(move)
                                    moveMade = True
                                    animate = True
                                
                                playMoveSound(move, gs, sounds)
                                sqSelected = ()
                                playerClicks = []
                            else:
                                if sounds:
                                    sounds["illegal"].play()
                                playerClicks = [sqSelected]
                
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        running = False
                    elif e.key == p.K_z and undoEnabled:
                        if len(gs.moveLog) > 0:
                            if not playerTwo:
                                if len(gs.moveLog) >= 2:
                                    gs.undoMove()
                                    gs.undoMove()
                                elif len(gs.moveLog) == 1:
                                    gs.undoMove()
                            else:
                                gs.undoMove()
                            moveMade = True
                            animate = False
                            sqSelected = ()
                            playerClicks = []
                            gameOver = False
                            # Reset timer after undo
                            if len(gs.moveLog) == 0:
                                timerStarted = False
                    
                    elif e.key == p.K_r:
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False
                        whiteTime = selectedTimeLimit
                        blackTime = selectedTimeLimit
                        lastTime = time.time()
                        timerStarted = False
            
            if not gameOver and not humanTurn and not showingPromotion:
                # Start timer on AI's first move
                if not timerStarted and timerEnabled:
                    timerStarted = True
                    lastTime = time.time()
                
                ChessAI.DEPTH = aiDifficulty
                AIMove = ChessAI.findBestMove(gs, validMoves)
                if AIMove is None:
                    AIMove = ChessAI.findRandomMove(validMoves)
                
                if AIMove and AIMove.isPawnPromotion:
                    AIMove.promotionChoice = 'Q'
                
                if AIMove:
                    gs.makeMove(AIMove)
                    moveMade = True
                    animate = True
                    playMoveSound(AIMove, gs, sounds)
            
            if moveMade and gs is not None:
                if animate and not showingPromotion:
                    animateMove(gs.moveLog[-1], screen, gs.board, clock, currentTheme)
                validMoves = gs.getValidMoves()
                moveMade = False
                animate = False
            
            if gs is not None:
                drawGameState(screen, gs, validMoves, sqSelected, currentTheme)
                drawMoveLog(screen, gs.moveLog, font)
                drawButtons(screen, font, undoEnabled)
                
                if timerEnabled:
                    drawTimer(screen, whiteTime, blackTime, gs.whiteToMove, font)
                
                drawTurnIndicator(screen, gs, font)
                
                if showingPromotion:
                    drawPromotionMenu(screen, gs.whiteToMove)
                
                if gs.checkmate:
                    gameOver = True
                    winner = 'Black' if gs.whiteToMove else 'White'
                    drawText(screen, f'{winner} wins by checkmate!')
                    if sounds and not p.mixer.get_busy():
                        sounds["end"].play()
                elif gs.stalemate:
                    gameOver = True
                    drawText(screen, 'Stalemate - Draw!')
                    if sounds and not p.mixer.get_busy():
                        sounds["end"].play()
                elif timerEnabled and (whiteTime <= 0 or blackTime <= 0):
                    gameOver = True
                    winner = 'Black' if whiteTime <= 0 else 'White'
                    drawText(screen, f'{winner} wins on time!')
                    if sounds and not p.mixer.get_busy():
                        sounds["end"].play()
            else:
                gameState = "menu"
            
            clock.tick(MAX_FPS)
            p.display.flip()

if __name__ == "__main__":
    main()