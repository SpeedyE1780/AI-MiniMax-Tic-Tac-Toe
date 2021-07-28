# -*- coding: utf-8 -*-
"""
Created on:

@author: 
"""
import random
from collections import namedtuple
from tkinter import *
import tkinter.messagebox
import threading
import time

GameState = namedtuple('GameState', 'to_move, utility, board, moves')
infinity = float('inf')
game_result = { 1:"Player 1 Wins", -1:"Player 2 Wins", 0:"It is a Tie" }

class Game:
    """To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial

        while True:
            for player in players:
                
                move = player(self, state)
                state = self.result(state, move)

                if self.terminal_test(state):
                    self.display(state)

                    ##The utitlity was always passed the initial state as an argument instead of the current state
                    ##print("Game Over.", game_result.get(self.utility(state, self.to_move(self.initial)), "Thank you for playing"))
                    print("Game Over.", game_result.get(self.utility(state), "Thank you for playing"))

                    ##The function was returning a value but it's not nedded
                    ##return self.utility(state, self.to_move(self.initial))
                    return None
                

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

##The grid will be created later so no need to initialize it and the state in the constructor
##    def __init__(self, h=3, v=3, k=3):
##        self.h = h
##        self.v = v
##        self.k = k
##        moves = [(x, y) for x in range(1, h + 1)
##                 for y in range(1, v + 1)]
##        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def __init__(self):
        ##Initialize the main window
        self.Window = Tk()
        self.Window.resizable(False,False)
        self.Window.title("Tic Tac Toe!")

        ##Create the main menu
        self.mainMenu = Frame(self.Window)
        self.mainMenu.pack()
        lblTitle = Label(self.mainMenu , text="Tic Tac Toe Grid")
        lblTitle.grid(row = 0 , column = 0 , columnspan = 2)

        ##Enter the horizontal size
        self.horizontal = StringVar()
        self.lblHorizontal = Label(self.mainMenu , text="Enter number of cells horizontally")
        self.lblHorizontal.grid(row = 1 , column = 0)
        self.entryHorizontal = Entry(self.mainMenu , textvariable = self.horizontal)
        self.entryHorizontal.grid(row = 1 , column = 1)

        ##Enter the vertical size
        self.vertical = StringVar()
        self.lblVertical = Label(self.mainMenu , text="Enter number of cells vertically")
        self.lblVertical.grid(row = 2 , column = 0)
        self.entryVertical = Entry(self.mainMenu , textvariable = self.vertical)
        self.entryVertical.grid(row = 2 , column = 1)

        ##Enter the number of consecutive moves to win
        self.toWin = StringVar()
        self.lbltoWin = Label(self.mainMenu , text="Enter number of consecutive cells to win")
        self.lbltoWin.grid(row = 3 , column = 0)
        self.entrytoWin = Entry(self.mainMenu , textvariable = self.toWin)
        self.entrytoWin.grid(row = 3 , column = 1)

        ##Submit Button
        self.createGrid = Button(self.mainMenu , text="Create Grid" , command = self.CreateGrid)
        self.createGrid.grid(row = 4 , column = 1)

        ##Set the player 1 and 2 mode
        self.p1Mode = IntVar()
        self.p2Mode = IntVar()
        self.playerSelection = Frame(self.Window)
        self.lblPlayerSelection = Label(self.playerSelection , text="Player Selection")
        self.lblPlayerSelection.grid(row = 0, column = 1)

        self.p1Label = Label(self.playerSelection , text = "Player 1")
        self.p1Label.grid(row = 1 , column = 0)
        self.p2Label = Label(self.playerSelection , text = "Player 2")
        self.p2Label.grid(row = 1 , column = 2)

        ##Human Players
        self.p1Human = Radiobutton(self.playerSelection , text="Human Player" , variable= self.p1Mode , value=1)
        self.p1Human.grid(row = 2, column = 0)
        self.p2Human = Radiobutton(self.playerSelection , text="Human Player" , variable= self.p2Mode , value=1)
        self.p2Human.grid(row = 2, column = 2)

        ##Random Players
        self.p1Random = Radiobutton(self.playerSelection , text="Random Player" , variable= self.p1Mode , value=2)
        self.p1Random.grid(row = 3, column = 0)
        self.p2Random = Radiobutton(self.playerSelection , text="Random Player" , variable= self.p2Mode , value=2)
        self.p2Random.grid(row = 3, column = 2)

        ##Minimax Players
        self.p1MiniMax = Radiobutton(self.playerSelection , text="Minimax Player" , variable= self.p1Mode , value=3)
        self.p1MiniMax.grid(row = 4, column = 0)
        self.p2MiniMax = Radiobutton(self.playerSelection , text="Minimax Player" , variable= self.p2Mode , value=3)
        self.p2MiniMax.grid(row = 4, column = 2)

        ##AlphaBeta Players
        self.p1AlphaBeta = Radiobutton(self.playerSelection , text="AlphaBeta Player" , variable= self.p1Mode , value=4)
        self.p1AlphaBeta.grid(row = 5, column = 0)
        self.p2AlphaBeta = Radiobutton(self.playerSelection , text="AlphaBeta Player" , variable= self.p2Mode , value=4)
        self.p2AlphaBeta.grid(row = 5, column = 2)

        ##StartGame Button
        self.startGame = Button(self.playerSelection , text="Start" , command= self.StartGame)
        self.startGame.grid(row = 6, column = 1)
        self.Window.mainloop()

    def CreateGrid(self):
        """Create a grid using the parameters entered by the user"""

        ##Get the horizontal size
        ##Check the input is an int
        try:
            self.h = int(self.horizontal.get())

            if not self.h in range(3,11): ##Keep the grid size between 3x3 and 10x10
                tkinter.messagebox.showwarning("Horizontal Warning" , "Please enter a number between 3 and 10")
                return None

        except ValueError:
            tkinter.messagebox.showerror("Horizontal Input Error" , "Please enter a number")
            return None

        ##Get the vertical size
        ##Check the input is an int
        try:
            self.v = int(self.vertical.get())

            if not self.v in range(3,11): ##Keep the grid size between 3x3 and 10x10
                tkinter.messagebox.showwarning("Vertical Warning" , "Please enter a number between 3 and 10")
                return None

        except ValueError:
            tkinter.messagebox.showerror("Vertical Input Error" , "Please enter a number")
            return None

        ##Get the consecutive cells
        ##Check the input is an int
        try:
            self.k = int(self.toWin.get())

            if self.k > self.h or self.k > self.v: ##Make sure that the line can fit in the grid
                tkinter.messagebox.showwarning("Consecutive Cell Warning" , "Please enter a number that's less or equal to the Horizontal and Vertical")
                return None

        except ValueError:
            tkinter.messagebox.showerror("Consecutive Cell Input Error" , "Please enter a number")
            return None

        ##Create the moves and set the initial state
        moves = [(x, y) for x in range(1, self.h + 1)
              for y in range(1, self.v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

        ##Create the game screen
        self.gameScreen = Frame(self.Window)

        ##Add a label to indicate who's turn it is
        self.lblPlayerTurn = Label(self.gameScreen , text = "")
        self.lblPlayerTurn.grid(row = 0 , column = 0 , columnspan = self.h + 1)

        ##Initialize the buttons each button represents a move
        self.gameButtons = {}
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                ##Give x and y default value so that they don't all return the same values
                self.gameButtons[x,y] = Button(self.gameScreen , width = 10, command = lambda x=x, y=y : self.UpdatePlayerMove((x, y)))
                self.gameButtons[x,y].grid(row = x + 1 , column = y)

        ##Exit button once the game ends
        btnExit = Button(self.gameScreen , text = "Exit" , command = self.ExitGame , width = 10)
        btnExit.grid(row = self.v + 2 , column = 0 , columnspan = self.h + 1)

        ##Move to the player selection screen
        self.mainMenu.pack_forget()
        self.playerSelection.pack()

    def StartGame(self):
        """Start Game using the start button"""

        ##Get the Player 1 Mode
        player1 = self.p1Mode.get()
        if player1 == 1:
            player1 = human_player

        elif player1 == 2:
            player1 = random_player

        elif player1 == 3:
            player1 = minmax_player

        elif player1 == 4:
            player1 = alphabeta_player

        else:
            tkinter.messagebox.showerror("Player 1 Error" , "Choose a mode for player 1")
            return None

        ##Get the Player 2 Mode
        player2 = self.p2Mode.get()
        if player2 == 1:
            player2 = human_player

        elif player2 == 2:
            player2 = random_player

        elif player2 == 3:
            player2 = minmax_player

        elif player2 == 4:
            player2 = alphabeta_player

        else:
            tkinter.messagebox.showerror("Player 2 Error" , "Choose a mode for player 2")
            return None

        ##Start the game on a different thread to be able to wait for the human players to input a move
        self.playerSelection.pack_forget()
        self.gameScreen.pack()
        self.gameThread = threading._start_new_thread(self.play_game , (player1,player2))


    def ExitGame(self):
        """Exit the game and leave to the main menu"""
        ##Check if the user can quit if not show a warning
        if self.gameEnded:
            self.gameScreen.pack_forget()
            self.mainMenu.pack()
        else:
            tkinter.messagebox.showwarning("Cannot Exit Game" , "Game is still in progress")

    def UpdatePlayerMove(self , move):
        """"Update the move of human players"""
        self.playerMove = move

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move , updateLabel = False):

