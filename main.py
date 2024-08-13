import pygame
import math
pygame.init()

WIDTH, HEIGHT = 880, 880
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
# last move played
# selected piece
# game finished/result

#COLOURS
dark_brown = (123, 69, 51) #light dull beige
light_brown = (185, 122, 87) #dark dull beige/brown



class PieceType:

    def __init__(self, name, value, moves):
        self.name = name
        self.value = value
        self.moves = moves



PAWN = PieceType("PAWN", "1", [
    (0, 1), (0, 2), (1, 1), (-1, 1), 
])
ROOK = PieceType("ROOK", "1", [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), 
    (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), 
])
KNIGHT = PieceType("KNIGHT", "1", [
    (2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2), 
])
BISHOP = PieceType("BISHOP", "1", [
    (1, 1),  (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1),  (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), 
    (1, -1),  (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, 1),  (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), 
])
QUEEN = PieceType("QUEEN", "1", [
    (1, 1),  (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1),  (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), 
    (1, -1),  (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, 1),  (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), 
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), 
    (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), 
])
KING = PieceType("KING", "1", [
    (0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1), (2, 0), (-2, 0)
])



class Piece:
    
    def __init__(self, name, colour, type, position):
        self.name = name
        self.colour = colour
        self.type = type
        self.position = position

    def draw(self, win):
        coords = pos_to_coords(self.position)
        img_loc = r"piece_imgs\\"
        if self.colour == 1:
            img_loc += "white_"
        else:
            img_loc += "black_"
        img_loc += self.type.name.lower()
        img_loc += "_110_x_110.png"
        piece_img = pygame.image.load(img_loc).convert_alpha()
        #pygame.draw.circle(win, (255 * self.colour, 255 * self.colour, 255 * self.colour), coords, 40)
        win.blit(piece_img, coords)
    
    def moves(self):
        return self.type.moves



pieces = [
    Piece("WhiteAPawn", 1, PAWN, (0, 1)),
    Piece("WhiteBPawn", 1, PAWN, (1, 1)),
    Piece("WhiteCPawn", 1, PAWN, (2, 1)),
    Piece("WhiteDPawn", 1, PAWN, (3, 1)),
    Piece("WhiteEPawn", 1, PAWN, (4, 1)),
    Piece("WhiteFPawn", 1, PAWN, (5, 1)),
    Piece("WhiteGPawn", 1, PAWN, (6, 1)),
    Piece("WhiteHPawn", 1, PAWN, (7, 1)),
    Piece("WhiteARook", 1, ROOK, (0, 0)),
    Piece("WhiteBKnight", 1, KNIGHT, (1, 0)),
    Piece("WhiteCBishop", 1, BISHOP, (2, 0)),
    Piece("WhiteQueen", 1, QUEEN, (3, 0)),
    Piece("WhiteKing", 1, KING, (4, 0)),
    Piece("WhiteFBishop", 1, BISHOP, (5, 0)),
    Piece("WhiteGKnight", 1, KNIGHT, (6, 0)),
    Piece("WhiteHRook", 1, ROOK, (7, 0)),
    Piece("BlackAPawn", 0, PAWN, (0, 6)),
    Piece("BlackBPawn", 0, PAWN, (1, 6)),
    Piece("BlackCPawn", 0, PAWN, (2, 6)),
    Piece("BlackDPawn", 0, PAWN, (3, 6)),
    Piece("BlackEPawn", 0, PAWN, (4, 6)),
    Piece("BlackFPawn", 0, PAWN, (5, 6)),
    Piece("BlackGPawn", 0, PAWN, (6, 6)),
    Piece("BlackHPawn", 0, PAWN, (7, 6)),
    Piece("BlackARook", 0, ROOK, (0, 7)),
    Piece("BlackBKnight", 0, KNIGHT, (1, 7)),
    Piece("BlackCBishop", 0, BISHOP, (2, 7)),
    Piece("BlackDQueen", 0, QUEEN, (3, 7)),
    Piece("BlackEKing", 0, KING, (4, 7)),
    Piece("BlackFBishop", 0, BISHOP, (5, 7)),
    Piece("BlackGKnight", 0, KNIGHT, (6, 7)),
    Piece("BlackHRook", 0, ROOK, (7, 7)),
]


