from dataclasses import replace
from typing import Optional

from src.Bet import Bet
from src.GameState import GameState, RoundResult


class Martingale:

    @staticmethod
    def classic(state: GameState) -> Optional[Bet]:
        if len(state.history) == 0:
            return Bet(selection="red", size=1)

        last_round = state.history[-1]
        if last_round.result == RoundResult.LOSS:
            return replace(last_round.bet, size=last_round.bet.size * 2)

        return Bet(selection="red", size=1)