## This leads to the player losing his turn because the playgame function will iterate to the next player
## Computer based players can't enter illegal moves because they're choosing from a list of move so we check the move when the human player is inputing it
##        if move not in state.moves:
##            print("\nThis is not a legal move, please play again\n")
##            return state  # Illegal move has no effect
        
        ## Get a copy of the board and update it by adding the player who took that move
        board = state.board.copy()
        board[move] = state.to_move
        
        ##To prevent updating while minimax searches for his move
        if updateLabel:
            ##Replace the button with a label of the player who took this cell
            lblMove = Label(self.gameScreen , text = state.to_move , width = 10)
            lblMove.grid(row = move[0] + 1 , column = move[1])
            self.gameButtons[move].grid_forget()
        else:
            self.lblPlayerTurn.config(text="Processing")

        ## Get a copy of the moves and delete the current move
        moves = list(state.moves)
        moves.remove(move)
        
        ## Return the current state
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

##  No need to send the player as an argument because the utility only depends on one player
##  def utility(self, state, player):
    def utility(self, state):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        ##The utility value is only dependent on one player it shouldn't be changed based on the current player
        ##return state.utility if player == 'X' else -state.utility
        return state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial

        ##Stops the player from quitting before the game ends
        self.gameEnded = False
        while True:
            for player in players:

                ##Update the label's saying who's turn is it
                self.lblPlayerTurn.config(text = ("Player 1's Turn" if state.to_move == 'X' else "Player 2's Turn"))

                ##When it's the human's turn wait for him to press a button then update his move
                if player == human_player:
                    ##Reset the move to none
                    self.playerMove = None

                    ##No move has been chosen yet
                    while self.playerMove == None:
                        time.sleep(0.05) ##Wait for 50 ms seconds before checking again

                    ##Update the move to the player's move
                    move = self.playerMove
                else:
                    move = player(self, state)

                ##Update the current state
                state = self.result(state, move , True)

                ##Check that the game has ended
                if self.terminal_test(state):
                    self.display(state)

                    ##The utitlity was always passed the initial state as an argument instead of the current state
                    ##print("Game Over.", game_result.get(self.utility(state, self.to_move(self.initial)), "Thank you for playing"))
                    print("Game Over.", game_result.get(self.utility(state), "Thank you for playing"))

                    ##Update the label to the game result and enable the player to quit the game
                    self.lblPlayerTurn.config(text = game_result.get(self.utility(state)))
                    self.gameEnded = True

                    ##The function was returning a value but it's not nedded
                    ##return self.utility(state, self.to_move(self.initial))
                    return None
        
    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        ## Directions to determine number of consecutive cells
        horizontal = (1, 0)
        vertical = (0, 1)
        posDiagonal = (1, 1) ##Checks for cells down right / up left
        negDiagonal = (1, -1) ##Checks for cells down left / up right

