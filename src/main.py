

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


    def start(self, mode="human"):
      
      self.makeLevel()
        # Game logic here
      if mode == "human":
          self.play_human() 

    def apply_move(self, row, col):
        result = self.flip_cell(row, col)
        if self.beatLevel():
            self.player.next_level(self.player.score)
            self.makeLevel()  # Generate a new level
            self.flipped = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Reset flipped state
            return 5
        if result == 0:
            return -1  # Game over
        elif result > 0:
            self.player.update_score(result - 1)
            self.pointsEarned += result
            return result
       
      
    def play_human(self):
        while True:
            self.display_board()
            print(f"Level: {self.player.level}, Score: {self.player.score}, Points Earned: {self.pointsEarned}")
            print("What cell would you like to flip? (row col)")
            try:
                row, col = map(int, input().split())
                row -= 1  # Adjust for 0-based indexing
                col -= 1  # Adjust for 0-based indexing
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    result = self.flip_cell(row, col)
                    if result == 0:
                        print("You hit a Voltorb! Game over.")
                        break

                    elif result > 0:
                        self.player.update_score(result - 1)
                        self.pointsEarned += result
                    elif result == -1:
                        print("This cell has already been flipped. Please choose another cell.")
                    if self.beatLevel():
                        print("Congratulations! You've cleared the level.")
                        self.player.next_level(self.player.score)
                        self.makeLevel()  # Generate a new level
                        self.flipped = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Reset flipped state
                else:
                    print("Invalid input. Please enter valid row and column indices.")
            except ValueError:
                print("Invalid input. Please enter two integers separated by a space.")





    def makeLevel(self):
        self.numVoltorbs = self.player.level * 2 + 3
        self.numPoints = self.player.level * 2 + 2
        self.voltorbCountVertically = [0] * self.rows
        self.voltorbCountHorizontally = [0] * self.cols
        self.pointCountVertically = [5] * self.rows
        self.pointCountHorizontally = [5] * self.cols

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


    def beatLevel(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] > 1 and not self.flipped[row][col]:
                    return False
        return True

    def flip_cell(self, row, col):
        if self.flipped[row][col]:
            return -1

        self.flipped[row][col] = True
        return self.board[row][col]

        

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


if __name__ == "__main__":
    main()
