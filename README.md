# [WIP] interview-alexa

A Pyhton testing framework for Alexa using `ask-cli`

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

From the command line:

```
cd My_Skill
python tests.py
```
