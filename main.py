import pygame
from piece_init import pieces, coords_to_pos

pygame.init()
WIDTH, HEIGHT = 880, 880
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
font = pygame.font.SysFont(None, 25)

# Board background colours
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
    
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for i in range(4):
        j = i + 1
        dark_letter = font.render(alphabet[2*i], True, dark_brown)
        light_letter = font.render(alphabet[2*i + 1], True, light_brown)
        game_window.blit(dark_letter, (3 + 220 * i, 863))
        game_window.blit(light_letter, (113 + 220 * i, 863))
        dark_number = font.render(str(8 - 2*i), True, dark_brown)
        light_number = font.render(str(7 - 2*i), True, light_brown)
        game_window.blit(dark_number, (867, 3 + 220 * i))
        game_window.blit(light_number, (867, 113 + 220 * i))



# Get piece at given square
def get_piece_at(position, piece_list):
    for piece in piece_list:
        if piece.position == position:
            return piece
    return None


# Combine relative position (move) with current piece position
def combine_rel_and_fixed_pos(rel_pos, piece):
    fixed_pos = piece.position
    if piece.colour == 1:
        combined_pos = (fixed_pos[0] + rel_pos[0], fixed_pos[1] + rel_pos[1])
    else:
        combined_pos = (fixed_pos[0] + rel_pos[0], fixed_pos[1] - rel_pos[1])
    return combined_pos


# Check if white or black is in check
def board_in_check(piece_list, last_move):

    black_king_pos = (8, 8)
    white_king_pos = (8, 8)

    for piece in piece_list:
        if piece.name == "BlackKing":
            black_king_pos = piece.position
        if piece.name == "WhiteKing":
            white_king_pos = piece.position

    for piece in piece_list:
        # Black in check
        if piece.colour == 1:
            if black_king_pos in get_legal_moves(piece, piece_list, last_move):
                return 0
        # White in check
        else:
            if white_king_pos in get_legal_moves(piece, piece_list, last_move):
                return 1
    return 42


# Check if white or black is in checkmate
def board_in_checkmate(piece_list, last_move):
    output = True
    current_check = board_in_check(piece_list, last_move)
    if current_check == 42:
        return False
    # Iterate through all moves of all pieces
    for piece in piece_list:
        if piece.colour != current_check:
            continue
        legal_moves = get_legal_moves(piece, piece_list, last_move)
        start_pos = piece.position
        for legal_move in legal_moves:
            new_square_piece = get_piece_at(legal_move, piece_list)
            if new_square_piece != None:
                piece_list.remove(new_square_piece)
            piece.position = legal_move
            if board_in_check(piece_list, last_move) == 42:
                output = False
            piece.position = start_pos
            if new_square_piece != None:
                piece_list.append(new_square_piece)
    return output


# Check if board is in stalemate
def board_in_stalemate(piece_list, whose_turn, last_move):

    for piece in piece_list:
        if piece.colour != whose_turn:
            continue
        legal_moves = get_legal_moves(piece, piece_list, last_move)
        if len(legal_moves) > 0:
            return False

    return True


# Convert position to chess square notation
def pos_numbers_to_letters(pos):
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]
    return alphabet[pos[0]] + str(pos[1] + 1)


