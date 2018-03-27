import unittest
from interview_alexa import say


class TestingAllTheThings(unittest.TestCase):

    @say('open my skill')
    def test_launch_intent(self, result):
        self.assertEqual(result, "My expected result")


if __name__ == '__main__':
    unittest.main()
