import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3.3, "N": 3.2, "p": 1}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 3


pst = {
    'p': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 2, 3, 3, 2, 1, 1],
        [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
        [0.5, 1, 1, -2, -2, 1, 1, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    'N': [
        [-5, -4, -3, -3, -3, -3, -4, -5],
        [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
        [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
        [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
        [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
        [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
        [-4, -2, 0, 0, 0, 0, -2, -4],
        [-5, -4, -3, -3, -3, -3, -4, -5]
    ],
    'B': [
        [-2, -1, -1, -1, -1, -1, -1, -2],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
        [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
        [-1, 0, 1, 1, 1, 1, 0, -1],
        [-1, 1, 1, 1, 1, 1, 1, -1],
        [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
        [-2, -1, -1, -1, -1, -1, -1, -2]
    ],
    'R': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0.5, 1, 1, 1, 1, 1, 1, 0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [0, 0, 0, 0.5, 0.5, 0, 0, 0]
    ],
    'Q': [
        [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
        [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
        [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
        [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
        [-1, 0, 0.5, 0, 0, 0, 0, -1],
        [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
    ],
    'K': [
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-2, -3, -3, -4, -4, -3, -3, -2],
        [-1, -2, -2, -2, -2, -2, -2, -1],
        [2, 2, 0, 0, 0, 0, 2, 2],
        [2, 3, 1, 0, 0, 1, 3, 2]
    ]
}


pst_endgame_king = [
    [-5, -4, -3, -2, -2, -3, -4, -5],
    [-3, -2, -1, 0, 0, -1, -2, -3],
    [-3, -1, 2, 3, 3, 2, -1, -3],
    [-3, -1, 3, 4, 4, 3, -1, -3],
    [-3, -1, 3, 4, 4, 3, -1, -3],
    [-3, -1, 2, 3, 3, 2, -1, -3],
    [-3, -3, 0, 0, 0, 0, -3, -3],
    [-5, -3, -3, -3, -3, -3, -3, -5]
]

transpositionTable = {}

def findBestMove(gs, validMoves):
    global nextMove, transpositionTable
    nextMove = None
    random.shuffle(validMoves)
    transpositionTable.clear()
    alphaBeta(gs, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove

def alphaBeta(gs, depth, alpha, beta, turnMultiplier):
    global nextMove, transpositionTable
    
    # Check transposition table
    boardHash = hashBoard(gs)
    if boardHash in transpositionTable and transpositionTable[boardHash][1] >= depth:
        return transpositionTable[boardHash][0]
    
    if depth == 0:
        score = turnMultiplier * evaluateBoard(gs)
        transpositionTable[boardHash] = (score, 0)
        return score
    
    maxScore = -CHECKMATE
    validMoves = gs.getValidMoves()
    
    if len(validMoves) == 0:
        if gs.inCheck():
            return -CHECKMATE
        else:
            return STALEMATE
    
    orderMoves(gs, validMoves)
    
    for move in validMoves:
        gs.makeMove(move)
        score = -alphaBeta(gs, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()
        
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    
    transpositionTable[boardHash] = (maxScore, depth)
    return maxScore

def orderMoves(gs, moves):
    moveScores = []
    for move in moves:
        score = 0
        # Prioritize captures
        if move.pieceCaptured != '--':
            score += 10 * pieceScore.get(move.pieceCaptured[1], 0) - pieceScore.get(move.pieceMoved[1], 0)
        
        # Prioritize pawn promotion
        if move.isPawnPromotion:
            score += 8
        
        # Prioritize castling
        if move.isCastleMove:
            score += 2
        
        # Prioritize center control
        if 2 <= move.endRow <= 5 and 2 <= move.endCol <= 5:
            score += 0.5
        
        moveScores.append((score, move))
    
    moveScores.sort(reverse=True, key=lambda x: x[0])
    moves[:] = [move for _, move in moveScores]

def hashBoard(gs):
    """Simple board hashing for transposition table"""
    return str(gs.board) + str(gs.whiteToMove)

def evaluateBoard(gs):
    if gs.checkmate:
        return -CHECKMATE if gs.whiteToMove else CHECKMATE
    if gs.stalemate:
        return STALEMATE
    
    score = 0
    materialCount = 0
    
    for r in range(8):
        for c in range(8):
            piece = gs.board[r][c]
            if piece == '--':
                continue
            
            value = pieceScore.get(piece[1], 0)
            materialCount += value
            
            
            isEndgame = materialCount < 20
            
            
            if piece[1] == 'K' and isEndgame:
                pstBonus = pst_endgame_king[r][c] if piece[0] == 'w' else pst_endgame_king[7-r][c]
            elif piece[1] in pst:
                if piece[1] == 'p':
                    pstBonus = pst[piece[1]][r][c] if piece[0] == 'w' else pst[piece[1]][7-r][c]
                else:
                    pstBonus = pst[piece[1]][r][c] if piece[0] == 'w' else pst[piece[1]][7-r][c]
            else:
                pstBonus = 0
            
            if piece[0] == 'w':
                score += value + pstBonus * 0.1
            else:
                score -= value + pstBonus * 0.1
    
    
    score += kingSafety(gs) * 0.5
    score += mobility(gs) * 0.05
    score += centerControl(gs) * 0.3
    score += pawnStructure(gs) * 0.2
    score += pieceActivity(gs) * 0.1
    
    return score

def kingSafety(gs):
    """Evaluate king safety"""
    kingPos = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation
    row, col = kingPos
    shield = 0
    
    
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                piece = gs.board[nr][nc]
                if piece != '--' and piece[0] == ('w' if gs.whiteToMove else 'b'):
                    shield += 1
    
    
    if row in [3, 4] and col in [3, 4]:
        shield -= 2
    
    return shield if gs.whiteToMove else -shield

def mobility(gs):
    """Count number of legal moves"""
    numMoves = len(gs.getValidMoves())
    return numMoves if gs.whiteToMove else -numMoves

def centerControl(gs):
    """Reward controlling center squares"""
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    extended_center = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 5), 
                       (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]
    
    score = 0
    for r, c in center_squares:
        piece = gs.board[r][c]
        if piece != '--':
            if piece[0] == 'w':
                score += 0.5
            else:
                score -= 0.5
    
    for r, c in extended_center:
        piece = gs.board[r][c]
        if piece != '--':
            if piece[0] == 'w':
                score += 0.2
            else:
                score -= 0.2
    
    return score

def pawnStructure(gs):
    """Evaluate pawn structure"""
    score = 0
    
    
    for c in range(8):
        white_pawns = []
        black_pawns = []
        for r in range(8):
            if gs.board[r][c] == 'wp':
                white_pawns.append(r)
            elif gs.board[r][c] == 'bp':
                black_pawns.append(r)
        
        if len(white_pawns) > 1:
            score -= 0.5 * (len(white_pawns) - 1)
        if len(black_pawns) > 1:
            score += 0.5 * (len(black_pawns) - 1)
    
    
    for c in range(8):
        for r in range(8):
            if gs.board[r][c][1] == 'p':
                hasSupport = False
                for dc in [-1, 1]:
                    if 0 <= c + dc < 8:
                        for dr in range(8):
                            if gs.board[dr][c+dc][1] == 'p' and gs.board[dr][c+dc][0] == gs.board[r][c][0]:
                                hasSupport = True
                                break
                
                if not hasSupport:
                    if gs.board[r][c][0] == 'w':
                        score -= 0.3
                    else:
                        score += 0.3
    
    return score

def pieceActivity(gs):
    """Reward pieces on active squares"""
    score = 0
    
    for r in range(8):
        for c in range(8):
            piece = gs.board[r][c]
            if piece == '--':
                continue
            
            
            if piece[1] == 'p':
                if piece[0] == 'w' and r < 4:
                    score += (6 - r) * 0.1
                elif piece[0] == 'b' and r > 3:
                    score -= (r - 1) * 0.1
            
            
            if piece[0] == 'w' and r != 7 and piece[1] in ['N', 'B']:
                score += 0.3
            elif piece[0] == 'b' and r != 0 and piece[1] in ['N', 'B']:
                score -= 0.3
    
    return score

def findRandomMove(validMoves):
    """Fallback random move"""
    return validMoves[random.randint(0, len(validMoves) - 1)] if validMoves else None