import unittest
from interview_alexa import test_utterance


class TestInterviewAlexa(unittest.TestCase):

    def test_decorator(self):

        @test_utterance('hello world')
        def foo(self, result):
            self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
