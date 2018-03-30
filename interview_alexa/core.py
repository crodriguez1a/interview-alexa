import subprocess
import json
import os
import re


class InterviewAlexa(object):
    def ask_simulate(self, text, debug):
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

    def record_events(self, id, result):
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
                    raise e

            # write event_json to file with the same name as test module and function
            file = open('tmp/{}.json'.format(id), 'w+')
            with file as outfile:
                json.dump(event_json, outfile)
            file.close()

        except Exception as e:
            raise e

    def localize(self, context, lambda_path='lambda/custom/handler.py'):
        """
        Signal that local tests should be
        executed against recorded events

        Usage:
        def setUp(self):
            localize(self)
        """
        context.local = True
        context.lambda_path = lambda_path

    def record(self, context):
        """
        Signal that events should be recorded

        Usage:
        def setUp(self):
            record(self)
        """
        context.record = True

    def has_events(self, ):
        """
        Signal if events were recorded
        """
        for dirpath, dirnames, files in os.walk('tmp'):
            return files

    def parse_response(self, response):
        """
        Parse common response object
        """
        try:
            # standard response
            return response['outputSpeech']['text']
        except:
            # delegated directive response
            return response['directives'] # TODO handle this better

    def parse_ask_response(self, result):
        """
        Parse response shape from ask cli
        """
        try:
            # common response node
            response = result['skillExecutionInfo']['invocationResponse']['body']['response']
            return self.parse_response(response)
        except:
            # alexa error response
            return result['error']['message']

    def parse_local_response(self, result):
        """
        Parse response shape from `python-lambda-local`
        """
        try:
            # standard response
            return response['outputSpeech']['text']
        except:
            # delegated directive response
            return response['directives'] # TODO handle this better

    def ask_local(self, context):
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

    def say(self, text, debug=False):
        """
        Usage:

        @say("Alexa, open my skill")
        def my_test(self, result):
            self.assertEqual(result, 'My exected result')

        """
        def _outer_wrapper(wrapped_function):
            def _wrapper(*args, **kwargs):
                context = args[0]
                record = context.__dict__.get('record', None)
                local = context.__dict__.get('local', None)

                ask_says = None

                if not record and local:
                    if self.has_events():
                        ask_says = self.ask_local(context)
                        return wrapped_function(context, ask_says)
                    else:
                        raise Exception('No events were recorded. Before localizing, call the `record()` function in your test module\'s `setUp` method ')

                elif record:
                    if local:
                        raise Exception('Cannot record in localized mode. Comment out the `localize()` method in your test module\'s `setUp` method')

                    ask_json = self.ask_simulate(text, debug)
                    result = ask_json['result']
                    self.record_events(context.id(), result) # TODO make the consumer aware of localization
                    ask_says = self.parse_ask_response(result)
                    return wrapped_function(context, ask_says)

                else:
                    ask_json = self.ask_simulate(text, debug)
                    result = ask_json['result'] # REVIEW Make this available to consumer?
                    ask_says = self.parse_ask_response(result)
                    return wrapped_function(context, ask_says)

                return wrapped_function(context, ask_says)
            return _wrapper
        return _outer_wrapper


# public methods
_ia = InterviewAlexa()

say = _ia.say
record = _ia.record
localize = _ia.localize
