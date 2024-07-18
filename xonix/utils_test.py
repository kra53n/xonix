import unittest

from utils import lispy, unlispy


class TestLispies(unittest.TestCase):
    cases = (
        (
            'accept',
            '(accept)',
        ),
        (
            {'action': {'player': 'up'}},
            '(action (player up))',
        ),
        (
            {'action': {'player': 'up', 'enemy': 'left'}},
            '(action ((player up) (enemy left)))',
        ),
        (
            {'action': {'enemies': ['1', '2', '3'], 'player': 'up'}},
            '(action ((enemies (1 2 3)) (player up)))',
        ),
    )

    def test_lispy(self):
        for lhs, rhs in self.cases:
            self.assertEqual(lispy(lhs), rhs)

    def test_unlispy(self):
        self.assertEqual({'accept': None}, unlispy(self.cases[0][1]))
        for lhs, rhs in self.cases[1:]:
            self.assertEqual(lhs, unlispy(rhs))


if __name__ == '__main__':
    unittest.main()
