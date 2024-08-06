import unittest
import highlowlogic


class TestHighLow(unittest.TestCase):
    """Runs tests"""

    def gen_game(self, players=['joe', 'marc']):
        test_game = highlowlogic.Game(players, 2, 2)
        return(test_game)

    def test_player_name_and_index(self):
        """Tests players name and index"""
        players = ["a", "Joe", "marc"]
        test_game = self.gen_game(players)
        for i in range(len(players)):
            test_game.curr_player_index = i
            player_test_name = test_game.get_current_player().name
            self.assertEqual(player_test_name, players[i])

    def test_cards(self):
        # Makes sure cards are not > 13
        test_game = self.gen_game()
        card = test_game.deck.draw_card()[0]
        self.assertLessEqual(card.value, 12)
        self.assertGreaterEqual(card.value, 0)

    def test_guess_higher(self):
        test_game = self.gen_game()
        for i in range(53):
            prev_card = test_game.curr_card
            result = test_game.player_choice(
                "higher", test_game.get_current_player().name)
            next_card = test_game.curr_card

            if result == True:
                self.assertGreater(next_card.value, prev_card.value)
            else:
                self.assertLessEqual(next_card.value, prev_card.value)

    def test_guess_lower(self):
        test_game = self.gen_game()
        for i in range(53):
            prev_card = test_game.curr_card
            result = test_game.player_choice(
                "lower", test_game.get_current_player().name)
            next_card = test_game.curr_card

            if result == True:
                self.assertLess(next_card.value, prev_card.value)
            else:
                self.assertGreaterEqual(next_card.value, prev_card.value)

    def test_bank(self):
        test_game = self.gen_game()
        result = test_game.player_choice(
            "bank", test_game.get_current_player().name)
        self.assertEqual(test_game.curr_player_guesses, 0)
        # True because bank failed and player is still playing
        self.assertTrue(result)
        test_game.curr_player_guesses = 1
        test_game.stack_size = 2

        result = test_game.player_choice(
            "bank", test_game.get_current_player().name)
        self.assertEqual(test_game.players[test_game.curr_player_index-1].bank,
                         (500 + 2*test_game.card_reward))
        self.assertFalse(result)

    def test_swap(self):
        test_game = self.gen_game()
        for i in range(1):
            curr_card = test_game.get_current_card()
            curr_player_bal = test_game.get_current_player().bank
            result = test_game.player_choice(
                "swap", test_game.get_current_player().name)
            self.assertTrue(result)
            if curr_player_bal > test_game.swap_cost:
                self.assertEqual(test_game.get_current_player(
                ).bank, curr_player_bal - test_game.swap_cost)
                self.assertNotEqual(curr_card, test_game.get_current_card())
            else:
                self.assertEqual(curr_card, test_game.get_current_card())

    def test_incorrect_choice(self):
        with self.assertRaises(ValueError):
            test_game = self.gen_game()
            test_game.player_choice(
                'incorrect', test_game.get_current_player().name)

    def test_highscore(self):
        test_game = self.gen_game()
        test_game.players[0].bank = 1000
        test_game.players[1].bank = 1200
        scoreboard = test_game.get_winner()
        self.assertGreaterEqual(scoreboard[0].bank, scoreboard[1].bank)
        self.assertEqual(scoreboard[0].bank, 1200)
        self.assertEqual(scoreboard[1].bank, 1000)

if __name__ == "__main__":
    unittest.main()
