from settings import *

class Snap_Shot():
    def __init__(self,board,moved_piece,captured_piece,old_row,old_colomn,new_row,new_colomn,turn,):
        self.board=board
        self.legal_moves=self.board.legal_moves
        self.checked_king_pos=self.board.checked_king_pos
        self.moved_piece=moved_piece
        self.moved_piece_tile=moved_piece.tile
        self.captured_piece=captured_piece
        self.old_row=old_row
        self.old_colomn=old_colomn
        self.new_row=new_row
        self.new_colomn=new_colomn
        self.turn=turn
        self.moved_first_move = moved_piece.first_move
        self.captured_first_move = captured_piece.first_move if captured_piece else None
    def apply(self):
        self.moved_piece.move(self.board.tiles[self.old_row, self.old_colomn])
        self.moved_piece.tile=self.moved_piece_tile
        self.moved_piece.first_move = self.moved_first_move
        self.board.pieces[(self.old_row,self.old_colomn)]=self.moved_piece
        self.board.pieces.get((self.new_row, self.new_colomn)).kill()
        self.board.pieces.pop((self.new_row, self.new_colomn))
        self.moved_piece.add(self.board.game.all_group)
        if self.captured_piece:
            self.captured_piece.first_move = self.captured_first_move
            self.captured_piece.add(self.board.game.all_group)
            self.board.pieces[(self.new_row, self.new_colomn)] = self.captured_piece
        self.board.turn=self.turn
        self.board.checked_king_pos=self.checked_king_pos
        self.board.legal_moves=self.legal_moves