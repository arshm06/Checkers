from tkinter import *
from tkinter import messagebox

class CheckersSquare(Canvas):
    '''displays a square in the Checkers game'''

    def __init__(self,master,r,c):
        '''CheckersSquare(master,r,c)
        creates a new blank Checker square at coordinate (r,c)'''
        # create and place the widget
        Canvas.__init__(self,master,width=50,height=50,bg='dark green', highlightthickness = 0)
        self.grid(row=r,column=c)
        # set the attributes
        self.position = (r,c)
        self.king = False
        # bind button click to placing a piece
        self.bind('<Button>',master.get_click)
        
    def get_king(self):
        '''CheckersSquare.get_king() -> (boolean)
        returns (self.king) attribute of square'''
        return self.king
    
    def make_king(self, boolean):
        '''CheckersSquare.make_king(boolean)
        changes (self.king) attribute of square'''
        self.king = boolean

    def get_position(self):
        '''CheckersSquare.get_position() -> (int,int)
        returns (row,column) of square'''
        return self.position

    def make_color(self,color):
        '''CheckersSquare.make_color(color)
        changes color of piece on square to specified color'''
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)
        self.create_oval(10,10,41,41,fill=color) # create oval
        if self.king: # create asterik if there is a square
            self.create_text(25,30,fill="black",font="Times 40 italic bold",text="*")
        
        
    def delete_oval(self):
        '''CheckersSquare.delete_color()
        deletes oval on the square'''
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)
        if self.king: # remove asterik if there is a square
            self.create_text(25,30,fill="black",font="Times 40 italic bold",text="")
            self.make_king(False)
        