##        if (self.k_in_row(board, move, player, (0, 1)) or
##                self.k_in_row(board, move, player, (1, 0)) or
##                self.k_in_row(board, move, player, (1, -1)) or
##                self.k_in_row(board, move, player, (1, 1))):

        if (self.k_in_row(board, move, player, vertical) or
                self.k_in_row(board, move, player, horizontal) or
                self.k_in_row(board, move, player, negDiagonal) or
                self.k_in_row(board, move, player, posDiagonal)):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row/column/diagonal

        ## Search in one direction
        ##while board.get((x, y)) == player: Didn't check if x and y are within the bounds of the grid
        while board.get((x, y)) == player and x in range(0 , self.h + 1) and y in range(0 , self.v + 1):
            n += 1
            x, y = x + delta_x, y + delta_y

        ## Search in the opposite direction
        x, y = move
        ##while board.get((x, y)) == player: Didn't check if x and y are within the bounds of the grid
        while board.get((x, y)) == player and x in range(0 , self.h + 1) and y in range(0 , self.v + 1):
            n += 1
            x, y = x - delta_x, y - delta_y

        n -= 1  # Because we counted move itself twice
        return n >= self.k

def minimax_search(state, game):
    """Search game to determine best action; use minimax search"""

    player = game.to_move(state) # get the player to move

    def max_value(state): # max_value function to return v the value of a max node and the best action found
        
        ##Return the utility of a terminal state
        if game.terminal_test(state):
            return game.utility(state) , None

        v = -infinity
        action = None
        
        ##Loop through all successors and get the max value
        for a in game.actions(state):
            value = max(v, min_value(game.result(state, a))[0]) ##min_value returns a tuple(value , action)

            ##Update v to the max value and update the action
            if v != value:
                v = value
                action = a
        return v , action

    def min_value(state): # min_value function to return v the value of a min node and the best action found
        
        ##Return the utility of a terminal state
        if game.terminal_test(state):
            return game.utility(state) , None

        v = +infinity
        action = None

        ##Loop through all successors and get the min value
        for a in game.actions(state):
            value = min(v , max_value(game.result(state,a))[0]) ##max_value returns a tuple(value , action)

            ##Update v to the min value and update the action
            if v != value:
                v = value
                action = a
        return v , action
                
    # Body of minimax:
    best_score = -infinity
    best_action = None
    
    if player == "X": ##Max player get the max value of the current state and the best action
        best_score , best_action = max_value(state)
            
    else: #Min player get the min value of the current state and the best action
        best_score , best_action = min_value(state)
      
    return best_action
    
