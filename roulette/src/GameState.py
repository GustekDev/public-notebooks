from __future__ import annotations

from dataclasses import dataclass, replace
from typing import List, Optional
from enum import Enum

from src.Bet import Bet


class RoundResult(Enum):
    WIN = 1
    LOSS = 2


@dataclass()
class RoundHistory:
    winning_number: int
    result: RoundResult
    bet: Bet
    round: int
    units: int


@dataclass()
class GameState:
    initial_units: int
    units: int
    bet: Optional[Bet]
    round: int
    history: List[RoundHistory]

    def place_bets(self, bet: Bet) -> GameState:
        return replace(
            self, bet=bet, units=self.units - bet.size, round=self.round + 1
        ) if bet else replace(
            self, bet=bet, round=self.round + 1
        )

    def end_of_round(self, winning_number: int, win_odds: int) -> GameState:
        if self.bet and win_odds > 0:
            new_units = self.units + self.bet.size * win_odds
            return replace(
                self,
                units=new_units,
                bet=None,
                history=self.history + [RoundHistory(winning_number, RoundResult.WIN, self.bet, self.round, new_units)]
            )

        return replace(
            self,
            bet=None,
            history=self.history + [RoundHistory(winning_number, RoundResult.LOSS, self.bet, self.round, self.units)]
        )

    def can_play(self, bet: Bet) -> bool:
        return self.units >= bet.size and self.units > 0 if bet else True

    @staticmethod
    def initial_state(initial_units: int = 1000) -> GameState:
        return GameState(initial_units, initial_units, Bet(0, 0), 0, [])
