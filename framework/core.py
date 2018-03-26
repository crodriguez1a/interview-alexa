import subprocess
import json
import os
import re

def ask_simulate(text, debug):
    """

    """
    commands = ['ask', 'simulate', '--text', text]

    if debug:
        commands.append('--debug')

    ask_simulate_response = subprocess.run(commands, stdout=subprocess.PIPE)

    # pass through exceptions from ask
    try:
        return json.loads(ask_simulate_response.stdout)
    except:
        raise Exception(ask_simulate_response.stdout)

def record_events(id, result):
    """

    """
    try:
        event_json = result['skillExecutionInfo']['invocationRequest']['body']

        # create a tmp dir if one does not exit
        if not os.path.isdir('tmp'):
            try:
                os.makedirs('tmp')
            except Exception as e:
                print(e)

        # write event_json to file with the same name as test module and function
        file = open('tmp/{}.json'.format(id), 'w+')
        with file as outfile:
            json.dump(event_json, outfile)

    except Exception as e:
        raise e

def localize(context, lambda_path='lambda/custom/handler.py'):
    """

    """
    context.local = True
    context.lambda_path = lambda_path

def has_events():
    """

    """
    for dirpath, dirnames, files in os.walk('tmp'):
        return files

def parse_response(response):
    try:
        # standard response
        return response['outputSpeech']['text']
    except:
        # delegated directive response
        return response['directives'] # TODO handle this better


def parse_ask_response(result):
    try:
        # common response node
        response = result['skillExecutionInfo']['invocationResponse']['body']['response']
        return parse_response(response)
    except:
        # error response
        return result['error']['message']

def parse_local_response(result):
    try:
        # standard response
        return response['outputSpeech']['text']
    except:
        # delegated directive response
        return response['directives'] # TODO handle this better

def ask_local(context):
    """

    """
    id = context.id()
    event_path = 'tmp/{}.json'.format(id)
    commands = ['python-lambda-local', '-f', 'lambda_handler', context.lambda_path, event_path]

    try:
        local_response = subprocess.run(commands, stdout=subprocess.PIPE)
        stdout_bytes = local_response.stdout.decode('utf8').replace("'", '"')
        result = re.findall(r'response\"\: \{([\s\S]*?)\}', stdout_bytes)
        print(result)

        return parse_response(response_json)
    except Exception as e:
        raise e

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
            ask_says = None

            if not context.record and context.local and has_events():
                return ask_local(context)
            elif context.record: # TODO context.record?
                ask_json = ask_simulate(text, debug)
                result = ask_json['result']
                record_events(context.id(), result) # TODO make the consumer aware of localization
                ask_says = parse_ask_response(result)

                return wrapped_function(context, ask_says)
            else:
                ask_json = ask_simulate(text, debug)
                result = ask_json['result'] # REVIEW Make this available to consumer?
                ask_says = parse_ask_response(result)

                return wrapped_function(context, ask_says)

            result = wrapped_function(context, ask_says)

            return result
        return _wrapper
    return _outer_wrapper
