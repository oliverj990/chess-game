import pygame
import math
from piece_init import Piece, PieceType, pieces, pos_to_coords, coords_to_pos, KNIGHT, PAWN, KING
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


# Draw checkered board given two colours.
def draw_board(game_window, colour1, colour2):
    
    # Fill whole window in one colour.
    game_window.fill(colour1)

    # Draw boxes in other colour in half of the squares.
    for i in range(8):
        for j in range(4):
            pygame.draw.rect(game_window, colour2, (110 * i, 770 - 220 * j - (i % 2) * 110, 110, 110))



def get_piece_at(position, piece_list):
    for piece in piece_list:
        if piece.position == position:
            return piece
    return None



def combine_rel_and_fixed_pos(rel_pos, piece):
    fixed_pos = piece.position
    if piece.colour == 1:
        combined_pos = (fixed_pos[0] + rel_pos[0], fixed_pos[1] + rel_pos[1])
    else:
        combined_pos = (fixed_pos[0] - rel_pos[0], fixed_pos[1] - rel_pos[1])
    return combined_pos


# Get possible moves of a piece given a complete board configuration.
def get_legal_moves(piece, piece_list):
    piece_colour = piece.colour
    all_possible_moves = list(piece.moves())
    illegal_moves = []
    legal_moves = []

    # Add all captures to illegal_moves list (captures of both colours)
    for possible_move in all_possible_moves:
        if get_piece_at(combine_rel_and_fixed_pos(possible_move, piece), piece_list) != None:
            illegal_moves.append(possible_move)

    # Add all multiples of captures to illegal_moves list
    if piece.type != KNIGHT:
        temp_fixed_list = list(illegal_moves)
        for illegal_move in temp_fixed_list:
            x, y = 0, 0
            if illegal_move[0] > 0:
                x = 1
            elif illegal_move[0] < 0:
                x = -1
            if illegal_move[1] > 0:
                y = 1
            elif illegal_move[1] < 0:
                y = -1
            for i in range(7):
                j = i + 1
                move_multiple = (illegal_move[0] + j * x, illegal_move[1] + j * y)
                illegal_moves.append(move_multiple)
    
    # Remove legal (opposite-colour) captures from illegal_moves
    for possible_move in all_possible_moves:
        if get_piece_at(combine_rel_and_fixed_pos(possible_move, piece), piece_list) != None:
            if get_piece_at(combine_rel_and_fixed_pos(possible_move, piece), piece_list).colour != piece_colour:
                while possible_move in illegal_moves:
                    illegal_moves.remove(possible_move)

    # Add all possible moves which are not in illegal_moves to legal_moves
    for possible_move in all_possible_moves:
        if possible_move not in illegal_moves:
            legal_move = combine_rel_and_fixed_pos(possible_move, piece)
            if legal_move[0] in range(8) and legal_move[1] in range(8):
                legal_moves.append(legal_move)

    return legal_moves



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
                    print(get_legal_moves(clicked_piece, pieces))
                    if clicked_piece.colour == whose_turn:
                        selected_piece = clicked_piece
                # Play move with selected piece.
                elif clicked_piece != None and selected_piece != None and clicked_pos not in get_legal_moves(selected_piece, pieces):
                    print(get_legal_moves(clicked_piece, pieces))
                    if clicked_piece.colour == whose_turn:
                        selected_piece = clicked_piece
                elif selected_piece != None and clicked_pos in get_legal_moves(selected_piece, pieces):
                    selected_piece.hasMoved = True
                    selected_piece.position = clicked_pos
                    selected_piece = None
                    whose_turn = 1 - whose_turn
                    if clicked_piece != None:
                        pieces.remove(clicked_piece)
        
        pygame.display.update()
    
    pygame.quit()



main()
