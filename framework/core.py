import subprocess
import json
import os
import re

def ask_simulate(text, debug):
    """
    Run `ask simulate`
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
    Write event json response to tmp file
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
    Signal that local tests should be
    executed against recorded events
    """
    context.local = True
    context.lambda_path = lambda_path

def record(context):
    """
    Signal that events should be recorded
    """
    context.record = True

def has_events():
    """
    Signal if events were recorded
    """
    for dirpath, dirnames, files in os.walk('tmp'):
        return files

def parse_response(response):
    """
    Parse common response object
    """
    try:
        # standard response
        return response['outputSpeech']['text']
    except:
        # delegated directive response
        return response['directives'] # TODO handle this better


def parse_ask_response(result):
    """
    Parse response shape from ask cli
    """
    try:
        # common response node
        response = result['skillExecutionInfo']['invocationResponse']['body']['response']
        return parse_response(response)
    except:
        # error response
        return result['error']['message']

def parse_local_response(result):
    """
    Parse response shape from `python-lambda-local`
    """
    try:
        # standard response
        return response['outputSpeech']['text']
    except:
        # delegated directive response
        return response['directives'] # TODO handle this better

def ask_local(context):
    """
    Run `python-lambda-local` against recorded events
    """
    id = context.id()
    event_path = 'tmp/{}.json'.format(id)
    commands = ['python-lambda-local', '-f', 'lambda_handler', context.lambda_path, event_path]
    local_response = subprocess.run(commands, stdout=subprocess.PIPE)

    try:
        # decode bytes
        bytes_response = local_response.stdout.decode('utf8')
        # extract result node
        result = re.findall(r'RESULT\:([\s\S]*?)\[root', bytes_response)

        if result:
            result_dict = eval(result[0])
        
            try:
                return result_dict['response']['outputSpeech']['text']
            except:
                return result_dict['response']

    except:
        raise Exception(local_response.stdout)

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
            record = context.__dict__.get('record', None)
            local = context.__dict__.get('local', None)

            ask_says = None

            if not record and local and has_events():
                ask_says = ask_local(context)
                return wrapped_function(context, ask_says)

            elif record: # TODO context.record?
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

            return wrapped_function(context, ask_says)
        return _wrapper
    return _outer_wrapper
