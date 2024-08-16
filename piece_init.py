import pygame
import math


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
    
    def __init__(self, name, colour, type, position, hasMoved):
        self.name = name
        self.colour = colour
        self.type = type
        self.position = position
        self.hasMoved = hasMoved

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
        win.blit(piece_img, coords)
    
    def moves(self):
        return self.type.moves



pieces = [
    Piece("WhiteAPawn", 1, PAWN, (0, 1), False),
    Piece("WhiteBPawn", 1, PAWN, (1, 1), False),
    Piece("WhiteCPawn", 1, PAWN, (2, 1), False),
    Piece("WhiteDPawn", 1, PAWN, (3, 1), False),
    Piece("WhiteEPawn", 1, PAWN, (4, 1), False),
    Piece("WhiteFPawn", 1, PAWN, (5, 1), False),
    Piece("WhiteGPawn", 1, PAWN, (6, 1), False),
    Piece("WhiteHPawn", 1, PAWN, (7, 1), False),
    Piece("WhiteARook", 1, ROOK, (0, 0), False),
    Piece("WhiteBKnight", 1, KNIGHT, (1, 0), False),
    Piece("WhiteCBishop", 1, BISHOP, (2, 0), False),
    Piece("WhiteQueen", 1, QUEEN, (3, 0), False),
    Piece("WhiteKing", 1, KING, (4, 0), False),
    Piece("WhiteFBishop", 1, BISHOP, (5, 0), False),
    Piece("WhiteGKnight", 1, KNIGHT, (6, 0), False),
    Piece("WhiteHRook", 1, ROOK, (7, 0), False),
    Piece("BlackAPawn", 0, PAWN, (0, 6), False),
    Piece("BlackBPawn", 0, PAWN, (1, 6), False),
    Piece("BlackCPawn", 0, PAWN, (2, 6), False),
    Piece("BlackDPawn", 0, PAWN, (3, 6), False),
    Piece("BlackEPawn", 0, PAWN, (4, 6), False),
    Piece("BlackFPawn", 0, PAWN, (5, 6), False),
    Piece("BlackGPawn", 0, PAWN, (6, 6), False),
    Piece("BlackHPawn", 0, PAWN, (7, 6), False),
    Piece("BlackARook", 0, ROOK, (0, 7), False),
    Piece("BlackBKnight", 0, KNIGHT, (1, 7), False),
    Piece("BlackCBishop", 0, BISHOP, (2, 7), False),
    Piece("BlackDQueen", 0, QUEEN, (3, 7), False),
    Piece("BlackEKing", 0, KING, (4, 7), False),
    Piece("BlackFBishop", 0, BISHOP, (5, 7), False),
    Piece("BlackGKnight", 0, KNIGHT, (6, 7), False),
    Piece("BlackHRook", 0, ROOK, (7, 7), False),
]
