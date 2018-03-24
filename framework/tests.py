import unittest
from core import test_utterance


class TestingAllTheThings(unittest.TestCase):

    @test_utterance('open my skill')
    def test_launch_intent(self, result):
        self.assertEqual(result, "My expected result")


if __name__ == '__main__':
    unittest.main()