class CheckersGame(Frame):
    '''represents a game of Checkers'''

    def __init__(self,master):
        '''CheckersGame(master,[computerPlayer])
        creates a new Checkers game'''
        # initialize the Frame
        Frame.__init__(self,master,bg='white')
        self.grid()
        # set up game data
        self.colors = ('red','white')  # players' colors
        self.firstClick = ()
        self.jump = [False]
        self.jumpSquares = []
        # create board in starting position, player 0 going first
        self.board = {}  # dict to store position
        # dedicate squares to players position
        for row in range(8):
            for column in range(8):
                coords = (row,column)
                if row % 2 != column % 2:
                    if row < 3:
                        self.board[coords] = 0  # player 1
                    elif row > 4:
                        self.board[coords] = 1  # player 0
                    else:
                        self.board[coords] = None
                else:
                    self.board[coords] = None
        self.currentPlayer = 0  # player 0 starts 
        self.squares = {}  # stores CheckersSquares
        # changes the background of each square depending on location
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                self.squares[rc] = CheckersSquare(self,row,column)
                if row % 2 == column % 2:
                    self.squares[rc]['bg'] = 'blanched almond'
                    self.squares[rc].unbind('<Button>')
        # set up scoreboard and status markers
        self.rowconfigure(8,minsize=3)  # leave a little space
        self.turnSquare = CheckersSquare(self,9,2)  # to label the turn indicator square
        self.turnSquare['bg'] = 'gray'
        # create indicator squares and score labels  
        self.turnSquare.make_color(self.colors[0])
        self.turnSquare.unbind('<Button>')
        Label(self,text='Turn:',font=('Arial',18)).grid(row=9,column=1)
        # update squares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                piece = self.get_piece(rc)
                if piece is not None:
                    self.squares[rc].make_color(self.colors[piece])
        
    def get_piece(self,coords):
        '''CheckersBoard.get_piece(coords) -> int
        returns the piece at coords'''
        return self.board[coords]

    def get_player(self):
        '''CheckersBoard.get_player() -> int
        returns the current player'''
        return self.currentPlayer
    
    def get_legal_moves(self, coords):
        '''CheckersBoard.get_legal_moves() -> list
        returns a list of the current player's legal moves'''
        moves = []  # place legal moves here
        self.jump = [False] # place jumps here
        # decide which direction the square can move
        if self.squares[coords].get_king():
            pivotList = [(-1,-1), (-1,1), (1,1), (1,-1)]
        elif self.get_piece(coords) == 1:
            pivotList = [(-1,-1), (-1,1)]
        elif self.get_piece(coords) == 0:
            pivotList = [(1,1), (1,-1)]
        # test whether the possible move is legal
        for pivot in pivotList:
            tempCoords = (coords[0]+pivot[0], coords[1]+pivot[1])
            if tempCoords in self.board.keys():
                if self.get_piece(tempCoords) is None:
                    moves.append(tempCoords)
                # check if a jump is possible
                elif self.get_piece(tempCoords) == 1 - self.currentPlayer:
                    tempCoords = (coords[0]+2*pivot[0], coords[1]+2*pivot[1])
                    if tempCoords in self.board.keys():
                        if self.get_piece(tempCoords) is None:
                            self.jump.append(tempCoords) # add jump to another list too
                            moves.append(tempCoords)
        
        # if a jump is possible, change the first element to True
        if len(self.jump) > 1:
            self.jump[0] = True
        return moves
    
    def get_possible_squares(self):
        '''CheckersBoard.get_possible_squares() -> list
        returns a list of the current player's legal cells to click'''
        possibleSquares = [] # stores legal cells
        self.jumpSquares = [] # stores legal cells which are used to jump
        for box in self.squares.keys():
            # decide the move of the cell based on its player characterisitc
            if self.squares[box].get_king():
                pivotList = [(-1,-1), (-1,1), (1,1), (1,-1)]
            elif self.currentPlayer == 1:
                pivotList = [(-1,-1), (-1,1)]
            elif self.currentPlayer == 0:
                pivotList = [(1,1), (1,-1)]
            for pivot in pivotList:
                # check if the box has legal moves
                tempCoords = (box[0]+pivot[0], box[1]+pivot[1])
                if tempCoords in self.board.keys() and box[0]%2 != box[1]%2  and self.get_piece(box)==self.currentPlayer:
                    if self.get_piece(tempCoords) is None and self.get_piece(box) is not None:
                        possibleSquares.append(box)
                    elif self.get_piece(tempCoords) == 1 - self.currentPlayer:
                        # checks for jumps
                        tempCoords = (box[0]+2*pivot[0], box[1]+2*pivot[1])
                        if tempCoords in self.board.keys() and self.get_piece(box) is not None:
                            if self.get_piece(tempCoords) is None:
                                self.jumpSquares.append(box) # add jump to another list too
                                possibleSquares.append(box)
                                
        return possibleSquares
        
    def next_player(self):
        '''CheckersBoard.next_player()
        advances to next player'''
        self.currentPlayer = 1 - self.currentPlayer
        self.turnSquare.make_color(self.colors[self.currentPlayer]) # change color of square
        
    def get_click(self,event):
        '''CheckersBoard.get_click(event)
        checks a click and acts accordingly'''
        self.check_lose()
        # checks if a click is the first one
        if self.firstClick == ():
            self.firstClick = event.widget.get_position()
            # check if the click is viable
            if self.firstClick in self.get_possible_squares() and self.get_piece(self.firstClick) == self.currentPlayer:
                if len(self.jumpSquares) != 0 and self.firstClick not in self.jumpSquares:
                    self.firstClick = ()
                    return
                # border the cell
                self.squares[self.firstClick]['highlightthickness']=2
                self.squares[self.firstClick]['highlightbackground']='black'
            else:
                self.firstClick = ()
        else:
            self.secondClick = event.widget.get_position()
            # checks if the second click is a real option
            if self.secondClick in self.get_legal_moves(self.firstClick):
                # if the player does not jump when they can
                if self.jump[0] and self.secondClick not in self.jump:
                    self.check_lose()
                    return
                # if player jumps when they can
                elif self.jump[0] and self.secondClick in self.jump:
                    # takes average of the cells to find the middle cell that is jumped over
                    self.squares[((self.firstClick[0]+self.secondClick[0])/2, (self.firstClick[1] + self.secondClick[1])/2)].delete_oval()
                    self.board[((self.firstClick[0]+self.secondClick[0])/2, (self.firstClick[1] + self.secondClick[1])/2)] = None
                    self.board[self.firstClick] = None
                    self.board[self.secondClick] = self.currentPlayer
                    # if the move creates a king or if the cell is a king
                    if self.secondClick[0] == 7 and self.get_piece(self.secondClick) == 0 or self.secondClick[0] == 0 and self.get_piece(self.secondClick) == 1 or self.squares[self.firstClick].get_king():
                        self.squares[self.secondClick].make_king(True)
                        # if the cell is not already a king
                        if not self.squares[self.firstClick].get_king():
                            self.squares[self.firstClick].delete_oval()
                            self.squares[self.secondClick].make_color(self.colors[self.currentPlayer])
                            self.squares[self.firstClick]['highlightthickness']=0
                            self.get_legal_moves(self.secondClick)
                            self.firstClick = ()
                            self.check_lose()
                            self.next_player()
                            return
                    self.squares[self.firstClick].delete_oval()
                    self.squares[self.secondClick].make_color(self.colors[self.currentPlayer])
                    self.squares[self.firstClick]['highlightthickness']=0
                    self.get_legal_moves(self.secondClick)
                    # if the player can jump again
                    if self.jump[0]:
                        self.firstClick = self.secondClick
                        self.squares[self.firstClick]['highlightthickness']=2
                        self.squares[self.firstClick]['highlightbackground']='black'
                        return
                    self.firstClick = ()
                    self.check_lose()
                    self.next_player()
                    return
                # changes values after moving
                self.board[self.firstClick] = None
                self.board[self.secondClick] = self.currentPlayer
                # checks for kings
                if self.secondClick[0] == 7 and self.get_piece(self.secondClick) == 0 or self.secondClick[0] == 0 and self.get_piece(self.secondClick) == 1 or self.squares[self.firstClick].get_king():
                    self.squares[self.secondClick].make_king(True)
                # changes appearance after moving
                self.squares[self.firstClick].delete_oval()
                self.squares[self.secondClick].make_color(self.colors[self.currentPlayer])
                self.squares[self.firstClick]['highlightthickness']=0
                self.firstClick = ()
                self.check_lose()
                self.next_player()
                    
    def check_lose(self):
        '''CheckersBoard.check_lose(self)
        checks if a player has lost'''
        lose = True
        # checks if there is a cell which can be moved
        for box in self.board.keys():
            if self.get_piece(box) == self.currentPlayer:
                if len(self.get_legal_moves(box)) != 0:
                    # if criteria holds, the player has not lost
                    lose = False
        
        # shows a message which indicates that a player has won
        if lose:
            messagebox.showerror('Checkers','Player ' + self.colors[1-self.currentPlayer] + ' wins',parent=self)
            return
    
def play_checkers():
    '''play_checkers()
    starts a new game of Checkers'''
    root = Tk()
    root.title('Checkers')
    CG = CheckersGame(root)
    CG.mainloop()

play_checkers()

#
