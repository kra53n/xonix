import unittest

from utils import lispy


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
            {'action': {'player': 'up', 'enemies': (1, 2, 3)}},
            '(action ((player up) (enemies (1 2 3))))',
        ),
    )

    def test_lispy(self):
        for lhs, rhs in self.cases:
            self.assertEqual(lispy(lhs), rhs)


if __name__ == '__main__':
    # test_lispy()
    unittest.main()