# Draw checkered board given two colours.
def draw_board(game_window, colour1, colour2):
    
    # Fill whole window in one colour.
    game_window.fill(colour1)

    # Draw boxes in other colour in half of the squares.
    for i in range(8):
        for j in range(4):
            pygame.draw.rect(game_window, colour2, (110 * i, 770 - 220 * j - (i % 2) * 110, 110, 110))


# Translate board coordinates to board position.
def coords_to_pos(coords):
    (x, y) = coords
    c = math.floor(x/110)
    r = 7 - math.floor(y/110)
    position = (c , r)
    return position


# Translate board position to board coordinates.
def pos_to_coords(position):
    (c, r) = position
    x = c * 110
    y = 770 - r * 110
    coords = (x, y)
    return coords



def get_piece_at(position, piece_list):
    for piece in piece_list:
        if piece.position == position:
            return piece
    return None



def remove_self_and_multiples(list_item, start_list):
    tuple_list = list(start_list)
    higher_multiples = []
    for i in range(7):
        if list_item[0] != 0 and list_item[1] != 0:
            higher_multiples.append((i + list_item[0], i + list_item[1]))
        elif list_item[0] != 0 and list_item[1] == 0:
            higher_multiples.append((i + list_item[0], 0))
        elif list_item[0] == 0 and list_item[1] != 0:
            higher_multiples.append((0, i + list_item[1]))
    
    for higher_multiple in higher_multiples:
        if higher_multiple in tuple_list:
            tuple_list.remove(higher_multiple)

    return tuple_list


# Get possible moves of a piece given a complete board configuration.
def get_possible_moves(piece, piece_list):
    piece_pos = piece.position
    possible_moves = list(piece.moves())

    for i in range(len(possible_moves)):
        possible_move = possible_moves[i]
        if piece.colour == 1:
            possible_moves[i] = (piece_pos[0] + possible_move[0], piece_pos[1] + possible_move[1])
        else:
            possible_moves[i] = (piece_pos[0] - possible_move[0], piece_pos[1] - possible_move[1])

    moves_on_board = []
    allowed_moves = []

    while len(possible_moves) > 0:
        move_to_check = possible_moves[0]
        piece_at_move = get_piece_at(move_to_check, piece_list)
        if move_to_check[0] not in [0, 1, 2, 3, 4, 5, 6, 7, ] or move_to_check[1] not in [0, 1, 2, 3, 4, 5, 6, 7, ]:
            possible_moves.remove(move_to_check)
        if move_to_check in possible_moves:
            possible_moves.remove(move_to_check)
            moves_on_board.append(move_to_check)

    while len(moves_on_board) > 0:
        move_to_check = moves_on_board[0]
        piece_at_move = get_piece_at(move_to_check, piece_list)
        if piece_at_move != None:
            if piece_at_move.colour == piece.colour:
                moves_on_board = remove_self_and_multiples(move_to_check, moves_on_board)
            else:
                moves_on_board = remove_self_and_multiples(move_to_check, moves_on_board)
                allowed_moves.append(move_to_check)
        if move_to_check in moves_on_board:
            moves_on_board.remove(move_to_check)
            allowed_moves.append(move_to_check)

    return allowed_moves



def main():
    run = True
    clock = pygame.time.Clock()
    selected_piece = None
    whose_turn = 1

    while run:
        clock.tick(60)

        draw_board(WIN, dark_brown, light_brown)

        for piece in pieces:
            piece.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_coords = pygame.mouse.get_pos()
                clicked_pos = coords_to_pos(clicked_coords)
                clicked_piece = get_piece_at(clicked_pos, pieces)
                
                # Select a piece.
                if clicked_piece != None and selected_piece == None:
                    print(get_possible_moves(clicked_piece, pieces))
                    if clicked_piece.colour == whose_turn:
                        selected_piece = clicked_piece
                # Play move with selected piece.
                elif clicked_piece != None and selected_piece != None and clicked_pos not in get_possible_moves(selected_piece, pieces):
                    print(get_possible_moves(clicked_piece, pieces))
                    if clicked_piece.colour == whose_turn:
                        selected_piece = clicked_piece
                elif selected_piece != None and clicked_pos in get_possible_moves(selected_piece, pieces):
                    selected_piece.position = clicked_pos
                    selected_piece = None
                    whose_turn = 1 - whose_turn
                    if clicked_piece != None:
                        pieces.remove(clicked_piece)
        
        pygame.display.update()
    
    pygame.quit()



main()
