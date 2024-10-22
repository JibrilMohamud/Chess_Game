import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 74)

# Load images
def load_images():
    pieces = ['b_bishop', 'b_king', 'b_knight', 'b_pawn', 'b_queen', 'b_rook', 
              'w_bishop', 'w_king', 'w_knight', 'w_pawn', 'w_queen', 'w_rook']
    images = {}
    for piece in pieces:
        images[piece] = pygame.image.load(f'images/{piece}.png')
        images[piece] = pygame.transform.scale(images[piece], (90, 90))
    return images

# Draw chessboard
def draw_board(screen):
    colors = [WHITE, BROWN]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Main
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')
images = load_images()

MAIN_GAME = 1
GAME_OVER = 2
game_state = MAIN_GAME  

# Initial piece positions
board = [['' for _ in range(8)] for _ in range(8)]
board[0] = ['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_bishop', 'b_knight', 'b_rook']
board[1] = ['b_pawn'] * 8
board[6] = ['w_pawn'] * 8
board[7] = ['w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_bishop', 'w_knight', 'w_rook']

def is_valid_move(piece, start_pos, board, turn):
    if piece[0] != turn[0]:  # Check if the piece belongs to the current turn
        return []
    # Call specific piece move functions
    if piece == 'w_pawn':
        return is_valid_pawn_move(start_pos, board, 'w')
    elif piece == 'b_pawn':  
        return is_valid_pawn_move(start_pos, board, 'b')
    elif piece[2:] == 'rook':
        return is_valid_rook_move(start_pos, board)
    elif piece[2:] == 'knight':
        return is_valid_knight_move(start_pos, board)
    elif piece[2:] == 'bishop':
        return is_valid_bishop_move(start_pos, board)
    elif piece[2:] == 'queen':
        return is_valid_queen_move(start_pos, board)
    elif piece[2:] == 'king':
        return is_valid_king_move(start_pos, board)
    return []

# Individual piece functions (return lists of possible moves)
# (Omitted for brevity—use the previous detailed versions of these functions)


def is_valid_pawn_move(start_pos, board, turn):
    start_row, start_col = start_pos
    direction = -1 if turn == 'w' else 1  # Fix the direction for white and black
    moves = []

    # Moving forward
    if 0 <= start_row + direction < 8 and board[start_row + direction][start_col] == '':
        moves.append((start_row + direction, start_col))
        
        # Check for double move from the starting position
        if (start_row == 6 and turn == 'w') or (start_row == 1 and turn == 'b'):
            if board[start_row + 2 * direction][start_col] == '':
                moves.append((start_row + 2 * direction, start_col))

    # Capturing diagonally
    for diagon in [-1, 1]:
        new_col = start_col + diagon
        if 0 <= new_col < 8 and 0 <= start_row + direction < 8:
            if board[start_row + direction][new_col] != '' and board[start_row + direction][new_col][0] != turn:
                moves.append((start_row + direction, new_col))

    return moves


def is_valid_rook_move(start_pos, board):
    start_row, start_col = start_pos
    moves = []

    # Vertical moves
    for row in range(start_row + 1, 8):
        if board[row][start_col] == '':
            moves.append((row, start_col))
        elif board[row][start_col][0] != board[start_row][start_col][0]:
            moves.append((row, start_col))
            break
        else:
            break

    for row in range(start_row - 1, -1, -1):
        if board[row][start_col] == '':
            moves.append((row, start_col))
        elif board[row][start_col][0] != board[start_row][start_col][0]:
            moves.append((row, start_col))
            break
        else:
            break

    # Horizontal moves
    for col in range(start_col + 1, 8):
        if board[start_row][col] == '':
            moves.append((start_row, col))
        elif board[start_row][col][0] != board[start_row][start_col][0]:
            moves.append((start_row, col))
            break
        else:
            break

    for col in range(start_col - 1, -1, -1):
        if board[start_row][col] == '':
            moves.append((start_row, col))
        elif board[start_row][col][0] != board[start_row][start_col][0]:
            moves.append((start_row, col))
            break
        else:
            break

    return moves

def is_valid_knight_move(start_pos, board):
    start_row, start_col = start_pos
    moves = []
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    for move in knight_moves:
        end_row, end_col = start_row + move[0], start_col + move[1]
        if 0 <= end_row < 8 and 0 <= end_col < 8:
            if board[end_row][end_col] == '' or board[end_row][end_col][0] != board[start_row][start_col][0]:
                moves.append((end_row, end_col))

    return moves

