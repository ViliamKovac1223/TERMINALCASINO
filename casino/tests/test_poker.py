import pytest
import os
import sys

# Allow imports from given directory as well
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from games.poker.poker import deal_card, hand_score, evaluate_hand, get_partial_hand_score, get_card_value, hand_name
from games.poker.poker import FULL_DECK


class TestPoker:
    @pytest.mark.parametrize("turn", [
        ([]),
        ([(6, 'd6')]),
    ])
    def test_deal_card(self, turn):
        deck = FULL_DECK.copy()
        for t in turn:
            deck.remove(t)
        deal_card(turn, deck)

        # If amount of cards isn't enough, fail the test
        if len(turn) + len(deck) != len(FULL_DECK):
            assert False

        # If cards from the turn is in the deck, fail the test
        for t in turn:
            if t in deck:
                assert False

        assert True

    @pytest.mark.parametrize("turn, board, answer", [
        ([(2, 'c2'), (3, 'c3'),],
            [(10, 'c10'), ('J', 'dJ'), ('Q', 'dQ'), ('K', 'dK'), ('A', 'dA')],
            5),
        ([(2, 'c2'), (3, 'c3'),],
            [(4, 'c4'), (5, 'd5'), (6, 'd6'), (7, 'd7'), (8, 'd8')],
            5),
        ([('A', 'cA'), ('K', 'cK'),],
            [(10, 'c10'), ('J', 'cJ'), ('Q', 'cQ'), ('K', 'dK'), ('A', 'dA')],
            9),
    ])
    def test_hand_score(self, turn, board, answer):
        assert hand_score(turn, board) == answer

    @pytest.mark.parametrize("cards, answer", [
            ([(10, 'c10'), ('J', 'dJ'), ('Q', 'dQ'), ('K', 'dK'), ('A', 'dA')],
            5),
            ([(4, 'c4'), (5, 'd5'), (6, 'd6'), (7, 'd7'), (8, 'd8')],
            5),
            ([(10, 'c10'), ('J', 'cJ'), ('Q', 'cQ'), ('K', 'cK'), ('A', 'cA')],
            9),
    ])
    def test_evaluate_hand(self, cards, answer):
        assert evaluate_hand(cards) == answer

    @pytest.mark.parametrize("cards, answer", [
            ([(10, 'c10'), ('J', 'dJ')],
            1),
            ([(10, 'c10'), (10, 'd10'), (10, 'h10'), (10, 's10')],
            8),
            ([(10, 'd10'), (10, 'h10'), (10, 's10')],
            4),
            ([(10, 'd10'), (10, 'h10'), (9, 's9'), (9, 'd9')],
            3),
            ([(10, 'd10'), (10, 'h10')],
            2),
    ])
    def test_partial_hand_score(self, cards, answer):
        assert get_partial_hand_score(cards) == answer

    @pytest.mark.parametrize("card, answer", [
        (10, 10),
        ('J', 11),
        ('Q', 12),
        ('K', 13),
        ('A', 14),
    ])
    def test_card_value(self, card, answer):
        assert get_card_value(card) == answer

    @pytest.mark.parametrize("hand, answer", [
        (9, "Straight Flush"),
        (8, "Four of a Kind"),
        (7, "Full House"),
        (6, "Flush"),
        (5, "Straight"),
        (4, "Three of a Kind"),
        (3, "Two Pair"),
        (2, "One Pair"),
        (1, "High Card")
    ])
    def test_hand_name(self, hand, answer):
        assert hand_name(hand) == answer
