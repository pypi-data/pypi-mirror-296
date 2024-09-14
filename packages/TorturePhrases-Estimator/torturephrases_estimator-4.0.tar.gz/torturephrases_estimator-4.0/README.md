# TorturePhrases_Estimator

TorturePhrases_Estimator is a Python package that identifies tortured phrases in text using a pre-defined list of awkward or over-complicated phrases.

## Installation

You can install the package using pip:

```bash
pip install TorturePhrases_Estimator
```

## Usage

```python
from TorturePhrases_Estimator import identify_tortured_phrases

text = "Subjects were dichotomized into experimental contingents, with one contingent being administered the active pharmaceutical ingredient and the other contingent receiving a pharmacologically inert substance."
tortured_phrases = identify_tortured_phrases(text)

print(tortured_phrases)
```
