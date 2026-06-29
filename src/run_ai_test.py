from environment import VoltorbFlipEnvironment
from probabilisticAI import ProbabilisticAI


def main():
    ai = ProbabilisticAI()
    environment = VoltorbFlipEnvironment(ai)

    print("Starting board:")
    environment.render()

    observation, summary = environment.run_game(max_turns=100, render_each_turn=True)

    print("AI test complete.")
    print(f"Final level: {summary['level']}")
    print(f"Final score: {summary['score']}")
    print(f"Points earned: {summary['points_earned']}")
    print(f"Game over: {summary['done']}")


if __name__ == "__main__":
    main()
