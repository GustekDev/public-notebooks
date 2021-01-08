from dataclasses import replace
from typing import Optional

from src.Bet import Bet
from src.GameState import GameState, RoundResult


class Gustek:

    @staticmethod
    def next_bet(state: GameState) -> Optional[Bet]:
        if len(state.history) == 0:
            return Bet(selection=1, size=1)

        last_round = state.history[-1]
        if last_round.result == RoundResult.LOSS:
            if state.round % 15 == 0:
                return replace(state.bet, size=last_round.bet.size * 2)
            else:
                return last_round.bet

        return Bet(selection=1, size=1)
