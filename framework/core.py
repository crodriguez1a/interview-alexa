import subprocess
import json

def test_utterance(text):
    """
    Usage:

    @test_utterance("Alexa, open my skill")
    def my_test(self, result):
        self.assertEqual(result, 'My exected result')

    """
    def _outer_wrapper(wrapped_function):
        def _wrapper(*args, **kwargs):
            ask_cli = subprocess.run(['ask', 'simulate', '--text', text], stdout=subprocess.PIPE)
            ask_json = json.loads(ask_cli.stdout)
            ask_says = ask_json['result']['skillExecutionInfo']['invocationResponse']['body']['response']['outputSpeech']['text']
            _self = args[0]
            result = wrapped_function(_self, ask_says)
            return result
        return _wrapper
    return _outer_wrapper
