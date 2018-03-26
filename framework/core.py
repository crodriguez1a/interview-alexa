import subprocess
import json
import os.path




def ask_simulate(text, debug):
    commands = ['ask', 'simulate', '--text', text]

    if debug:
        commands.append('--debug')

    ask_simulate_response = subprocess.run(commands, stdout=subprocess.PIPE)

    # pass through exceptions from ask
    try:
        return json.loads(ask_simulate_response.stdout)
    except:
        raise Exception(ask_simulate_response.stdout)

def record_events(context, result):
    events = context.events
    id = context.id()
    try:
        invocation_request = result['skillExecutionInfo']['invocationRequest']['body']
        # REVIEW tmp file?
        event_json = json.dumps(invocation_request, sort_keys=True, indent=2)
        events.append({ id: event_json }) # TODO output message recording events
    except:
        pass

def localize(context, lamda_path='lamda/custom/handler.py'):
    context.local = True
    context.events = []
    context.lamda_path = lamda_path

def test_local(context):
    event = context.events[context.id()]
    print('event', event)
    # write tmp file, dump event into file, then run...
    # python-lambda-local -f lambda_handler lambda/custom/handler.py test_event.json

def test_utterance(text, debug=False):
    """
    Usage:

    @test_utterance("Alexa, open my skill")
    def my_test(self, result):
        self.assertEqual(result, 'My exected result')

    """
    def _outer_wrapper(wrapped_function):
        def _wrapper(*args, **kwargs):
            context = args[0]

            if context.local and context.events:
                # TODO we need the index events[]
                test_local(context)
            elif context.local:
                ask_json = ask_simulate(text, debug)
                result = ask_json['result']
                record_events(context.events, result) # TODO make the consumer aware of localization
            else:
                ask_json = ask_simulate(text, debug)
                result = ask_json['result'] # REVIEW Make this available to consumer?

            try:
                # common response node
                response = result['skillExecutionInfo']['invocationResponse']['body']['response']

                try:
                    # standard response
                    ask_says = response['outputSpeech']['text']
                except:
                    # delegated directive response
                    ask_says = response['directives'] # TODO handle this better
            except:
                # error response
                ask_says = result['error']['message']

            result = wrapped_function(context, ask_says)

            return result
        return _wrapper
    return _outer_wrapper
