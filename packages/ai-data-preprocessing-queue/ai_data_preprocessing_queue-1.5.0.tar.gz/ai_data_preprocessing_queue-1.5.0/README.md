# ai-data-preprocessing-queue
[![Maintainability][codeclimate-image]][codeclimate-url]
[![Coverage Status][coveralls-image]][coveralls-url]
[![Known Vulnerabilities][snyk-image]][snyk-url]

## What it does
This tool is intended for preparing data for further processing.
It contains different text processing steps that can be enabled or disabled dynamically.


### Installation
pip install ai-data-preprocessing-queue

## How to use
```python
from ai_data_preprocessing_queue import Pipeline

state = {}
pre_processor_dict = {
  'to_lower' : None,
  'spellcheck' : 'test\r\ntesting'
}
pipeline = Pipeline(pre_processor_dict)
value = pipeline.consume('Input text', state)
```

`state` is optional here and can be used to cache preprocessing data between pipeline calls.

The preprocessors that the pipeline should use have to be transmitted as keys within a dictionary.
Some preprocessors also require additional data to function.
The data must be converted into string form and assigned to its preprocessor within the dictionary.

This dictionary then needs to be transmitted to the pipeline through its constructor.

Note: Pipeline has to be instantiated only once and can be reused.

## Existing preprocessors

### To Lower Case
Name: to_lower 

Required additional data: -

Converts the text to lower case characters.

### Remove Numbers
Name: remove_numbers

Required additional data: -

Removes all numbers from the text.

### Remove Punctuation
Name: remove_punctuation

Required additional data: -

Removes all special characters from the text.

### Text only
Name: text_only

Required additional data: -

Removes all special characters and numbers from the text.

### Spellcheck (Levenshtein)
Name: spellcheck

Required additional data: A string containing words, separated by newline, i.e. "word1\r\nword2"

Takes a list of words representing the correct spelling. Words within the given text that are close to a word from this list will be replaced with the listed word.

### Regex replacement
Name: regex_replacement

Required additional data: CSV data in string form with the following line format: &lt;pattern&gt;,&lt;replacement&gt;,&lt;order&gt;
  - pattern: a regex pattern that is to be found within the text
  - replacement: the word/text by which any match should be replaced
  - order: the order in which the regex entries are supposed to be applied (lowest number will be applied first!)

This preprocessor will search for occurrences of specific entities in your text and replace them by a specified pattern.

### Token Replacement
Name: token_replacement

Required additional data: CSV data in string form with the following line format: &lt;text&gt;,&lt;replacement&gt;,&lt;order&gt;
  - text: one or multiple words to search within the text
  - replacement: the word/text by which any match should be replaced
  - order: the order in which the entries are supposed to be applied (largest number will be applied first!)

With this preprocessor you can replace specific words and abbreviations within the text with specified tokens. It is also possible to replace abbreviations ending with a dot. Other special characters are not supported, though.

## How to start developing

### With VS Code

Just install VS Code with the Dev Containers extension. All required extensions and configurations are prepared automatically.

### With PyCharm

* Install the latest PyCharm version
* Install PyCharm plugin BlackConnect
* Install PyCharm plugin Mypy
* Configure the Python interpreter/venv
* pip install requirements-dev.txt
* pip install black[d]
* Ctl+Alt+S => Check Tools => BlackConnect => Trigger when saving changed files
* Ctl+Alt+S => Check Tools => BlackConnect => Trigger on code reformat
* Ctl+Alt+S => Click Tools => BlackConnect => "Load from pyproject.yaml" (ensure line length is 120)
* Ctl+Alt+S => Click Tools => BlackConnect => Configure path to the blackd.exe at the "local instance" config (e.g. C:\Python310\Scripts\blackd.exe)
* Ctl+Alt+S => Click Tools => Actions on save => Reformat code
* Restart PyCharm

## How to publish
* Update the version in setup.py and commit your change
* Create a tag with the same version number
* Let GitHub do the rest

[codeclimate-image]:https://api.codeclimate.com/v1/badges/bcde3599d064f687803f/maintainability
[codeclimate-url]:https://codeclimate.com/github/SamhammerAG/ai-data-preprocessing-queue/maintainability
[coveralls-image]:https://coveralls.io/repos/github/SamhammerAG/ai-data-preprocessing-queue/badge.svg?branch=master
[coveralls-url]:https://coveralls.io/github/SamhammerAG/ai-data-preprocessing-queue?branch=master
[snyk-image]:https://snyk.io/test/github/SamhammerAG/ai-data-preprocessing-queue/badge.svg
[snyk-url]:https://snyk.io/test/github/SamhammerAG/ai-data-preprocessing-queue