def is_valid_bishop_move(start_pos, board):
    start_row, start_col = start_pos
    moves = []

    # Diagonal moves
    for direction_row, direction_col in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        for i in range(1, 8):
            end_row, end_col = start_row + direction_row * i, start_col + direction_col * i
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if board[end_row][end_col] == '':
                    moves.append((end_row, end_col))
                elif board[end_row][end_col][0] != board[start_row][start_col][0]:
                    moves.append((end_row, end_col))
                    break
                else:
                    break

    return moves

def is_valid_queen_move(start_pos, board):
    return is_valid_rook_move(start_pos, board) + is_valid_bishop_move(start_pos, board)

def is_valid_king_move(start_pos, board):
    start_row, start_col = start_pos
    moves = []
    king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for move in king_moves:
        end_row, end_col = start_row + move[0], start_col + move[1]
        if 0 <= end_row < 8 and 0 <= end_col < 8:
            if board[end_row][end_col] == '' or board[end_row][end_col][0] != board[start_row][start_col][0]:
                moves.append((end_row, end_col))

    return moves

# ... (all movement functions remain unchanged)

def is_in_check(board, turn):
    # Find the king's position
    king_pos = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == f'{turn}_king':
                king_pos = (row, col)
                break
        if king_pos:  # Stop once the king's position is found
            break
    if not king_pos:
        return False  # If no king is found, it's not in check

    # Check for threats from opponent's pieces
    opponent = 'b' if turn == 'w' else 'w'
    for row in range(8):
        for col in range(8):
            if board[row][col] and board[row][col][0] == opponent:
                # Check if the opponent's piece can move to the king's position
                valid_moves = is_valid_move(board[row][col], (row, col), board, opponent)
                if king_pos in valid_moves:
                    return True  # King is in check
    return False  # King is not in check




def is_checkmate(board, turn):
    if not is_in_check(board, turn):
        return False
    for row in range(8):
        for col in range(8):
            if board[row][col] and board[row][col][0] == turn:
                for move in is_valid_move(board[row][col], (row, col), board, turn):
                    new_board = simulate_move(board, (row, col), move)
                    if not is_in_check(new_board, turn):
                        return False  # Found a valid move to escape check
    return True  # No valid moves to escape check, so it is checkmate


def simulate_move(board, start_pos, end_pos):
    new_board = [row[:] for row in board]  # Make a deep copy of the board
    piece = new_board[start_pos[0]][start_pos[1]]
    new_board[start_pos[0]][start_pos[1]] = ''
    new_board[end_pos[0]][end_pos[1]] = piece
    return new_board

turn = 'w'  # 'w' for white, 'b' for black
start_pos = None  # To track the selected piece's position

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # Check if a key was pressed
            if event.key == pygame.K_RETURN and game_state == GAME_OVER:
                game_state = MAIN_GAME
                board = [['' for _ in range(8)] for _ in range(8)]
                board[0] = ['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_bishop', 'b_knight', 'b_rook']
                board[1] = ['b_pawn'] * 8
                board[6] = ['w_pawn'] * 8
                board[7] = ['w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_bishop', 'w_knight', 'w_rook']
                turn = 'w'  # 'w' for white, 'b' for black
                start_pos = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
            if 0 <= row < 8 and 0 <= col < 8:
                if start_pos is None:
                    # First click to select a piece
                    if board[row][col] and board[row][col][0] == turn:
                        start_pos = (row, col)
                else:
                    # Second click to move the piece
                    end_pos = (row, col)
                    piece = board[start_pos[0]][start_pos[1]]
                    valid_moves = is_valid_move(piece, start_pos, board, turn)
                    if end_pos in valid_moves:
                        # Move the piece if the move is valid
                        board[end_pos[0]][end_pos[1]] = piece
                        board[start_pos[0]][start_pos[1]] = ''
                        turn = 'b' if turn == 'w' else 'w'
                    # Reset for the next move
                    start_pos = None
    if game_state == MAIN_GAME:
        draw_board(screen)
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    screen.blit(images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
        if is_checkmate(board, turn):
            game_state = GAME_OVER
            if turn == 'w':
                turn = 'Black'
            else:
                turn = 'White'
            print(f'Checkmate! {turn} wins!')
    elif game_state == GAME_OVER:
        screen.fill(BROWN)
        game_over_text = font.render("Checkmate", True, BLACK)
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - 50))
        result_text = font.render(f"{turn} wins", True, BLACK)
        screen.blit(result_text, ((WIDTH - result_text.get_width()) // 2, HEIGHT // 2))
        restart_text = font.render("Press Enter to Restart", True, BLACK)
        screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
