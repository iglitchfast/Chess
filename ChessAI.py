import random

# Scores for each piece (excluding King in eval since checkmate handles it)
pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3.1, "N": 3, "p": 1}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 3

# Piece-Square Tables (just for p and N for now, you can add more)
pst = {
    'p': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, -5, -5, 5, 5, 5],
        [1, 1, 2, 3, 3, 2, 1, 1],
        [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
        [0.5, 1, 1, -2, -2, 1, 1, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    'N': [
        [-5, -4, -3, -3, -3, -3, -4, -5],
        [-4, -2, 0, 0, 0, 0, -2, -4],
        [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
        [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
        [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
        [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
        [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
        [-5, -4, -3, -3, -3, -3, -4, -5]
    ],
    # Add more for B, R, Q, K if desired
}

# Top-level AI move finder
def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)  # To vary gameplay slightly
    alphaBeta(gs, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove

# Alpha-Beta Minimax function
def alphaBeta(gs, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * evaluateBoard(gs)
    
    maxScore = -CHECKMATE
    validMoves = gs.getValidMoves()
    orderMoves(validMoves)
    
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
            break  # Beta Cutoff
    return maxScore

# Move ordering by capture priority
def orderMoves(moves):
    moves.sort(key=lambda m: 0 if m.pieceCaptured == '--' else pieceScore.get(m.pieceCaptured[1], 0), reverse=True)

# Evaluation function using material, position, king safety, and mobility
def evaluateBoard(gs):
    board = gs.board
    score = 0
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == '--':
                continue
            value = pieceScore.get(piece[1], 0)
            pstBonus = pst[piece[1]][r][c] if piece[1] in pst else 0
            if piece[0] == 'w':
                score += value + pstBonus
            else:
                # For black pawns, mirror the PST vertically
                mirrorBonus = pst[piece[1]][7 - r][c] if piece[1] in pst and piece[1] == 'p' else pstBonus
                score -= value + mirrorBonus

    score += kingSafety(gs)
    score += mobility(gs)
    return score

# Bonus for pieces around king
def kingSafety(gs):
    kingPos = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation
    row, col = kingPos
    shield = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                piece = gs.board[nr][nc]
                if piece != '--' and piece[0] == ('w' if gs.whiteToMove else 'b'):
                    shield += 0.1
    return shield if gs.whiteToMove else -shield

# Mobility = number of valid moves
def mobility(gs):
    numMoves = len(gs.getValidMoves())
    return numMoves * 0.1 if gs.whiteToMove else -numMoves * 0.1

# Optional: Fallback random move (you can still use this if needed)
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]
