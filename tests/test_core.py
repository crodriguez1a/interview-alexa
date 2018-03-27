import unittest
from interview_alexa import say


class TestInterviewAlexa(unittest.TestCase):

    def test_decorator(self):

        @say('hello world')
        def foo(self, result):
            self.assertIsNone(result)

    # TODO 


if __name__ == '__main__':
    unittest.main()
