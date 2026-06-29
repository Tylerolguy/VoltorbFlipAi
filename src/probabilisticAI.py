class ProbabilisticAI:
    def __init__(self):
        self.name = "Probabilistic AI"

    def choose_move(self, observation):
        """
        Pick the next cell to flip.

        This method should only use public game information:
        - game.flipped
        - row point / Voltorb totals
        - column point / Voltorb totals

        It should not look directly at hidden values in game.board.
        """
        # best_row = None
        # best_col = None
        # lowest_risk = None

        # for row in range(observation["rows"]):
        #     for col in range(observation["cols"]):
        #         if observation["flipped"][row][col]:
        #             continue

        #         risk = self.estimate_risk(observation, row, col)

        #         if lowest_risk is None or risk < lowest_risk:
        #             lowest_risk = risk
        #             best_row = row
        #             best_col = col

        # self.print_choice(best_row, best_col, lowest_risk)
        # return best_row, best_col


        values = [[0 for _ in range(observation["cols"])] for _ in range(observation["rows"])]

        for row in range(observation["rows"]):
            for col in range(observation["cols"]):
                if observation["flipped"][row][col]:
                    values[row][col] = -10  # Already flipped, not a valid move

                risk = self.estimate_risk(observation, row, col)
                if risk == 0:
                    values[row][col] = self.p2(row, col, observation) * 3 + 6
                else:
                    values[row][col] = self.p2(row, col, observation) * 3 - risk * 8
        
        best_row = None
        best_col = None
        best_value = None
        #finds the highest value in the values array and returns the row and col of that value
        for row in range(observation["rows"]):
            for col in range(observation["cols"]):
                if observation["flipped"][row][col]:
                    continue

                if best_value is None or values[row][col] > best_value:
                    best_value = values[row][col]
                    best_row = row
                    best_col = col
        
        self.print_choice(best_row, best_col, best_value)
        return best_row, best_col


    def p2(self, row, col, observation):
        #how many points are left in this row/col
        rowPointsLeft = observation["row_points"][row] - sum(observation["visible_board"][row][c] for c in range(observation["cols"]) if observation["flipped"][row][c])
        colPointsLeft = observation["col_points"][col] - sum(observation["visible_board"][r][col] for r in range(observation["rows"]) if observation["flipped"][r][col])

        #this is the number of hidden cells that contain points in this row/col
        numberOfHiddenCellsInRow = sum(1 for c in range(observation["cols"]) if not observation["flipped"][row][c]) - observation["row_voltorbs"][row]
        numberOfHiddenCellsInCol = sum(1 for r in range(observation["rows"]) if not observation["flipped"][r][col]) - observation["col_voltorbs"][col]

        if numberOfHiddenCellsInRow == 0 or numberOfHiddenCellsInCol == 0:
            return 0
        elif rowPointsLeft == 0 or colPointsLeft == 0:
            return 0 
        elif rowPointsLeft - numberOfHiddenCellsInRow > 0 and colPointsLeft - numberOfHiddenCellsInCol > 0:
            return max(rowPointsLeft / numberOfHiddenCellsInRow, colPointsLeft / numberOfHiddenCellsInCol)
        else:
            return 0
        
    def estimate_risk(self, observation, row, col):
        """
        Estimate how likely a hidden cell is to contain a Voltorb.

        First version idea:
        row risk = remaining Voltorbs in this row / hidden cells in this row
        col risk = remaining Voltorbs in this column / hidden cells in this column
        final risk = average of row risk and col risk
        """

        row_voltorbs = observation["row_voltorbs"][row]
        col_voltorbs = observation["col_voltorbs"][col]
        if row_voltorbs == 0 or col_voltorbs == 0:
            return 0.0  # No risk if there are no Voltorbs in the row or column

        hidden_row_cells = sum(1 for c in range(observation["cols"]) if not observation["flipped"][row][c])
        hidden_col_cells = sum(1 for r in range(observation["rows"]) if not observation["flipped"][r][col])

        row_risk = row_voltorbs / hidden_row_cells if hidden_row_cells > 0 else 0
        col_risk = col_voltorbs / hidden_col_cells if hidden_col_cells > 0 else 0
        return max(row_risk, col_risk)  # Use the maximum risk as the final estimate

    def print_choice(self, row, col, risk=None):
        """
        Print the AI's selected move.

        This is useful while testing so you can see what the AI is doing.
        """
        if risk is None:
            print(f"{self.name} chooses row {row + 1}, column {col + 1}.")
        else:
            print(f"{self.name} chooses row {row + 1}, column {col + 1} with risk {risk:.2f}.")
