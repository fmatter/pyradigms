# pyradigms

Creates paradigms from a table of entries with parameters.

## Usage

```
from pyradigms import Pyradigms
pd = Pyradigms("output.csv")
pd.create_hash("input.csv")
pd.print_paradigms()
```

### print_paradigms
The `print_paradigms` method takes an argument `tables`, which is a three-dimensional dictionary, and prints them to the specified `.csv` output file.
It can be used to create paradigm representations of dictionaryes.
Take the following dictionary as an example.
It has three dimensions, the first being the meaning of the verb, the second being number, and the third being person.

```
bernese_verbs = {"to go": {
    "SG": {"1": "kɑː",
        "2": "kɛjʃ",
        "3": "kɛjtː"},
    "PL": {"1": "kœː",
        "2":"kœːtː",
        "3":"kœː"}
}, "to say": {
    "SG": {"1": "sækə",
        "2": "sɛjʃ",
        "3": "sɛjtː"},
    "PL": {"1": "sækə",
        "2":"sækətː",
        "3":"sækə"}
    }
}
```
With `print_paradigms(bernese_verbs)`, a `.csv` file with the following content is produced:

| to go | 1  | 2  | 3  
| ----- | ----- | ----  | ----
| SG | kɑː | kɛjʃ | kɛjtː
| PL | kœː | kœːtː | kœː

| to say | 1 | 2 | 3
| ----- | ----- | ------ | ------
| SG | sækə | sɛjʃ | sɛjtː
| PL | sækə | sækətː | sækə

### create_hash
The `create_hash` method reads entries from a `.csv` file and produces a dictionary like the one above.
The `.csv` file should have the following format, again illustrated with the Bernese German forms:

| Verb | Number | Person | Form
| ----- | -----| ----- | -----
| to go | SG | 1 | kɑː
| to go | SG | 2 | kɛjʃ
| to go | SG | 3 | kɛjtː
| to go | PL | 1 | kœː
| to go | PL | 2 | kœːtː
| to go | PL | 3 | kœː
| to say | SG | 1 | sækə
| to say | SG | 2 | sɛjʃ
| to say | SG | 3 | sɛjtː
| to say | PL | 1 | sækə
| to say | PL | 2 | sækətː
| to say | PL | 3 | sækə

In order to specify what parameter should be projected onto which dimension, the arguments `x`, `y`, and `z` must be passed.
They each take a list of strings, the strings being parameters present in the `.csv` file.
`z` represents the multiple paradigm tables listed vertically.
`y` represents the rows of a single paradigm table.
`x` represents the columns of a single paradigm table.
The `Form` values are what is actually printed in the cells.
Thus, with the following command, the example dictionary above is created from the example `.csv` structure above:
```
pd.create_hash(
    "bernese_verbs.csv",
    x = ["Verb"],
    y = ["Number"],
    z = ["Person"]
)
```

The resulting dictionary can then be rendered to a paradigm with `pyradigms.print_paradigms()` (it is stored in the `Pyradigms` instance).

When multiple strings are given for one dimension, the parameters are combined in the resulting paradigm.
This is useful when there are more than three parameters one wants to represent.
For example, the file `examples/latin_verbs.csv` has the columns `Form	Person	Number	Tense	Verb	Mood`.
It would make sense to combine person and number, as well as tense and mood.
A separate paradigm should be produced for each verb.
This is achieved with the following command:


```
pd.create_hash(
    "examples/latin_verbs.csv",
    x = ["Person", "Number"],
    y = ["Tense", "Mood"],
    z = ["Verb"]
)
pd.print_paradigms()
```

This results in the following paradigm list:

| portaːre | 1SG | 2SG | 3SG | 1PL | 2PL | 3PL
| --- | --- | --- | --- | --- | --- | ---
| PRS:IND | portoː | portaːs | portat | portaːmus | portaːtis | portant
| PST.IPFV:IND | portaːbam | portaːbaːs | portaːbat | portaːbaːmus | portaːbaːtis | portaːbant
| FUT:IND | portaːboː | portaːbis | portaːbit | portaːbimus | portaːbitis | portaːbunt
| PRS:SUBJ | portem | porteːs | portet | porteːmus | porteːtis | portent
| PST.IPFV:SUBJ | portaːrem | portaːreːs | portaːret | portaːreːmus | portaːreːtis | portaːrent

| terːeːre | 1SG | 2SG | 3SG | 1PL | 2PL | 3PL
| --- | --- | --- | --- | --- | --- | ---
| PRS:IND | terːeoː | terːeːs | terːet | terːeːmus | terːeːtis | terːent
| PST.IPFV:IND | terːeːbam | terːeːbaːs | terːeːbat | terːeːbaːmus | terːeːbaːtis | terːeːbant
| FUT:IND | terːeːboː | terːeːbis | terːeːbit | terːeːbimus | terːeːbitis | terːeːbunt
| PRS:SUBJ | terːream | terːeaːs | terːeat | terːeaːmus | terːeaːtis | terːeant
| PST.IPFV:SUBJ | terːeːrem | terːeːres | terːeret | terːeːreːmus | terːeːreːtis | terːeːrent

| petere | 1SG | 2SG | 3SG | 1PL | 2PL | 3PL
| --- | --- | --- | --- | --- | --- | ---
| PRS:IND | petoː | petis | petit | petimus | petitis | petunt
| PST.IPFV:IND | peteːbam | peteːbas | peteːbat | peteːbaːmus | peteːbaːtis | peteːbant
| FUT:IND | petam | peteːs | petet | peteːmus | peteːtis | petent
| PRS:SUBJ | petam | petaːs | petat | petaːmus | petaːtis | petant
| PST.IPFV:SUBJ | peteːbar | peteːbaːris; peteːbaːre | peteːbaːtur | peteːbaːmus | peteːbaːminiː | peteːbaːtur

It is also possible to specify a value for a given parameter, using the `filtered_parameters` argument, which takes a dictionary.
Only forms with that value will then be represented in the resulting paradigm(s).
For example, to only print indicative forms, the following command would be used:

```
pd.create_hash(
    "examples/latin_verbs.csv",
    x = ["Person", "Number"],
    y = ["Tense"],
    z = ["Verb"],
    filtered_parameters = {"Mood": "IND"}
)
pd.print_paradigms()
```