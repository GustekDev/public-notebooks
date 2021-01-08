import random
from typing import Union, Callable, Optional

from src.GameState import GameState, Bet
from src.strategies.ExitStrategy import ExitStrategy


class Roulette:

    RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    BLACK = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

    @staticmethod
    def play(
        next_bet: Callable[[GameState], Optional[Bet]],
        end_of_game: Callable[[GameState], bool] = ExitStrategy.exit,
        initial_units: int = 1000
    ) -> GameState:
        state = GameState.initial_state(initial_units)
        bet = next_bet(state)

        while state.can_play(bet) and not end_of_game(state):
            state = state.place_bets(bet)
            winning_number = Roulette.roll()
            state = state.end_of_round(
                winning_number,
                Roulette.evaluate(state.bet.selection, winning_number) if bet else 0
            )
            bet = next_bet(state)

        return state

    @staticmethod
    def evaluate(selection: Union[int, str], winning_number: int) -> int:
        if winning_number == selection:
            return 36

        if (selection == "red" and Roulette.is_red(winning_number)) \
                or (selection == "black" and Roulette.is_black(winning_number)):
            return 2

        return 0

    @staticmethod
    def roll() -> int:
        return random.randint(0, 36)

    @staticmethod
    def is_red(n: int) -> bool:
        return n in Roulette.RED

    @staticmethod
    def is_black(n: int) -> bool:
        return n in Roulette.BLACK
