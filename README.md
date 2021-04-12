# pyradigms

pyradigms is a python package for composing and decomposing linguistic paradigms.

## Installation
Use `pip(3) install pyradigms` or get the latest version from gitlab with `pip(3) install git+https://gitlab.com/florianmatter/pyradigms.git`.


## Using pyradigms

Basically, pyradigms is intended to convert between tables like this, where every row represents a linguistic form and every column represents a parameter:

| Verb   | Form   | Tense   | Person   | Number   | Mood   |
|:-------|:-------|:--------|:---------|:---------|:-------|
| ma     | ngamam | NFUT    | 1        | SG       | RLS    |
| ma     | nam    | NFUT    | 2        | SG       | RLS    |
| ma     | mam    | NFUT    | 3        | SG       | RLS    |
| ma     | thamam | NFUT    | 1+2      | SG       | RLS    |
| ma     | ngamam | NFUT    | 1        | PL       | RLS    |
| ma     | namam  | NFUT    | 2        | PL       | RLS    |
| ma     | pamam  | NFUT    | 3        | PL       | RLS    |
| ma     | ngama  | NFUT    | 1        | SG       | IRR    |
| ma     | thama  | NFUT    | 2        | SG       | IRR    |
| ma     | kama   | NFUT    | 3        | SG       | IRR    |
|…     | …   | …    | …        | …       | …    |

and paradigms, where columns and rows both represent parameters, with forms in the cells:

| *ma*    | PST.IRR   | PST.RLS   | NFUT.IRR   | NFUT.RLS   |
|:------|:----------|:----------|:-----------|:-----------|
| 1SG   | *ngimi*   | *me*      | *ngama*    | *ngamam*   |
| 2SG   | *ni*      | *ne*      | *thama*    | *nam*      |
| 3SG   | *mi*      | *me*      | *kama*     | *mam*      |
| 1+2SG | *thumi*   | *thume*   | *pama*     | *thamam*   |
| 1PAUC | *ngumi*   | *ngume*   | *nguyema*  |            |
| 2PAUC | *numi*    | *nume*    | *nuyema*   |            |
| 3PAUC | *pumi*    | *pume*    | *kuyema*   |            |
| 1PL   | *ngumi*   | *ngume*   | *nguyema*  | *ngamam*   |
| 2PL   | *numi*    | *nume*    | *nuyema*   | *namam*    |
| 3PL   | *pumi*    | *pume*    | *kuyema*   | *pamam*    |

The two basic functionalities are composing paradigms, which creates tables like the latter form tables like the former, and decomposing paradigms, which does the opposite.

## composing paradigms

`pyradigms` takes a list such as the one seen in the first table, which you can find under [examples/murrinhpatha_verb_entries.csv](examples/murrinhpatha_verb_entries.csv).
To create a paradigm, we need to specify at least the following values:

- `x`: A list of parameter(s) which contain the values to be used as column names.
- `y`: A list of parameter(s) which contain the values to be used as row names.
- `z`: A list of parameter(s) which contain the values to be used as table names.

`x` and `y` are the usual axes, the third dimension `z` is represented by using multiple tables.
We can also provide the following optional values:

- `filters`: a list of dicts.
The dicts contain a parameter name as key, and a list as values.
Only entries which have the specified value for the specified parameter will be used.
- `ignore`: a list of parameters which will be ignored completely.
- `x_sort`: a list of values according to which the columns will be sorted.
- `y_sort`: a list of values according to which the rows will be sorted.
- `separators`: a list of strings to be used as separators between two parameter values.
The first one will be used, but multiple can be specified for decomposing paradigms, see below. Default is `["."]`.
- `content_string`: The parameter which contain the values to be used as cell contents. Default is `"Form"`.
- `person_values`: List of strings which will be combined with other strings without using a separator.
They will also be parsed accordingly.
Default is `["1", "2", "3", "1+3", "1+2"]`.

All these values are module-wide, so we specify them before composing or decomposing paradigms.
There are three methods for constructing paradigms:

- `compose_from_csv`: takes a path to a csv file
- `compose_paradigm`: takes a pandas dataframe
- `compose_from_text`: takes a csv string

All three have the optional argument `csv_output` which can contain a path to a csv file.
If present, the output will be written to that file.

Here is how the Murrinhpatha paradigm above can be constructed:

```python
import pyradigms as pyd
pyd.x = ["Tense", "Mood"]
pyd.y = ["Person", "Number"]
pyd.z = ["Verb"]
pyd.y_sort = ["1SG", "2SG", "3SG", "1+2SG", "1PAUC", "2PAUC", "3PAUC", "1PL", "2PL", "3PL"]
paradigms = pyd.compose_from_csv("examples/murrinhpatha_verb_entries.csv")
print(paradigms["ma"])
```

This will:

1. use combinations of Tense as Mood as column names
2. use the combination of Person and Number as row names
3. create a table for each verb
4. sort the Person-Number combinations accordingly.

If `z` is not an empty list, pyradigms will return a dict which has the `z` values as keys, containing pandas dataframes, therefore `print(paradigms["ma"])`.
If `z` is an empty list, only a single dataframe will be returned.

A different example from the same data, where we filter only second person values, and then put number on the `x`, verbs on the `y`, and tense-mood on the `z` axis:

```python
pyd.x = ["Number"]
pyd.y = ["Verb"]
pyd.z = ["Tense", "Mood"]
pyd.filters = {"Person": ["2"]}
pyd.x_sort=["SG", "PAUC", "PL"]
paradigms = pyd.compose_from_csv("murrinhpatha_verb_entries.csv")
print(paradigms["NFUT.IRR"])
```

| NFUT.IRR   | SG        | PAUC     | PL       |
|:-----------|:----------|:---------|:---------|
| rdi        | *thurdi*  | *nudde*  | *nuddi*  |
| ba         | *da*      | *nuba*   | *nuba*   |
| me         | *ne*      | *nume*   | *nume*   |
| li         | *tjili*   | *nilli*  | *nilli*  |
| bi         | *di*      | *nubi*   | *nubi*   |
| ni         | *thani*   | *narne*  | *narni*  |
| e          | *tje*     | *ne*     | *ne*     |
| ngi        | *thungi*  | *nunge*  | *nungi*  |
|…|…|…|…|



## decomposing paradigms
 