# Get possible moves of a piece given a complete board configuration.
def get_legal_moves(piece, piece_list, last_move):
    piece_pos = piece.position
    piece_colour = piece.colour
    all_possible_moves = list(piece.moves())
    illegal_moves = []
    legal_moves = []

    # Add all captures to illegal_moves list (captures of both colours)
    for possible_move in all_possible_moves:
        if get_piece_at(combine_rel_and_fixed_pos(possible_move, piece), piece_list) != None:
            illegal_moves.append(possible_move)

    # Add all multiples of captures to illegal_moves list
    if piece.type.name != "KNIGHT":
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
                if possible_move in illegal_moves:
                    illegal_moves.remove(possible_move)

    # Add all possible moves which are not in illegal_moves to legal_moves
    for possible_move in all_possible_moves:
        if possible_move not in illegal_moves:
            legal_move = combine_rel_and_fixed_pos(possible_move, piece)
            if legal_move[0] in range(8) and legal_move[1] in range(8):
                legal_moves.append(legal_move)

    # Check for castling
    if piece.type.name == "KING":

        # Check king hasn't moved
        if piece.hasMoved:
            if combine_rel_and_fixed_pos((2, 0), piece) in legal_moves:
                legal_moves.remove(combine_rel_and_fixed_pos((2, 0), piece))
            if combine_rel_and_fixed_pos((-2, 0), piece) in legal_moves:
                legal_moves.remove(combine_rel_and_fixed_pos((-2, 0), piece))

        # Check rook hasn't moved
        for rook in pieces:
            if rook.name[-5:] == "HRook" and rook.hasMoved:
                if combine_rel_and_fixed_pos((2, 0), piece) in legal_moves:
                    legal_moves.remove(combine_rel_and_fixed_pos((2, 0), piece))
            elif rook.name[-5:] == "ARook" and rook.hasMoved:
                if combine_rel_and_fixed_pos((-2, 0), piece) in legal_moves:
                    legal_moves.remove(combine_rel_and_fixed_pos((-2, 0), piece))
        
        # Check if castling would be a capture
        if get_piece_at(combine_rel_and_fixed_pos((2, 0), piece), pieces) != None:
            if combine_rel_and_fixed_pos((2, 0), piece) in legal_moves:
                legal_moves.remove(combine_rel_and_fixed_pos((2, 0), piece))
        if get_piece_at(combine_rel_and_fixed_pos((-2, 0), piece), pieces) != None:
            if combine_rel_and_fixed_pos((-2, 0), piece) in legal_moves:
                legal_moves.remove(combine_rel_and_fixed_pos((-2, 0), piece))

    # Check for weird pawn moves
    if piece.type.name == "PAWN":

        # Check for double-move
        if piece.hasMoved:
            illegal_move = combine_rel_and_fixed_pos((0, 2), piece)
            if illegal_move in legal_moves:
                legal_moves.remove(illegal_move)
        
        # Block pawn advance
        piece_in_front = get_piece_at(combine_rel_and_fixed_pos((0, 1), piece), piece_list)
        if piece_in_front != None:
            if piece_in_front.position in legal_moves:
                legal_moves.remove(piece_in_front.position)
        
        # Only allow diagonal for captures
        diagonals = [(1, 1), (-1, 1)]
        for diag_pos in diagonals:
            diag_piece = get_piece_at(combine_rel_and_fixed_pos(diag_pos, piece), piece_list)
            if diag_piece != None:
                if diag_piece.colour == piece_colour:
                    if diag_piece.position in legal_moves:
                        legal_moves.remove(diag_piece.position)
            if diag_piece == None:
                if combine_rel_and_fixed_pos(diag_pos, piece) in legal_moves:
                    legal_moves.remove(combine_rel_and_fixed_pos(diag_pos, piece))
        
        # Check for en passant
        if last_move == (combine_rel_and_fixed_pos((1, 2), piece), combine_rel_and_fixed_pos((1, 0), piece)):
            legal_moves.append(combine_rel_and_fixed_pos((1, 1), piece))
        if last_move == (combine_rel_and_fixed_pos((-1, 2), piece), combine_rel_and_fixed_pos((- 1, 0), piece)):
            legal_moves.append(combine_rel_and_fixed_pos((-1, 1), piece))

    return legal_moves



def piece_list_to_fen1(piece_list):
    fen = ""
    for i in range(8):
        fen_row = ""
        row_pieces = {}
        for j in range(8):
            row_pieces[j] = None
        for piece in piece_list:
            if piece.position[1] == i:
                row_pieces[piece.position[0]] = piece
        counter = 0
        for j in range(8):
            row_piece = row_pieces[j]
            if row_piece != None:
                piece_type = row_piece.type.name
                if piece_type == "KNIGHT":
                    piece_type = "N"
                else:
                    piece_type = piece_type[0]
                if row_piece.colour == 0: piece_type = piece_type.lower()
                if counter != 0:
                    fen_row += str(counter)
                fen_row += piece_type
                counter = 0
            elif row_piece == None:
                counter += 1
                if j == 7 and counter > 0:
                    fen_row += str(counter)
        fen = fen_row + "/" + fen
    return fen[:-1]



def fen_to_piece_list(fen):
    return



def main():
    run = True
    clock = pygame.time.Clock()
    selected_piece = None
    whose_turn = 1
    last_move = ((-1, -1,), (-2, -2))
    positions = []

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
                    if clicked_piece.colour == whose_turn:
                        selected_piece = clicked_piece
                elif clicked_piece != None and selected_piece != None and clicked_pos not in get_legal_moves(selected_piece, pieces, last_move):
                    if clicked_piece.colour == whose_turn:
                        selected_piece = clicked_piece
                # Play move with selected piece.
                elif selected_piece != None and clicked_pos in get_legal_moves(selected_piece, pieces, last_move):
                    already_check = board_in_check(pieces, last_move)
                    selected_pos = selected_piece.position

                    if clicked_piece != None:
                        pieces.remove(clicked_piece)

                    selected_piece.position = clicked_pos

                    # If in check, move is not permitted
                    if board_in_check(pieces, last_move) == whose_turn or (selected_piece.type.name == "KING" and selected_pos in ((4, 0), (4, 7)) and clicked_pos in ((6, 0), (6, 7), (2, 7), (2, 0)) and already_check == selected_piece.colour):
                        selected_piece.position = selected_pos
                        pieces.append(selected_piece)
                        if clicked_piece != None:
                            pieces.append(clicked_piece)
                    else:
                        # Move rook in case of castling
                        if selected_pos in ((4, 0), (4, 7)) and selected_piece.type.name == "KING":
                            rook_name = ""
                            rook_pos = (-1, -1)
                            if clicked_pos == (6, 0):
                                rook_name = "WhiteHRook"
                                rook_pos = (5, 0)
                            elif clicked_pos == (2, 0):
                                rook_name = "WhiteARook"
                                rook_pos = (3, 0)
                            elif clicked_pos == (6, 7):
                                rook_name = "BlackHRook"
                                rook_pos = (5, 7)
                            elif clicked_pos == (2, 7):
                                rook_name = "BlackARook"
                                rook_pos = (3, 7)
                            for rook in pieces:
                                if rook.name == rook_name:
                                    rook.position = rook_pos
                        elif selected_piece.type.name == "PAWN":
                            if last_move == (combine_rel_and_fixed_pos((0, 1), selected_piece), combine_rel_and_fixed_pos((0, -1), selected_piece)):
                                pieces.remove(get_piece_at(combine_rel_and_fixed_pos((0, -1), selected_piece), pieces))

                        #Update game data
                        last_move = (selected_pos, clicked_pos)
                        selected_piece.hasMoved = True
                        selected_piece = None
                        whose_turn = 1 - whose_turn
                        pos_fen = piece_list_to_fen1(pieces)
                        positions.append(pos_fen)

                        # Print game details
                        if whose_turn == 1:
                            print(pos_numbers_to_letters(clicked_pos) + ". It is now white's turn.")
                        else:
                            print(pos_numbers_to_letters(clicked_pos) + ". It is now black's turn.")
                        if board_in_checkmate(pieces, last_move):
                            print("Checkmate!")
                        elif board_in_check(pieces, last_move) != 42:
                            print("Check!")
                        elif board_in_stalemate(pieces, whose_turn, last_move):
                            print("Stalemate!")
                        elif positions.count(pos_fen) == 3:
                            print("Draw by repetition.")
                        
        
        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()
