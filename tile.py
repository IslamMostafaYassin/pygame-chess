from settings import *
from text import Text
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
            if old_piece:
                key = (old_piece.type, old_piece.tile.row, old_piece.tile.colomn)
                if self.board.legal_moves.get(key) and (self.row, self.colomn) in self.board.legal_moves[(key)]:
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
            self.board.complete_legal_moves(self.board.turn)
            if self.board.find_check(self.board.turn):
                king_pos = self.board.checked_king_pos
                key = ("king", *king_pos)
                king_moves = self.board.legal_moves.get(key)

                if king_moves:
                    self.board.legal_moves[key] = [move for move in king_moves if abs(move[1] - king_pos[1]) != 2]

                self.board.tiles[king_pos].pink_highlight()
            else:
                for tile in self.board.tiles.values():
                    tile.unhighlight()
            
            key=("king",7,4)
            king_moves = self.board.legal_moves.get(key)
            if king_moves:
                if (7,5) not in self.board.legal_moves[key]:
                    self.board.legal_moves[key] = [move for move in king_moves if (move[1] - 4) != 2]
                elif (7,3) not in self.board.legal_moves[key]:
                    self.board.legal_moves[key] = [move for move in king_moves if (4 - move[1]) != 2]
            key=("king",0,4)
            king_moves=self.board.legal_moves.get(key)
            if king_moves:
                if (0,5) not in self.board.legal_moves[key]:
                    self.board.legal_moves[key] = [move for move in king_moves if (move[1] - 4) != 2]
                elif (0,3) not in self.board.legal_moves[key]:
                    self.board.legal_moves[key] = [move for move in king_moves if (4 - move[1]) != 2]
            
            
            if self.board.no_legal_moves():
                if self.board.checked_king_pos:
                    Text(self.board.game.font,f"{"white" if self.board.turn=="black" else "black"} wins","green",(WINDOW_WIDTH/2,WINDOW_HEIGHT/2),self.board.game.all_group)
                else:
                    Text(self.board.game.font,"stalemate","blue",(WINDOW_WIDTH/2,WINDOW_HEIGHT/2),self.board.game.all_group)

        elif self.left_clicked():
            self.board.unhighlight_moves()
            self.board.piece_clicked_row = -1
            self.board.piece_clicked_colomn = -1
        