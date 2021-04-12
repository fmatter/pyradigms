# pyradigms

pyradigms is a python package for composing and decomposing linguistic paradigms.

##### Table of Contents  
[Installation](#installation)
[Usage](#usage)
[Composing paradigms](#composing)
[Decomposing paradigms](#decomposing)

## Installation
<a name="installation"/>
Use `pip(3) install pyradigms` or get the latest version from gitlab with `pip(3) install git+https://gitlab.com/florianmatter/pyradigms.git`.

## Usage
<a name="usage"/>

Basically, pyradigms is intended to convert between the two following formats:

| Verb   | Form   | Tense   | Person   | Number   | Mood   |
|:-------|:-------|:--------|:---------|:---------|:-------|
| ma     | ngamam | NFUT    | 1        | SG       | RLS    |
| ma     | nam    | NFUT    | 2        | SG       | RLS    |
| ma     | mam    | NFUT    | 3        | SG       | RLS    |
| ma     | thamam | NFUT    | 1+2      | SG       | RLS    |
|…     | …   | …    | …        | …       | …    |

| *ma*    | PST.IRR   | PST.RLS   | NFUT.IRR   | NFUT.RLS   |
|:------|:----------|:----------|:-----------|:-----------|
| 1SG   | *ngimi*   | *me*      | *ngama*    | *ngamam*   |
| 2SG   | *ni*      | *ne*      | *thama*    | *nam*      |
| 3SG   | *mi*      | *me*      | *kama*     | *mam*      |
| 1+2SG | *thumi*   | *thume*   | *pama*     | *thamam*   |
|…|…|…|…|…|

In linguistic morphology, a paradigm is a collection of word forms belonging to the same lexeme, here for the Murrinhpatha verb root *ma* 'say, do'.
The first table shows all word forms, with relevant grammatical categories like tense, person, etc. represented in their own column.
The second table is what is conventionally called a paradigm, which shows person-number combinations on the left, and tense-mood combinations at the top, with cells only containing the word forms.
`pyradigms` is primarily intended to create such paradigm tables from any list, allowing you to combine parameters in any way you like.

## Composing paradigms
<a name="composing"/>

To create a paradigm, we need to specify at least `x` and `y`, lists of parameter(s) which contain the values to be used as column and row names, respectively.
Optionally, a list `z` can be specified, which will be represented as several tables.
We can also provide the following optional values:

- `filters`: a list of dicts.
The dicts contain a parameter name as key, and a list as values.
Only entries which have the specified value for the specified parameter will be used.
- `ignore`: a list of parameters which will be ignored completely.
- `x_sort`: a list of values according to which columns will be sorted.
- `y_sort`: a list of values according to which rows will be sorted.
- `separators`: a list of strings to be used as separators between two parameter values.
The first one will be used, but multiple can be specified for decomposing paradigms, see below. Default value is `["."]`.
- `content_string`: The parameter which contain the values to be used as cell contents. Default value is `"Form"`.
- `person_values`: List of strings which will be combined with other strings without using a separator.
They will also be parsed accordingly.
Default value is `["1", "2", "3", "1+3", "1+2"]`.

All these values are module-wide, so we specify them before composing or decomposing paradigms.
There are three methods for constructing paradigms:

- `compose_from_csv`: takes a path to a csv file
- `compose_paradigm`: takes a pandas dataframe
- `compose_from_text`: takes a csv string

All three have the optional argument `csv_output` which can contain a path to a csv file.
If present, the output will be written to that file.

Here is an example based on the Murrinhpatha verbs seen above, which can be found under [examples/murrinhpatha_verb_entries.csv](examples/murrinhpatha_verb_entries.csv).

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

The resulting paradigm table:

| ma    | NFUT.RLS   | PST.IRR   | NFUT.IRR   | PST.RLS   |
|:------|:-----------|:----------|:-----------|:----------|
| 1SG   | *ngamam*   | *ngimi*   | *ngama*    | *me*      |
| 2SG   | *nam*      | *ni*      | *thama*    | *ne*      |
| 3SG   | *mam*      | *mi*      | *kama*     | *me*      |
| 1+2SG | *thamam*   | *thumi*   | *pama*     | *thume*   |
| 1PAUC |            | *ngumi*   | *nguyema*  | *ngume*   |
| 2PAUC |            | *numi*    | *nuyema*   | *nume*    |
| 3PAUC |            | *pumi*    | *kuyema*   | *pume*    |
| 1PL   | *ngamam*   | *ngumi*   | *nguyema*  | *ngume*   |
| 2PL   | *namam*    | *numi*    | *nuyema*   | *nume*    |
| 3PL   | *pamam*    | *pumi*    | *kuyema*   | *pume*    |

If `z` is not an empty list, pyradigms will return a dict which has the `z` values as keys, containing pandas dataframes, therefore `print(paradigms["ma"])`.
If `z` is an empty list, only a single dataframe will be returned.

A different example from the same data, where we filter only second person values, and then put person-number on the `x`, verbs on the `y`, and tense-mood on the `z` axis:

```python
pyd.x = ["Person", "Number"]
pyd.y = ["Verb"]
pyd.z = ["Tense", "Mood"]
pyd.filters = {"Person": ["2"]}
pyd.x_sort=["2SG", "2PAUC", "2PL"]
paradigms = pyd.compose_from_csv("murrinhpatha_verb_entries.csv")
print(paradigms["NFUT.IRR"])
```

| NFUT.IRR   | 2SG    | 2PAUC       | 2PL      |
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

Another example, with Latin noun forms:

```python
pyd.x = ["Case"]
pyd.y = ["Noun"]
pyd.z = ["Number"]
pyd.y_sort = ["NOM", "GEN", "DAT", "ACC","ABL","VOC"]
paradigms = pyd.compose_from_csv("examples/latin_noun_entries_short.csv")
print(paradigms["SG"])
print(paradigms["PL"])
```

| SG     | GEN        | NOM      | ACC        | ABL       | DAT        | VOC      |
|:-------|:-----------|:---------|:-----------|:----------|:-----------|:---------|
| uxor   | *uksoːris* | *uksor*  | *uksoːrem* | *uksoːre* | *uksoːriː* | *uksor*  |
| aestus | *ajstuːs*  | *ajstus* | *ajstum*   | *ajstuː*  | *ajstuiː*  | *ajstus* |
| aqua   | *akwaj*    | *akwa*   | *akwam*    | *akwaː*   | *akwaj*    | *akwa*   |

| PL     | ACC         | GEN        | ABL          | VOC         | NOM         | DAT          |
|:-------|:------------|:-----------|:-------------|:------------|:------------|:-------------|
| uxor   | *uksoːreːs* | *uksoːrum* | *uksoːribus* | *uksoːreːs* | *uksoːreːs* | *uksoːribus* |
| aestus | *ajstuːs*   | *ajstuum*  | *ajstibus*   | *ajstuːs*   | *ajstuːs*   | *ajstibus*   |
| aqua   | *akwaːs*    | *akwaːrum* | *akwiːs*     | *akwaj*     | *akwaj*     | *akwiːs*     |

Alternatively, we can generate tables for each case, and look at dative and ablative forms:

```python
pyd.x = ["Noun"]
pyd.y = ["Number"]
pyd.z = ["Case"]
pyd.y_sort=["SG", "PL"]
paradigms = pyd.compose_from_csv("examples/latin_noun_entries_short.csv")
print(paradigms["DAT"])
print(paradigms["ABL"])
```

| DAT   | aqua     | aestus     | uxor         |
|:------|:---------|:-----------|:-------------|
| SG    | *akwaj*  | *ajstuiː*  | *uksoːriː*   |
| PL    | *akwiːs* | *ajstibus* | *uksoːribus* |

| ABL   | uxor         | aestus     | aqua     |
|:------|:-------------|:-----------|:---------|
| SG    | *uksoːre*    | *ajstuː*   | *akwaː*  |
| PL    | *uksoːribus* | *ajstibus* | *akwiːs* |

Of course, you can also use pyradigms for comparative tables containing multiple languages.
For example, [examples/cariban_swadesh_entries.csv](examples/cariban_swadesh_entries.csv) contains some Swadesh entries for Cariban languages from [Matter (2021)](https://zenodo.org/record/4438189).
The following code puts cognate sets (reconstructed forms) on the y-axis, languages on the x-axis, and filters for six languages (for vertical space limitations in this readme…).

```python
pyd.x = ["Language"]
pyd.y = ["Cognateset"]
pyd.z = []
pyd.content_string = "Value"
lg_list = ["Werikyana", "Hixkaryána", "Waiwai", "Bakairi", "Arara", "Ikpeng"]
pyd.filters = {"Language": lg_list}
pyd.x_sort = lg_list
paradigms = pyd.compose_from_csv("examples/cariban_swadesh_entries.csv")
print(paradigms)
```

| Cognateset   | Werikyana   | Hixkaryána   | Waiwai   | Bakairi   | Arara   | Ikpeng   |
|:-------------|:------------|:-------------|:---------|:----------|:--------|:---------|
| *wewe        | *wewe*      | *wewe*       | *weewe*  |           |         |          |
| *punu        | *hunu*      | *hun*        | *ɸun*    | *ũrũ*     | *munu*  | *mnu*    |
| *pitupə      | *hi*        | *hut͡ʃhu*     | *ɸit͡ʃho* | *tubɨ*    | *iput*  | *pitu*   |
| *jəje        |             |              |          | *e*       | *jei*   | *jaj*    |
| *jətɨpə      | *jot͡ʃpɨ*    | *jot͡ʃhɨ*     | *jot͡ʃho* | *ibɨrɨ*   | *itpɨ*  | *itpɨn*  |

Alternatively, we can put cognate sets on the x-axis and languages on the y-axis:

```python
pyd.z = []
pyd.y = ["Language"]
pyd.x = ["Cognateset"]
pyd.filters = {}
pyd.y_sort = ['Werikyana', 'Hixkaryána', 'Waiwai', 'Arara', 'Ikpeng', 'Bakairi', 'Tiriyó', 'Akuriyó', 'Karijona', 'Wayana', 'Apalaí', "Kari'ña", "Ye'kwana", 'Kapón', 'Akawaio', 'Ingarikó', 'Patamona', 'Pemón', 'Macushi', 'Panare', 'Tamanaku', 'Yawarana', 'Mapoyo', 'Kumaná', 'Upper Xingu Carib', 'Kuikuro', 'Yukpa', 'Japreria', 'Waimiri-Atroari']
paradigms = pyd.compose_from_csv("examples/cariban_swadesh_entries.csv")
print(paradigms)
```

| Language        | *punu   | *pitupə   | *jəje   | *jətɨpə   | *wewe   |
|:----------------|:--------|:----------|:--------|:----------|:--------|
| Werikyana       | *hunu*  | *hi*      |         | *jot͡ʃpɨ*  | *wewe*  |
| Hixkaryána      | *hun*   | *hut͡ʃhu*  |         | *jot͡ʃhɨ*  | *wewe*  |
| Waiwai          | *ɸun*   | *ɸit͡ʃho*  |         | *jot͡ʃho*  | *weewe* |
| Arara           | *munu*  | *iput*    | *jei*   | *itpɨ*    |         |
| Ikpeng          | *mnu*   | *pitu*    | *jaj*   | *itpɨn*   |         |
| Bakairi         | *ũrũ*   | *tubɨ*    | *e*     | *ibɨrɨ*   |         |
| Tiriyó          | *pun*   | *pihpə*   |         | *jetɨpə*  | *wewe*  |
| Akuriyó         | *puunu* | *pihpə*   |         | *jeʔpə*   | *wewe*  |
| Karijona        | *bunu*  | *hitihə*  |         | *ijetihɨ* | *wewe*  |
| Wayana          | *punu*  | *pitpə*   |         | *jetpə*   | *wewe*  |
| Apalaí          | *pu*    | *piʔpo*   |         | *zeʔpo*   | *wewe*  |
| Kari'ña         | *pun*   | *piʔpo*   |         | *jeʔpo*   | *wewe*  |
| Ye'kwana        | *hunu*  | *hiʔhə*   | *ree*   | *jeeʔhə*  |         |
| Akawaio         | *pun*   | *piʔpə*   | *jɨi*   | *əʔpɨ*    |         |
| Ingarikó        | *pun*   | *piʔpɨ*   | *jɨi*   | *əʔpɨ*    |         |
| Pemón           | *pun*   | *piʔpə*   | *jəi*   | *jeʔpə*   |         |
| Macushi         | *pun*   | *piʔpɨ*   | *jei*   | *jeʔpɨ*   |         |
| Panare          | *-pu*   | *pihpə*   | *ije*   | *jəhpə*   |         |
| Tamanaku        | *punu*  | *pitpe*   | *jeje*  | *jetpe*   |         |
| Yawarana        | *puunu* | *pihpə*   | *jəəje* | *jəspə*   |         |
| Mapoyo          | *punu*  | *piʔpə*   | *jəhe*  | *jəʔpə*   |         |
| Kuikuro         | *huŋu*  | *hiɟo*    | *i*     | *ipɨɣɨ*   |         |
| Yukpa           | *pu*    |           |         | *jopo*    | *we*    |
| Waimiri-Atroari | *pɨnɨ*  | *biʃi*    |         | *jɨhɨ*    | *wiwe*  |

## decomposing paradigms
<a name="decomposing"/>
This was added as a secondary functionality and is somewhat experimental.
The basic idea is that it allows you to decompose a paradigm which is already in the traditional linguistic format, into a list of parametrized rows.
THis can be useful if you already have a nicely formatted paradigm somewhere, but need it in an explicit list format -- for example, to rearrange it with `compose_paradigm()`.

The file [examples/icelandic_pronoun_paradigm.csv](examples/icelandic_pronoun_paradigm.csv) contains the personal pronouns of Icelandic:
|        | 1       | 2       | 3M       | 3F       | 3N       |
|:-------|:--------|:--------|:---------|:---------|:---------|
| NOM.SG | *ég*    | *þú*    | *hann*   | *hún*    | *það*    |
| ACC.SG | *mig*   | *þig*   | *hann*   | *hana*   | *það*    |
| DAT.SG | *mér*   | *þér*   | *honum*  | *henni*  | *því*    |
| GEN.SG | *mín*   | *þín*   | *hans*   | *hennar* | *þess*   |
| NOM.PL | *við*   | *þið*   | *þeir*   | *þær*    | *þau*    |
| ACC.PL | *okkur* | *ykkur* | *þá*     | *þær*    | *þau*    |
| DAT.PL | *okkur* | *ykkur* | *þeim*   | *þeim*   | *þeim*   |
| GEN.PL | *okkar* | *ykkar* | *þeirra* | *þeirra* | *þeirra* |

`x` is a combination of person and gender, although first and second person have no gender distinction.
`y` is a combination of case and number.
If we define these parameters accordingly, we get the following:

```python
pyd.x = ["Person", "Gender"]
pyd.y = ["Case", "Number"]
pyd.z = []
entries = pyd.decompose_from_csv("examples/icelandic_pronoun_paradigm.csv")
print(entries)
```

|   Person | Gender   | Case   | Number   | Value   |
|---------:|:---------|:-------|:---------|:--------|
|        1 |          | NOM    | SG       | ég      |
|        1 |          | ACC    | SG       | mig     |
|        1 |          | DAT    | SG       | mér     |
|        1 |          | GEN    | SG       | mín     |
|        1 |          | NOM    | PL       | við     |
|        1 |          | ACC    | PL       | okkur   |
|        1 |          | DAT    | PL       | okkur   |
|        1 |          | GEN    | PL       | okkar   |
|        2 |          | NOM    | SG       | þú      |
|        2 |          | ACC    | SG       | þig     |
|        2 |          | DAT    | SG       | þér     |
|        2 |          | GEN    | SG       | þín     |
|        2 |          | NOM    | PL       | þið     |
|        2 |          | ACC    | PL       | ykkur   |
|        2 |          | DAT    | PL       | ykkur   |
|        2 |          | GEN    | PL       | ykkar   |
|        3 | M        | NOM    | SG       | hann    |
|        3 | M        | ACC    | SG       | hann    |
|        3 | M        | DAT    | SG       | honum   |
|        3 | M        | GEN    | SG       | hans    |
|        3 | M        | NOM    | PL       | þeir    |
|        3 | M        | ACC    | PL       | þá      |
|        3 | M        | DAT    | PL       | þeim    |
|        3 | M        | GEN    | PL       | þeirra  |
|        3 | F        | NOM    | SG       | hún     |
|        3 | F        | ACC    | SG       | hana    |
|        3 | F        | DAT    | SG       | henni   |
|        3 | F        | GEN    | SG       | hennar  |
|        3 | F        | NOM    | PL       | þær     |
|        3 | F        | ACC    | PL       | þær     |
|        3 | F        | DAT    | PL       | þeim    |
|        3 | F        | GEN    | PL       | þeirra  |
|        3 | N        | NOM    | SG       | það     |
|        3 | N        | ACC    | SG       | það     |
|        3 | N        | DAT    | SG       | því     |
|        3 | N        | GEN    | SG       | þess    |
|        3 | N        | NOM    | PL       | þau     |
|        3 | N        | ACC    | PL       | þau     |
|        3 | N        | DAT    | PL       | þeim    |
|        3 | N        | GEN    | PL       | þeirra  |