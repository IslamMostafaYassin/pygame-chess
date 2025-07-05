from settings import *


class Piece(pygame.sprite.Sprite):
    DIRECTIONS = []

    def __init__(self, image, tile, color, board, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center=tile.rect.center)
        self.color = color
        self.tile = tile
        self.board = board
        self.first_move = True

    def get_legal_moves(self):

        self.legal_moves = []
        for similar_directions in self.DIRECTIONS:
            for i, j in similar_directions:
                temp_row = self.tile.row+i
                temp_colomn = self.tile.colomn+j
                if not 0 <= temp_row <= 7 or not 0 <= temp_colomn <= 7:
                    break
                potentially_doomed_piece = self.board.pieces.get((
                    temp_row, temp_colomn))
                if potentially_doomed_piece:
                    if potentially_doomed_piece.color != self.color:
                        self.legal_moves.append((temp_row, temp_colomn))
                    break
                self.legal_moves.append((temp_row, temp_colomn))
        return self.legal_moves

    def move(self, tile):
        self.rect.center = tile.rect.center
        self.tile = tile


class Rook(Piece):
    DIRECTIONS = [[(i+1, 0) for i in range(7)], [(0, j+1) for j in range(7)], [
        (-(i+1), 0) for i in range(7)], [(0, -(j+1)) for j in range(7)]]

    def __init__(self, image, tile, color, board, groups):
        super().__init__(image, tile, color, board, groups)


class Bishup(Piece):
    DIRECTIONS = [[(i+1, i+1) for i in range(7)], [(-(j+1), -(j+1)) for j in range(7)], [
        (-(i+1), (i+1)) for i in range(7)], [((j+1), -(j+1)) for j in range(7)]]

    def __init__(self, image, tile, color, board, groups):
        super().__init__(image, tile, color, board, groups)


class knight(Piece):
    DIRECTIONS = ([(1, 2)], [(1, -2)], [(2, 1)], [(2, -1)],
                  [(-1, 2)], [(-1, -2)], [(-2, 1)], [(-2, -1)])

    def __init__(self, image, tile, color, board, groups):
        super().__init__(image, tile, color, board, groups)


class Queen(Piece):
    DIRECTIONS = Rook.DIRECTIONS+Bishup.DIRECTIONS

    def __init__(self, image, tile, color, board, groups):
        super().__init__(image, tile, color, board, groups)


class King(Piece):
    DIRECTIONS = ([(1, 0)], [(1, 1)], [(1, -1)], [(0, 1)],
                  [(0, -1)], [(-1, 0)], [(-1, 1)], [(-1, -1)])
    SPECIAL_DIRECTIONS = ((0, 2), (0, -2))

    def __init__(self, image, tile, color, board, groups):
        super().__init__(image, tile, color, board, groups)

    def get_legal_moves(self):
        self.legal_moves = []
        for similar_directions in self.DIRECTIONS:
            for i, j in similar_directions:
                temp_row = self.tile.row+i
                temp_colomn = self.tile.colomn+j
                if not 0 <= temp_row <= 7 or not 0 <= temp_colomn <= 7:
                    break
                potentially_doomed_piece = self.board.pieces.get((
                    temp_row, temp_colomn))
                if potentially_doomed_piece:
                    if potentially_doomed_piece.color != self.color:
                        self.legal_moves.append((temp_row, temp_colomn))
                    break
                self.legal_moves.append((temp_row, temp_colomn))
        counter = 0
        for i, j in self.SPECIAL_DIRECTIONS:
            temp_row = self.tile.row+i
            temp_colomn = self.tile.colomn+j
            if self.color == "white":
                rook = self.board.pieces.get((7, 7))
                if counter == 0 and rook and rook.first_move and self.first_move:
                    if not self.board.pieces.get((7, 6)) and not self.board.pieces.get((7, 5)):
                        self.legal_moves.append((temp_row, temp_colomn))
                rook = self.board.pieces.get((7, 0))
                if counter == 1 and rook and rook.first_move and self.first_move:
                    if not self.board.pieces.get((7, 1)) and not self.board.pieces.get((7, 2)) and not self.board.pieces.get((7, 3)):
                        self.legal_moves.append((temp_row, temp_colomn))
            elif self.color == "black":
                rook = self.board.pieces.get((0, 7))
                if counter == 0 and rook and rook.first_move and self.first_move:
                    if not self.board.pieces.get((0, 6)) and not self.board.pieces.get((0, 5)):
                        self.legal_moves.append((temp_row, temp_colomn))
                rook = self.board.pieces.get((0, 0))
                if counter == 1 and rook and rook.first_move and self.first_move:
                    if not self.board.pieces.get((0, 1)) and not self.board.pieces.get((0, 2)) and not self.board.pieces.get((0, 3)):
                        self.legal_moves.append((temp_row, temp_colomn))
            counter += 1

        return self.legal_moves


class Pawn(Piece):
    DIRECTIONS = [[(-1, 0), (-2, 0)]]
    CAPTURE_DIRECTIONS = [(-1, -1), (-1, 1)]

    def __init__(self, image, tile, color, board, groups):
        super().__init__(image, tile, color, board, groups)

    def get_legal_moves(self):

        self.legal_moves = []
        for similar_directions in self.DIRECTIONS:
            counter = 0
            for i, j in similar_directions:
                temp_row = self.tile.row+i if self.color == "white" else self.tile.row-i
                temp_colomn = self.tile.colomn+j if self.color == "white" else self.tile.colomn-j
                if not 0 <= temp_row <= 7 or not 0 <= temp_colomn <= 7:
                    break
                potentially_doomed_piece = self.board.pieces.get(
                    (temp_row, temp_colomn))
                if potentially_doomed_piece:
                    break
                if not self.first_move and counter == 1:
                    break
                self.legal_moves.append((temp_row, temp_colomn))
                counter += 1
        for i, j in self.CAPTURE_DIRECTIONS:
            temp_row = self.tile.row+i if self.color == "white" else self.tile.row-i
            temp_colomn = self.tile.colomn+j if self.color == "white" else self.tile.colomn-j
            potentially_doomed_piece = self.board.pieces.get(
                (temp_row, temp_colomn))
            if potentially_doomed_piece and potentially_doomed_piece.color != self.board.turn:
                self.legal_moves.append((temp_row, temp_colomn))
        return self.legal_moves
