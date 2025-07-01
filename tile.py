from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, row, colomn, board, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_frect(
            topleft=(colomn*TILE_SIZE, row*TILE_SIZE))
        self.row = row
        self.colomn = colomn
        self.board = board
        self.occupied = False

    def picking_piece(self, new_piece):
        if self.left_clicked() and new_piece and new_piece.color == self.board.turn:
            return True
        return False

    def putting_piece(self, old_piece):
        if self.left_clicked() and self.board.piece_clicked_row != -1 and self.board.piece_clicked_colomn != -1:
            if (self.row, self.colomn) in old_piece.get_legal_moves():
                return True
        return False

    def left_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_just_pressed()[0] and self.rect.collidepoint(mouse_pos):
            return True
        return False

    def update(self):
        old_row = self.board.piece_clicked_row
        old_colomn = self.board.piece_clicked_colomn
        old_piece = self.board.pieces.get((old_row, old_colomn))
        new_piece = self.board.pieces.get((self.row, self.colomn))
        if self.picking_piece(new_piece):
            self.board.piece_clicked_row = self.row
            self.board.piece_clicked_colomn = self.colomn
        elif self.putting_piece(old_piece):
            self.board.move(old_piece, old_row, old_colomn,
                            self.row, self.colomn)
        elif self.left_clicked():
            self.board.piece_clicked_row = -1
            self.board.piece_clicked_colomn = -1
