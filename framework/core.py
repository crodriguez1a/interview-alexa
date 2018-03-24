import subprocess
import json

def test_utterance(text, debug=False):
    """
    Usage:

    @test_utterance("Alexa, open my skill")
    def my_test(self, result):
        self.assertEqual(result, 'My exected result')

    """
    def _outer_wrapper(wrapped_function):
        def _wrapper(*args, **kwargs):
            commands = ['ask', 'simulate', '--text', text]

            if debug:
                commands.append('--debug')

            ask_cli = subprocess.run(commands, stdout=subprocess.PIPE)

            # pass through exceptions from ask
            try:
                ask_json = json.loads(ask_cli.stdout)
            except:
                raise Exception(ask_cli.stdout)

            try:
                ask_says = ask_json['result']['skillExecutionInfo']['invocationResponse']['body']['response']['outputSpeech']['text']
            except:
                ask_says = ask_json['result']['error']['message']

            _self = args[0]
            result = wrapped_function(_self, ask_says)

            return result
        return _wrapper
    return _outer_wrapper
