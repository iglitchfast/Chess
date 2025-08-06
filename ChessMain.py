import pygame as p
import ChessEngine, ChessAI

WIDTH = HEIGHT = 512
DIMENSION = 8  # 8x8 board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
PANEL_WIDTH = 200

def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
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
    sounds["start"].play()

    screen = p.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False

    load_images()
    font = p.font.SysFont("Arial", 18, False, False)
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False

    # Mode selection
    playerOne = True
    playerTwo = False
    selectingMode = True
    aiButton = p.Rect(WIDTH + 20, HEIGHT//2 - 60, 160, 40)
    pvpButton = p.Rect(WIDTH + 20, HEIGHT//2 + 20, 160, 40)

    while running:
        if selectingMode:
            screen.fill(p.Color("white"))
            drawBoard(screen)
            drawButtonsMode(screen, font, aiButton, pvpButton)
            p.display.flip()
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    if aiButton.collidepoint(location):
                        playerOne = True
                        playerTwo = False
                        selectingMode = False
                    elif pvpButton.collidepoint(location):
                        playerOne = True
                        playerTwo = True
                        selectingMode = False
            continue

        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if WIDTH <= location[0]:  # Right panel click
                    if undoRect.collidepoint(location):
                        if not playerTwo:
                            if len(gs.moveLog) >= 2:
                                gs.undoMove()
                                gs.undoMove()
                            elif len(gs.moveLog) == 1:
                                gs.undoMove()
                        else:
                            if len(gs.moveLog) >= 1:
                                gs.undoMove()

                        moveMade = True
                        animate = False
                        sqSelected = ()
                        playerClicks = []
                        gameOver = False

                    elif resetRect.collidepoint(location):
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False
                elif not gameOver and humanTurn:
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                            animate = True

                            if move.isCastleMove:
                                sounds["castle"].play()
                            elif move.pieceCaptured != "--":
                                sounds["capture"].play()
                            elif getattr(move, 'isPawnPromotion', False):
                                sounds["promote"].play()
                            elif gs.inCheck():
                                sounds["check"].play()
                            else:
                                sounds["move"].play()

                            sqSelected = ()
                            playerClicks = []
                        else:
                            sounds["illegal"].play()
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    if not playerTwo:
                        if len(gs.moveLog) >= 2:
                            gs.undoMove()
                            gs.undoMove()
                        elif len(gs.moveLog) == 1:
                            gs.undoMove()
                    else:
                        if len(gs.moveLog) >= 1:
                            gs.undoMove()

                    moveMade = True
                    animate = False
                    sqSelected = ()
                    playerClicks = []
                    gameOver = False
                elif e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        if not gameOver and not humanTurn:
            AIMove = ChessAI.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

            if AIMove.isCastleMove:
                sounds["castle"].play()
            elif AIMove.pieceCaptured != "--":
                sounds["capture"].play()
            elif getattr(AIMove, 'isPawnPromotion', False):
                sounds["promote"].play()
            elif gs.inCheck():
                sounds["check"].play()
            else:
                sounds["move"].play()

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)
        drawMoveLog(screen, gs.moveLog, font)
        undoRect, resetRect = drawButtons(screen, font)

        if gs.checkmate:
            gameOver = True
            drawText(screen, 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate')
            if not p.mixer.get_busy():
                sounds["end"].play()
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')
            if not p.mixer.get_busy():
                sounds["end"].play()

        clock.tick(MAX_FPS)
        p.display.flip()

def drawButtonsMode(screen, font, aiRect, pvpRect):
    p.draw.rect(screen, p.Color('lightblue'), aiRect)
    p.draw.rect(screen, p.Color('lightgreen'), pvpRect)
    aiText = font.render('Play vs AI', True, p.Color('black'))
    pvpText = font.render('Player vs Player', True, p.Color('black'))
    screen.blit(aiText, (aiRect.x + 30, aiRect.y + 10))
    screen.blit(pvpText, (pvpRect.x + 10, pvpRect.y + 10))



def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, game_state, valid_moves, square_selected):
    if (len(game_state.moveLog)) > 0:
        last_move = game_state.moveLog[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.endCol * SQ_SIZE, last_move.endRow * SQ_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == ('w' if game_state.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, moveLog, font):
    logRect = p.Rect(WIDTH, 20, PANEL_WIDTH, HEIGHT - 100)
    p.draw.rect(screen, p.Color("lightyellow"), logRect)
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        whiteMove = moveLog[i].getChessNotation()
        blackMove = moveLog[i + 1].getChessNotation() if i + 1 < len(moveLog) else ""
        moveTexts.append(f"{i//2 + 1}. {whiteMove} {blackMove}")
    moveY = 25
    for idx, text in enumerate(moveTexts[-20:]):
        color = p.Color("black") if idx % 2 == 0 else p.Color("blue")
        textObj = font.render(text, True, color)
        screen.blit(textObj, (WIDTH + 10, moveY))
        moveY += 20

def drawButtons(screen, font):
    undoRect = p.Rect(WIDTH + 20, HEIGHT - 70, 75, 30)
    resetRect = p.Rect(WIDTH + 105, HEIGHT - 70, 75, 30)
    p.draw.rect(screen, p.Color('lightcoral'), undoRect)
    p.draw.rect(screen, p.Color('lightgreen'), resetRect)
    undoText = font.render('Undo', True, p.Color('black'))
    resetText = font.render('Reset', True, p.Color('black'))
    screen.blit(undoText, (undoRect.x + 12, undoRect.y + 5))
    screen.blit(resetText, (resetRect.x + 12, resetRect.y + 5))
    return undoRect, resetRect

def animateMove(move, screen, board, clock):
    colors = [p.Color("white"), p.Color("gray")]
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, True, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH + PANEL_WIDTH, HEIGHT).move(WIDTH // 2 - textObject.get_width() // 2, HEIGHT // 2 - textObject.get_height() // 2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()
