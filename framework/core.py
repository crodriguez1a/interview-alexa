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
            # print(ask_cli)

            # pass through exceptions from ask
            try:
                ask_json = json.loads(ask_cli.stdout)
            except:
                raise Exception(ask_cli.stdout)

            # capture the entire the result
            # REVIEW Make this available to consumer?
            result = ask_json['result']

            try:
                # common response node
                response = result['skillExecutionInfo']['invocationResponse']['body']['response']

                try:
                    # standard response
                    ask_says = response['outputSpeech']['text']
                except:
                    # delegated directive response
                    # TODO handle this
                    ask_says = response['directives']
            except:
                # error response
                ask_says = result['error']['message']

            _self = args[0]
            result = wrapped_function(_self, ask_says)

            # REVIEW consider carrying the event foward as a temporary file to attempt idempotency
            return result
        return _wrapper
    return _outer_wrapper
