from typing import Optional

from src.Bet import Bet
from src.GameState import GameState


class ConstantStrategy:

    @staticmethod
    def next_bet(state: GameState) -> Optional[Bet]:
        return Bet(selection=0, size=1)

    @staticmethod
    def all_in(state: GameState) -> Optional[Bet]:
        return Bet(selection="red", size=state.units)
