from src.GameState import GameState


class ExitStrategy:

    @staticmethod
    def exit(state: GameState) -> bool:
        return state.units >= state.initial_units * 2
