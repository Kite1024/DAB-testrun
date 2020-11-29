import unittest

from lib import Cell, GameState


class Tests(unittest.TestCase):

    def test_cell(self):
        assert Cell('.').is_empty()
        assert not Cell('.').is_occupied()
        assert not Cell('.').is_pawn()
        assert not Cell('.').is_wall()
        assert not Cell('.').is_trail()
        assert Cell('.').char() == '.'

        assert not Cell('X').is_empty()
        assert Cell('X').is_occupied()
        assert Cell('X').is_pawn()
        assert not Cell('X').is_wall()
        assert not Cell('X').is_trail()
        assert Cell('X').char() == 'X'

        assert not Cell('o').is_empty()
        assert Cell('o').is_occupied()
        assert not Cell('o').is_pawn()
        assert not Cell('o').is_wall()
        assert Cell('o').is_trail()
        assert Cell('o').char() == 'o'

        assert not Cell('#').is_empty()
        assert Cell('#').is_occupied()
        assert not Cell('#').is_pawn()
        assert Cell('#').is_wall()
        assert not Cell('#').is_trail()
        assert Cell('#').char() == '#'

        assert not Cell('*').is_empty()
        assert Cell('*').is_occupied()
        assert not Cell('*').is_pawn()
        assert not Cell('*').is_wall()
        assert Cell('*').is_trail()
        assert Cell('*').char() == '*'

    def test_gamestate(self):
        s = GameState("###########...aaaA.##..B.....##..bbb...###########", 10, 5, 'A')
        self.assertEqual(s.pawn_column(), 7)
        self.assertEqual(s.pawn_row(), 1)
        self.assertEqual(s.cell(2, 8).char(), '.')
        self.assertRaises(ValueError, s.cell, -2, 2)
        self.assertEqual(s.cell_safe(-2, 2).char(), '#')
        self.assertEqual(s.cell_safe(2, 8).char(), '.')
        self.assertEqual(s.field_width(), 10)
        self.assertEqual(s.field_height(), 5)
