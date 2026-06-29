from main import Game, Player


class VoltorbFlipEnvironment:
    def __init__(self, ai):
        self.ai = ai
        self.player = Player()
        self.game = Game(self.player)
        self.game.makeLevel()
        self.done = False

    def reset(self):
        """
        Start a fresh game for the current AI.
        """
        self.player = Player()
        self.game = Game(self.player)
        self.game.makeLevel()
        self.done = False
        return self.get_observation()

    def get_summary(self):
        """
        Return basic results from the current run.
        """
        return {
            "level": self.player.level,
            "score": self.player.score,
            "points_earned": self.game.pointsEarned,
            "done": self.done,
        }

    def get_observation(self):
        """
        Create the public game state the AI is allowed to see.

        Hidden cells are shown as None. Revealed cells show their true value.
        """
        visible_board = []

        for row in range(self.game.rows):
            visible_row = []
            for col in range(self.game.cols):
                if self.game.flipped[row][col]:
                    visible_row.append(self.game.board[row][col])
                else:
                    visible_row.append(None)
            visible_board.append(visible_row)

        return {
            "rows": self.game.rows,
            "cols": self.game.cols,
            "visible_board": visible_board,
            "flipped": self.game.flipped,
            "row_points": self.game.pointCountVertically,
            "row_voltorbs": self.game.voltorbCountVertically,
            "col_points": self.game.pointCountHorizontally,
            "col_voltorbs": self.game.voltorbCountHorizontally,
        }

    def render(self):
        """
        Display the current board state.
        """
        self.game.display_board()
        print(f"Level: {self.player.level}, Score: {self.player.score}, Points Earned: {self.game.pointsEarned}")

    def step(self, move):
        """
        Apply one AI move to the game.

        The move should be a tuple: (row, col), using 0-based indexes.
        """
        row, col = move
        result = self.game.apply_move(row, col)
        if result == -1:
            self.done = True

        return self.get_observation(), result, self.done

    def run_turn(self):
        """
        Ask the AI for one move, then apply that move.
        """
        observation = self.get_observation()
        move = self.ai.choose_move(observation)
        return self.step(move)

    def run_game(self, max_turns=None, render_each_turn=False):
        """
        Keep running AI turns until the game ends.
        """
        turns = 0

        while not self.done:
            if max_turns is not None and turns >= max_turns:
                break

            self.run_turn()
            turns += 1

            if render_each_turn:
                print()
                print(f"After turn {turns}:")
                self.render()

        return self.get_observation(), self.get_summary()
