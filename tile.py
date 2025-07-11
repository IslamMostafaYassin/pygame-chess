from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, row, colomn, board, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 0))
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

    def highlight(self, capture_piece=False):
        if capture_piece:
            pygame.draw.rect(self.image, "red", self.image.get_frect(), 1)
        else:
            pygame.draw.rect(self.image, "cyan", self.image.get_frect(), 1)


    def pink_highlight(self, capture_piece=False):
        pygame.draw.rect(self.image, "pink", self.image.get_frect())

    def unhighlight(self):
        self.image.fill((255, 255, 255, 0))

    def update(self):
        # self.image.fill((255, 255, 255, 0))
        old_row = self.board.piece_clicked_row
        old_colomn = self.board.piece_clicked_colomn
        old_piece = self.board.pieces.get((old_row, old_colomn))
        new_piece = self.board.pieces.get((self.row, self.colomn))
        if self.picking_piece(new_piece):
            self.board.unhighlight_moves()
            self.board.piece_clicked_row = self.row
            self.board.piece_clicked_colomn = self.colomn
            self.board.highlight_moves()
        elif self.putting_piece(old_piece):
            self.board.unhighlight_moves()
            self.board.move(old_piece, old_row, old_colomn,
                            self.row, self.colomn)
            if self.board.find_check("black" if self.board.turn=="white" else "white"):
                self.board.ctrl_z()
            elif self.board.find_check(self.board.turn):
                self.board.tiles[*self.board.checked_king_pos].pink_highlight()
            else:
                for tile in self.board.tiles.values():
                    tile.unhighlight()

        elif self.left_clicked():
            self.board.unhighlight_moves()
            self.board.piece_clicked_row = -1
            self.board.piece_clicked_colomn = -1
        