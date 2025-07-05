from settings import *
from tile import Tile
from pieces import *


class Board(pygame.sprite.Sprite):
    def __init__(self, game, groups):
        super().__init__(groups)
        self.game = game
        self.turn = "white"
        self.image = pygame.image.load("images/Board.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_frect()
        pieces_sprite_sheet = pygame.image.load(
            "images/pieces_sprite_sheet_small.png")
        self.pieces_images = []
        for i in range(12):
            image = pieces_sprite_sheet.subsurface(
                (TILE_SIZE*i, 0, TILE_SIZE, TILE_SIZE)).copy()
            self.pieces_images.append(image)
        self.piece_clicked_row = -1
        self.piece_clicked_colomn = -1
        self.highlighted_tiles = []

        # make tiles
        self.tiles = {}
        for row in range(NUM_OF_TILES):
            for colomn in range(NUM_OF_TILES):
                tile = Tile(row, colomn, self, (self.game.all_group))
                self.tiles[(row, colomn)] = tile

        starting_pieces = [
            (Rook, 0, (7, 0), "white"),
            (Rook, 0, (7, 7), "white"),
            (Rook, 6, (0, 0), "black"),
            (Rook, 6, (0, 7), "black"),

            (Bishup, 2, (7, 2), "white"),
            (Bishup, 2, (7, 5), "white"),
            (Bishup, 8, (0, 2), "black"),
            (Bishup, 8, (0, 5), "black"),

            (knight, 1, (7, 1), "white"),
            (knight, 1, (7, 6), "white"),
            (knight, 7, (0, 1), "black"),
            (knight, 7, (0, 6), "black"),

            (Queen, 3, (7, 3), "white"),
            (Queen, 9, (0, 3), "black"),

            (King, 4, (7, 4), "white"),
            (King, 10, (0, 4), "black"),
        ]
        for col in range(8):
            starting_pieces.append((Pawn, 5, (6, col), "white"))
            starting_pieces.append((Pawn, 11, (1, col), "black"))

        self.pieces = {}

        for piece, frame, pos, color in starting_pieces:
            piece = piece(
                self.pieces_images[frame], self.tiles[pos], color, self, self.game.all_group)
            self.pieces[pos] = piece

    def highlight_moves(self):
        piece = self.pieces.get(
            (self.piece_clicked_row, self.piece_clicked_colomn))
        for row, colomn in piece.get_legal_moves():
            tile = self.tiles[(row, colomn)]
            tile.highlight()
            self.highlighted_tiles.append(tile)

    def unhighlight_moves(self):
        for tile in self.highlighted_tiles:
            tile.unhighlight()
        self.highlighted_tiles = []

    def move(self, piece, old_row, old_colomn, new_row, new_colomn):
        piece.move(self.tiles[new_row, new_colomn])
        piece.first_move = False
        if self.pieces.get((new_row, new_colomn)):
            self.pieces[(new_row, new_colomn)].kill()
        if type(piece) == King:
            if old_colomn == 4:
                if piece.color == "white":
                    if new_colomn == 6:
                        rook = self.pieces.get((7, 7))
                        self.move(rook, 7, 7, 7, 5)
                    elif new_colomn == 2:
                        rook = self.pieces.get((7, 0))
                        self.move(rook, 7, 0, 7, 3)
                elif piece.color == "black":
                    if new_colomn == 6:
                        rook = self.pieces.get((0, 7))
                        self.move(rook, 0, 7, 0, 5)
                    elif new_colomn == 2:
                        rook = self.pieces.get((0, 0))
                        self.move(rook, 0, 0, 0, 3)
                self.turn = piece.color
        if type(piece) == Pawn:
            if piece.color == "white" and new_row == 0 or piece.color == "black" and new_row == 7:
                piece.kill()
                if piece.color == "white":
                    new_piece = Queen(self.pieces_images[3], self.tiles[(
                        new_row, new_colomn)], "white", self, self.game.all_group)
                    self.pieces[(new_row, new_colomn)] = new_piece
                elif piece.color == "black":
                    new_piece = Queen(self.pieces_images[9], self.tiles[(
                        new_row, new_colomn)], "black", self, self.game.all_group)
                    self.pieces[(new_row, new_colomn)] = new_piece
                piece = new_piece

        self.pieces[(new_row, new_colomn)] = piece
        self.pieces.pop((old_row, old_colomn))
        self.piece_clicked_row = -1
        self.piece_clicked_colomn = -1
        self.turn = "white" if self.turn == "black" else "black"
