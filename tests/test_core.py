import unittest
from unittest import mock
from urllib.error import HTTPError

from interview_alexa.core import say, InterviewAlexa

class TestInterviewAlexa(unittest.TestCase):

    def setUp(self):
        self.ask_success = {
            'result': {
                'skillExecutionInfo': {
                    'invocationResponse': {
                        'body': {
                            'response': {
                                'outputSpeech': {
                                    'text': 'and hello to you'
                                }
                            }
                        }
                    }
                }
            }
        }

        self.ask_error = {
            'result': {
                'error': {
                    'message': 'derp'
                }
            }
        }

        self.ask_directives = {
            'result': {
                'skillExecutionInfo': {
                    'invocationResponse': {
                        'body': {
                            'response': {
                                'directives': [
                                    {'type': 'Dialog.Delegate'}
                                ]
                            }
                        }
                    }
                }
            }
        }

        InterviewAlexa.ask_simulate = mock.MagicMock(return_value=self.ask_success)

    def test_decorator(self):
        @say('hello world')
        def t(self, result):
            self.assertIsNone(result)

        assert callable(t)

    def test_returns_skill_output(self):
        @say('hi')
        def t(self, result):
            self.assertEqual(result, 'and hello to you')

        assert callable(t)
        t(self)

    def test_returns_skill_error(self):
        InterviewAlexa.ask_simulate = mock.MagicMock(return_value=self.ask_error)

        @say('hi')
        def t(self, result):
            self.assertEqual(result, 'derp')

        t(self)

    def test_returns_directives(self):
        InterviewAlexa.ask_simulate = mock.MagicMock(return_value=self.ask_directives)

        @say('hi')
        def t(self, result):
            self.assertEqual(result, [{'type': 'Dialog.Delegate'}])

        t(self)

    def test_raises_exception_after_ask_cli_error(self):
        mock_ask_simulate = mock.MagicMock(return_value=self.ask_success)
        mock_ask_simulate.side_effect = HTTPError('foo.com', '404', 'not-found', {}, None)
        InterviewAlexa.ask_simulate = mock_ask_simulate

        @say('hi')
        def t(self, result):
            pass

        with self.assertRaises(HTTPError):
            t(self)






if __name__ == '__main__':
    unittest.main()
