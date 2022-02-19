```python
from pyradigms import Pyradigm
from IPython.display import display, Markdown, Latex
pyd = Pyradigm.from_csv("../examples/latin_noun_entries_short.csv")
```

    <class 'pandas.core.frame.DataFrame'>


# What's in a paradigm?

## What's in the cells of a paradigm?
Typically, a linguistic paradigm has **forms** in its cells that are somehow related to one another.
For instance, this is a paradigm containing differently inflected forms of the Latin noun _aestus_ '':


```python
res = pyd.as_markdown(y="Case", x=["Number"], x_sort=["SG", "PL"], y_sort = ["NOM", "GEN", "ACC", "DAT", "ABL", "VOC"], filters={"Noun": "aestus"})
```

    [37mDEBUG  [0m Composing a new paradigm from entries:
         Noun     Form Case Number
    0  aestus   ajstus  NOM     SG
    1  aestus  ajstuːs  GEN     SG
    2  aestus  ajstuiː  DAT     SG
    3  aestus   ajstum  ACC     SG
    4  aestus   ajstus  VOC     SG
    (36 entries)[0m
    [37mDEBUG  [0m Filtering parameters:
    	Noun: a, e, s, t, u, s
    [0m
    [37mDEBUG  [0m New entries:
         Noun     Form Case Number
    0  aestus   ajstus  NOM     SG
    1  aestus  ajstuːs  GEN     SG
    2  aestus  ajstuiː  DAT     SG
    3  aestus   ajstum  ACC     SG
    4  aestus   ajstus  VOC     SG
    (12 entries)[0m
    [37mDEBUG  [0m New y id: [Case][0m
    [37mDEBUG  [0m New x id: [Number][0m
    [37mDEBUG  [0m Creating pivot table for [z], using [Number] for x axis and [Case] for y axis[0m



```python
display(Markdown(res))
```


| Case   | SG      | PL       |
|:-------|:--------|:---------|
| NOM    | ajstus  | ajstuːs  |
| GEN    | ajstuːs | ajstuum  |
| ACC    | ajstum  | ajstuːs  |
| DAT    | ajstuiː | ajstibus |
| ABL    | ajstuː  | ajstibus |
| VOC    | ajstus  | ajstuːs  |


The forms in these cells are connected by the fact that they belong to the same **lexeme**.
Overly structurally oriented linguists sometimes abstract away from concrete word forms, and only show the morph(eme)s that are different (or identical) between the cells:

This is intended to make visible the similarities between many different lexemes, making a more generalized statement.

## What's on the axes of a paradigm?
Typically, axes represent **inflectional categories**, such as in the Latin example above:
The x axis represents the different **inflectional values** of the category 'case', and the y axis shows the different values of the category 'number'.
However, this need not be so; a very common use of a paradigm is for **pronouns**, for example these XXX pronouns:

