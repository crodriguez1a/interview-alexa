Interview Alexa
===============

A Python Testing Framework for Alexa using ASK CLI

Typical usage:

```python
import unittest
from interview_alexa import say


class TestingAllTheThings(unittest.TestCase):

    @say('open my skill')
    def test_launch_intent(self, result):
        self.assertEqual(result, 'My expected result')

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
from interview_alexa import say


class TestingAllTheThings(unittest.TestCase):

    @say('open my skill')
    def test_launch_intent(self, result):
        self.assertEqual(result, "My expected result")

if __name__ == '__main__':
    unittest.main()
```

**Options:**

- **`debug=True`**

```python
@say('open my skill', debug=True)
def test_launch_intent(self, result):
    self.assertEqual(result, "My expected result")
    
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

```python
@say('open my skill')
def test_aa__begin_dialog(self, result):
    self.assertEqual(result, "My expected result")

@say('do something with my skill')
def test_ab__continue_dialog(self, result):
    self.assertEqual(result, "My expected result")
```

If the expected result is a delegated dialog, your response may not include any output speech. In that case, you may want to ``pass``:

```python
@say('do something with my skill')
def test_ac__delegated_dialog(self, result):
    pass
```

**Local Testing**

This package takes advantage of a another great package called ``python-lambda-local`` to run tests locally.

In order to do so, we use ``ask-cli`` to record your request events, and ``python-lambda-local`` to test against recorded events.

First, make sure to import the record and localize functions. Then run record in your tests module's ``setUp`` method:

```python
import unittest
from interview_alexa import say, record, localize


class TestingAllTheThings(unittest.TestCase):

    def setUp(self):
        record(self)

    @say('open my skill')
    def test_aa__launch_intent(self, result):
        self.assertEqual(result, 'My expected result')

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

```python
import unittest
from interview_alexa import say, record, localize


class TestingAllTheThings(unittest.TestCase):

def setUp(self):
    # record(self)
    localize(self)

...
```
