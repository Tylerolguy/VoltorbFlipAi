

import random


def main():
  player1 = Player()
  game = Game(player1)
  game.start()




class Game:
    def __init__(self, player):
        self.rows = 5
        self.cols = 5
        self.player = player
        self.numVoltorbs = 0
        self.numPoints = 0
        self.board = []
        self.pointsEarned = 0
        self.voltorbCountVertically = [0 for _ in range(self.rows)] #the right sides vertical count of voltorbs
        self.voltorbCountHorizontally = [0 for _ in range(self.cols)] #the bottom horizontal count of voltorbs
        self.pointCountVertically = [5 for _ in range(self.rows)] #the right sides vertical count of points
        self.pointCountHorizontally = [5 for _ in range(self.cols)] #the bottom horizontal count of points
        self.flipped = [[False for _ in range(self.cols)] for _ in range(self.rows)] #the flipped state of each cell


    def start(self):
      self.makeLevel()
        # Game logic here
      while True:
        self.display_board()
        print(f"Level: {self.player.level}, Score: {self.player.score}, Points Earned: {self.pointsEarned}")
        print("What cell would you like to flip? (row col)")
        try:
            row, col = map(int, input().split())
            row -= 1  # Adjust for 0-based indexing
            col -= 1  # Adjust for 0-based indexing
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.flip_cell(row, col)
            else:
                print("Invalid input. Please enter valid row and column indices.")
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")

    def makeLevel(self):
        self.numVoltorbs = self.player.level * 5
        self.numPoints = self.player.level * 4
        
        self.board = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

        while self.numVoltorbs > 0:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] == 1:
                self.board[row][col] = 0  # Voltorb
                self.numVoltorbs -= 1
                self.voltorbCountVertically[row] += 1
                self.voltorbCountHorizontally[col] += 1
                self.pointCountVertically[row] -= 1
                self.pointCountHorizontally[col] -= 1

        while self.numPoints > 0:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] == 1 or self.board[row][col] == 2:
                self.board[row][col] += 1  # Point
                self.numPoints -= 1
                self.pointCountVertically[row] += 1
                self.pointCountHorizontally[col] += 1


    def flip_cell(self, row, col):
        if self.flipped[row][col]:
            print("This cell has already been flipped.")
            return

        self.flipped[row][col] = True
        cell_value = self.board[row][col]

        if cell_value == 0:
            print("You flipped a Voltorb! Game over.")
            self.player.resetLevel()
            self.start()  # Restart the game
        else:
            print(f"You flipped a cell with {cell_value} point(s).")
            self.player.update_score(cell_value - 1)
            self.pointsEarned += cell_value
            if all(all(self.flipped[r][c] or self.board[r][c] == 0 or self.board[r][c] == 1 for c in range(self.cols)) for r in range(self.rows)):
                print("Congratulations! You've cleared the level.")
                self.player.next_level(self.player.score)
                self.makeLevel()  # Generate a new level
                self.flipped = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Reset flipped state


    def display_board(self):
        print(" ", end="") 
        for col in range(len(self.board[0])):
            print("   ", end="")  # Adjust spacing for column numbers
            print(col + 1, end="")  # Display the column number
        print()  # New line after column numbers
        for row in range(len(self.board)):
            print(row + 1, end="   ")  # Display the row number
            for col in range(len(self.board[row])):
                if self.flipped[row][col]:
                    print(self.board[row][col], end="   ")
                else:
                    print("X", end="   ")
            print(str(self.pointCountVertically[row]) + "/" + str(self.voltorbCountVertically[row]))  # Display the vertical count of voltorbs for this row
        print("   ", end="") 
        print(" ".join(str(self.pointCountHorizontally[col]) + "/" + str(self.voltorbCountHorizontally[col]) for col in range(len(self.board[0]))))  # Display the horizontal count of voltorbs for each column
    


class Player:
    def __init__(self):
        self.level = 1
        self.score = 0

    def update_score(self, points):
        self.score += points

    def next_level(self, points):
        self.level += 1
        self.score += points
    
    def resetLevel(self):
        self.level = 1


main()