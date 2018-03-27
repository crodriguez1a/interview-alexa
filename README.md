Interview Alexa
===============

A Python Testing Framework for Alexa using ASK CLI

Typical usage:

<<<<<<< Updated upstream
```python
import unittest
from interview_alexa import test_utterance
=======
    import unittest
    from interview_alexa import say
>>>>>>> Stashed changes


class TestingAllTheThings(unittest.TestCase):

<<<<<<< Updated upstream
@test_utterance('open my skill')
def test_launch_intent(self, result):
    self.assertEqual(result, 'My expected result')
=======
        @say('open my skill')
        def test_launch_intent(self, result):
            self.assertEqual(result, 'My expected result')
>>>>>>> Stashed changes

if __name__ == '__main__':
unittest.main()
```

Prerequisites
=============

* Install ``node``
  * <https://nodejs.org/en/download/package-manager/>

* Install and initialize ``ask-cli``
	* <https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html>

    	npm install -g ask-cli
    	ask init

* Follow the ``ask-cli`` prompts

* Export environment variables:

```bash
export SKILL_ID=amzn1.ask.skill.12345
export ASK_DEFAULT_DEVICE_LOCALE=en-US
```

* Clone your existing Alexa skill:

```bash
ask clone echo SKILL_ID
```


Usage
=====

Inside the directory of your cloned skill, create a file called ``tests.py``

```bash
project
│
└───My_Cloned_Skill
	│
	└───tests.py
```

**Writing Tests:**

```python
import unittest
from interview_alexa import test_utterance

<<<<<<< Updated upstream
=======
		import unittest
		from interview_alexa import say
>>>>>>> Stashed changes

class TestingAllTheThings(unittest.TestCase):

    @test_utterance('open my skill')
    def test_launch_intent(self, result):
	self.assertEqual(result, "My expected result")

<<<<<<< Updated upstream
=======
		    @say('open my skill')
		    def test_launch_intent(self, result):
		        self.assertEqual(result, "My expected result")


		if __name__ == '__main__':
		    unittest.main()
>>>>>>> Stashed changes

if __name__ == '__main__':
    unittest.main()
```

**Options:**

- **`debug=True`**

<<<<<<< Updated upstream
```python
@test_utterance('open my skill', debug=True)
def test_launch_intent(self, result):
    self.assertEqual(result, "My expected result")
=======
		@say('open my skill', debug=True)
		def test_launch_intent(self, result):
		    self.assertEqual(result, "My expected result")

		    # => will produce a verbose output from ask-cli
>>>>>>> Stashed changes

    # => will produce a verbose output from ask-cli
```

**Simple Testing**:

```bash
cd My_Skill
python tests.py
```

--
```bash
A passing test would output something like:

✓ Simulation created for simulation id: 1234-5679-910112-abc-123
◠ Waiting for simulation response.
----------------------------------------------------------------------
Ran 1 test in 5.848s

OK
```

**Dialog Testing**

Since the Python test runner executes tests alphabetical by test name, you'll want to ensure that any tests that simulate dialog are named alphabetically.

<<<<<<< Updated upstream
```python
@test_utterance('open my skill')
def test_aa__begin_dialog(self, result):
    self.assertEqual(result, "My expected result")

@test_utterance('do something with my skill')
def test_ab__continue_dialog(self, result):
    self.assertEqual(result, "My expected result")
```
=======
		@say('open my skill')
		def test_aa__begin_dialog(self, result):
		    self.assertEqual(result, "My expected result")

		@say('do something with my skill')
		def test_ab__continue_dialog(self, result):
		    self.assertEqual(result, "My expected result")
>>>>>>> Stashed changes


If the expected result is a delegated dialog, your response may not include any output speech. In that case, you may want to ``pass``:

<<<<<<< Updated upstream
```python
@test_utterance('do something with my skill')
def test_ac__delegated_dialog(self, result):
    pass
```
=======
		@say('do something with my skill')
		def test_ac__delegated_dialog(self, result):
		    pass
>>>>>>> Stashed changes


**Local Testing**

This package takes advantage of a another great package called ``python-lambda-local`` to run tests locally.

In order to do so, we use ``ask-cli`` to record your request events, and ``python-lambda-local`` to test against recorded events.

First, make sure to import the record and localize functions. Then run record in your tests module's ``setUp`` method:

<<<<<<< Updated upstream
```python
import unittest
from interview_alexa import test_utterance, record, localize
=======
    import unittest
    from interview_alexa import say, record, localize
>>>>>>> Stashed changes


class TestingAllTheThings(unittest.TestCase):

def setUp(self):
    record(self)

<<<<<<< Updated upstream
@test_utterance('open my skill')
def test_aa__launch_intent(self, result):
    self.assertEqual(result, 'My expected result')
=======
        @say('open my skill')
        def test_aa__launch_intent(self, result):
            self.assertEqual(result, 'My expected result')
>>>>>>> Stashed changes

...
```

Once you've run your test with **record mode** on, you should see a ``tmp`` folder in your working directory with some JSON files with the same names as your tests.

```bash
project
│
└───My_Cloned_Skill
	│
	└───tests.py
	│
	└───tmp
	  │
	  └───__main__.TestingAllTheThings.test_aa.json
```

Now that you have some events recorded locally, you can run your tests in **localize mode**, and run your tests again with ``python tests.py`` as you normally would.

<<<<<<< Updated upstream
```python
import unittest
from interview_alexa import test_utterance, record, localize
=======

    import unittest
    from interview_alexa import say, record, localize
>>>>>>> Stashed changes


class TestingAllTheThings(unittest.TestCase):

def setUp(self):
    # record(self)
    localize(self)

...
```