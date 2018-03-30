import unittest
from unittest import mock
from urllib.error import HTTPError
import os
import shutil

from interview_alexa import say, InterviewAlexa

class TestInterviewAlexa(unittest.TestCase):

    def setUp(self):
        self.ask_success = {
            'result': {
                'skillExecutionInfo': {
                    'invocationRequest': {
                        'body': {
                            "version": "1.0",
                            "session":  {}
                        }
                    },
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

    def test_recording_events(self):
        InterviewAlexa.ask_simulate = mock.MagicMock(return_value=self.ask_success)
        InterviewAlexa.record(InterviewAlexa, self)

        @say('hi')
        def t(self, result):
            self.assertEqual(result, 'and hello to you')

        t(self)

        self.assertTrue(self.record)
        # tmp directory was created
        self.assertTrue(os.path.isdir('tmp'))

        # file was written to tmp folder
        filename = '__main__.TestInterviewAlexa.test_recording_events.json'
        for dirpath, dirnames, files in os.walk('tmp'):
            self.assertTrue(filename in files)

        # event contents were written to file
        contents = '{"version": "1.0", "session": {}}'
        event_json = open('tmp/{}'.format(filename), 'r')
        self.assertEqual(contents, event_json.read())
        event_json.close()

        shutil.rmtree('tmp')


    def test_localized_testing(self):
        InterviewAlexa.ask_simulate = mock.MagicMock(return_value=self.ask_success)
        InterviewAlexa.localize(InterviewAlexa, self, 'fake_lambda.py')

        @say('hi')
        def t(self, result):
            self.assertEqual(result, 'and hello to you')

        # cannot localize in without having recorded
        with self.assertRaises(Exception):
            t(self)

        self.assertTrue(self.local)
        self.assertEqual(self.lambda_path, 'fake_lambda.py')

        # tmp record
        InterviewAlexa.record(InterviewAlexa, self)
        # cannot record in localized mode
        with self.assertRaises(Exception):
            t(self)






if __name__ == '__main__':
    unittest.main()
