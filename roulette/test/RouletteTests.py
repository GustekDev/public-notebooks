import unittest
import random

import mock

from src.GameState import RoundResult
from src.Roulette import Roulette
from src.strategies.ConstantStrategy import ConstantStrategy
from src.strategies.Martingale import Martingale


class RouletteTests(unittest.TestCase):
    @mock.patch('random.randint')
    def test_no_win(self, mock_random):
        mock_random.return_value = 1
        result = Roulette.play(
            next_bet=ConstantStrategy.next_bet,
            initial_units=10
        )
        self.assertEqual(0, result.units)
        self.assertEqual(10, len(result.history))

    @mock.patch('random.randint')
    def test_all_in_loss(self, mock_random):
        mock_random.return_value = 2
        result = Roulette.play(
            next_bet=ConstantStrategy.all_in,
            initial_units=10
        )
        self.assertEqual(0, result.units)
        self.assertEqual(1, len(result.history))

    @mock.patch('random.randint')
    def test_all_win(self, mock_random):
        mock_random.return_value = 0
        result = Roulette.play(
            next_bet=ConstantStrategy.next_bet,
            initial_units=200
        )
        self.assertEqual(410, result.units)
        self.assertEqual(6, len(result.history))

    def test_evaluate_single_number_win(self):
        for i in range(37):
            self.assertEqual(36, Roulette.evaluate(i, i))

    def test_evaluate_single_number_loss(self):
        for i in range(37):
            self.assertEqual(0, Roulette.evaluate(i, i+1))

    def test_evaluate_colour_win(self):
        red_number = random.sample(Roulette.RED, 1)[0]
        black_number = random.sample(Roulette.BLACK, 1)[0]
        self.assertEqual(2, Roulette.evaluate("red", red_number))
        self.assertEqual(2, Roulette.evaluate("black", black_number))

    def test_evaluate_colour_loss(self):
        red_number = random.sample(Roulette.RED, 1)[0]
        black_number = random.sample(Roulette.BLACK, 1)[0]
        self.assertEqual(0, Roulette.evaluate("black", red_number))
        self.assertEqual(0, Roulette.evaluate("red", black_number))

    def test_evaluate_colour_loss_when_zero(self):
        self.assertEqual(0, Roulette.evaluate("black", 0))
        self.assertEqual(0, Roulette.evaluate("red", 0))

    @mock.patch('random.randint')
    def test_martingale_all_win(self, mock_random):
        mock_random.return_value = random.sample(Roulette.RED, 1)[0]
        result = Roulette.play(
            next_bet=Martingale.classic,
            initial_units=10
        )
        self.assertEqual(20, result.units)
        self.assertEqual(10, len(result.history))

    @mock.patch('random.randint')
    def test_martingale_all_loss(self, mock_random):
        mock_random.return_value = random.sample(Roulette.BLACK, 1)[0]
        result = Roulette.play(
            next_bet=Martingale.classic,
            initial_units=10
        )
        self.assertEqual(3, result.units)
        self.assertEqual(3, len(result.history))

    @mock.patch('random.randint')
    def test_martingale_3_loss_and_8_win(self, mock_random):
        mock_random.side_effect = random.sample(Roulette.BLACK, 2) + [0] + random.sample(Roulette.RED, 15)
        result = Roulette.play(
            next_bet=Martingale.classic,
            initial_units=15
        )
        self.assertEqual(30, result.units)
        self.assertEqual(18, len(result.history))
        self.assertEqual(1, result.history[0].bet.size)
        self.assertEqual(2, result.history[1].bet.size)
        self.assertEqual(4, result.history[2].bet.size)
        self.assertEqual(8, result.history[3].bet.size)
        self.assertEqual(RoundResult.LOSS, result.history[0].result)
        self.assertEqual(RoundResult.LOSS, result.history[1].result)
        self.assertEqual(RoundResult.LOSS, result.history[2].result)
        self.assertEqual(RoundResult.WIN, result.history[3].result)
        for r in result.history[4:]:
            self.assertEqual(1, r.bet.size)
            self.assertEqual(RoundResult.WIN, r.result)


if __name__ == '__main__':
    unittest.main()
