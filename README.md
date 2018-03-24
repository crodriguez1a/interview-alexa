# [WIP] interview-alexa

A Python testing framework for Alexa using `ask-cli`

TODO [Pipify](http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html)

**Prerequisites**

- You'll need [ask-cli](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html)

- Install and initialize ask-cli:

	```
	npm install -g ask-cli
	ask init
	```


- Follow the **ask-cli** [prompts](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html)

- Export environment variables:

	```
	export SKILL_ID=amzn1.ask.skill.12345
	export ASK_DEFAULT_DEVICE_LOCALE=en-US
	```

- Clone your existing Skill:

	```
	ask clone echo SKILL_ID
	```


# Usage

Inside the directory of your cloned skill, create a file called `tests.py`

```
project
│
└───My_Cloned_Skill
	│
	└───tests.py
```

**Writing Tests:**

```
import unittest
from interview-alexa import test_utterance


class TestingAllTheThings(unittest.TestCase):

    @test_utterance('open my skill')
    def test_launch_intent(self, result):
        self.assertEqual(result, "My expected result")


if __name__ == '__main__':
    unittest.main()
```

**Options:**

- **`debug=True`**

```
  	@test_utterance('open my skill', debug=True)
    def test_launch_intent(self, result):
        self.assertEqual(result, "My expected result")
        # => verbose output

```


**Simple Testing**:

```
cd My_Skill
python tests.py
```
A passing test would output something like:

```
✓ Simulation created for simulation id: 1234-5679-910112-abc-123
◠ Waiting for simulation response.
----------------------------------------------------------------------
Ran 1 test in 5.848s

OK
```

**Dialog Testings**

Since the Python test runner executes tests alphabetical by test name, you'll want to ensure that any utterances in a dialog having an alphabetical naming convention.

```
@test_utterance('open my skill', debug=True)
def test_a_begin_dialog(self, result):
		self.assertEqual(result, "My expected result")
		# => verbose output
```

```
@test_utterance('do something with my skill', debug=True)
def test_aa_continue_dialog(self, result):
		self.assertEqual(result, "My expected result")
		# => verbose output
```
