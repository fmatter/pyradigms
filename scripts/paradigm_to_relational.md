---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.7
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Getting traditional linguistic paradigms database-ready
This is a brief illustration of how `pyradigms` can be used to convert a traditional linguistic paradigm into something more usable for computational approaches. This workflow may be handy when handling existing data in paradigmatic format, and/or to make entering data easier.

```python
from pyradigms import Pyradigm
import pandas as pd
from IPython.display import display, Markdown
```

Here's an icelandic paradigm in traditional format:

```python
paradigm = pd.read_csv("../examples/icelandic_pronoun_paradigm.csv", keep_default_na=False, index_col=0)
display(Markdown(paradigm.to_markdown()))
```

We can give this to `pyradigms`, letting it know what parameters are reflected on what axis:

```python
pyd = Pyradigm.from_dataframe(paradigm, format="paradigm", x=["Person", "Gender"], y=["Case", "Number"], log_level="WARNING")
```

It tries to decompose the paradigm, and stores it in wide format (which is also the default input):

```python
display(Markdown(pyd.to_markdown(format="wide")))
```

And from there, getting a long format is a trivial last step:

```python
display(Markdown(pyd.to_markdown(format="long")))
```

This could now be loaded into a database for further processing.
Note that what is labeled `Form` throughout could contain an `ID` of a form instead.