def alphabeta_search(state, game):
    """Search game to determine best action; use minimax search"""

    player = game.to_move(state) # get the player to move

    def max_value(state , alpha , beta): # max_value function to return v the value of a max node and the best action found
        
        ##Return the utility of a terminal state
        if game.terminal_test(state):
            return game.utility(state) , None

        v = -infinity
        action = None
        
        ##Loop through all successors and get the max value
        for a in game.actions(state):
            value = max(v, min_value(game.result(state, a) , alpha , beta)[0]) ##min_value returns a tuple(value , action) 

            ##Update v to the max value and update the action
            if v != value:
                v = value
                action = a

                ##Update alpha
                alpha = max(alpha , v)

                ##Check if remaining nodes can be pruned
                if v >= beta:
                    return v , action

        return v , action

    def min_value(state , alpha , beta): # min_value function to return v the value of a min node and the best action found
        
        ##Return the utility of a terminal state
        if game.terminal_test(state):
            return game.utility(state) , None

        v = +infinity
        action = None

        ##Loop through all successors and get the min value
        for a in game.actions(state):
            value = min(v , max_value(game.result(state,a) , alpha , beta)[0]) ##max_value returns a tuple(value , action) 

            ##Update v to the min value and update the action
            if v != value:
                v = value
                action = a

                ##Update beta
                beta = min(v , beta)

                ##Check if remaining nodes can be pruned
                if v <= alpha:
                    return v, action

        return v , action
                
    # Body of minimax:
    best_score = -infinity
    best_action = None
    
    if player == "X": ##Max player get the max value of the current state and the best action
        best_score , best_action = max_value(state , -infinity , infinity)
            
    else: #Min player get the min value of the current state and the best action
        best_score , best_action = min_value(state , -infinity , infinity)
      
    return best_action


"""Define the players"""

def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None

def minmax_player(game, state):
    """A player that chooses a legal move using minmax."""
    return minimax_search(state, game)
    
def alphabeta_player(game, state):
    """A player that chooses a legal move using minmax with alpha-beta pruning."""
    return alphabeta_search(state, game)
   
##Function no longer needed since the user will use the buttons instead
def human_player(game, state):
    """Human player: make a move by querying standard input."""
    
    print("Game board:")
    game.display(state)
    print("Available moves: {}".format(game.actions(state)))
    print("")
    move = None

    if game.actions(state):

         ##Check if the move is valid
        invalidMove = True
        while invalidMove:
            move_string = input('Your move? ')
            move = eval(move_string)

            if move not in state.moves:
                invalidMove = True
                print("\nThis is not a legal move, please play again \n")
            else:
                invalidMove = False

## Not needed doesn't check for valid or invalid moves
##            try:
##               move = eval(move_string)
##               invalidMove = False
##            except NameError:
##                invalidMove = True
##                move = move_string

    else:
        print("no legal moves: passing turn to next player")

    return move

# play a game of tic tac toe
ttt_game = TicTacToe()