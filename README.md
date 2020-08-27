# pyradigms

Creates paradigms from a table of entries with parameters.

## Getting started
`pip install pyradigms`

## Usage
There are two separate methods; `read_file` creates a three-dimensional dictionary from a `.csv` file with a list of forms with parameters, `print_paradigms` creates human-readable paradigms, also in `.csv` format, from such a dictionary.
You can either first read a file and then print the desired paradigm, or you can print a paradigm directly from a three-dimensional hash.

### `read_file`

In order to specify what parameter should be projected onto which dimension, the arguments `x`, `y`, and `z` must be passed.
They each take a list of strings, the strings being column names present in the `.csv` file.
`z` represents the multiple paradigm tables listed vertically or in multiple files in the output.
`y` represents the rows of a single paradigm table.
`x` represents the columns of a single paradigm table.
These dimensions must all be lists of strings, if a list contains multiple strings, those parameters will be combined in the resulting paradigm.
Printed in the cells of the paradigm are the values in the column `Form`; if your `.csv` file uses a different label, specify it with `read_file(target_string=<label>)`

Schematic usage:

```
import pyradigms
pd = pyradigms.Pyradigms()
pd.read_file(
    "input.csv",
    x = ["X1", "X2"],
    y = ["Y"],
    z = ["Z"],
)
pd.print_paradigms()
```

Here is an illustration from the included examples:
The file `examples/latin_verbs.csv` has the columns `Form	Person	Number	Tense	Verb	Mood`:

Form | Person | Number | Tense | Verb | Mood
-- | -- | -- | -- | -- | --
portoː | 1 | SG | PRS | portaːre | IND
portaːs | 2 | SG | PRS | portaːre | IND
portat | 3 | SG | PRS | portaːre | IND
portaːmus | 1 | PL | PRS | portaːre | IND
portaːtis | 2 | PL | PRS | portaːre | IND
portant | 3 | PL | PRS | portaːre | IND
terːeoː | 1 | SG | PRS | terːeːre | IND
… | … | … | … | … | …

One could for example want to combine person and number, as well as tense and mood.
A separate paradigm should be produced for each verb.
This is achieved as follows:

```
import pyradigms
pd = pyradigms.Pyradigms()
pd.read_file(
    "latin_verbs.csv",
    x = ["Person", "Number"],
    y = ["Tense", "Mood"],
    z = ["Verb"],
)
pd.print_paradigms(name="latin_verb_paradigms")
```

This results in the following paradigm list (in "latin_verb_paradigms.csv"):

|    portaːre   |    1SG    |    2SG     |    3SG    |     1PL      |     2PL      |    3PL     |
|---------------|-----------|------------|-----------|--------------|--------------|------------|
|    PRS:IND    |   portoː  |  portaːs   |   portat  |  portaːmus   |  portaːtis   |  portant   |
|  PST.IPFV:IND | portaːbam | portaːbaːs | portaːbat | portaːbaːmus | portaːbaːtis | portaːbant |
|    FUT:IND    | portaːboː | portaːbis  | portaːbit | portaːbimus  | portaːbitis  | portaːbunt |
|    PRS:SUBJ   |   portem  |  porteːs   |   portet  |  porteːmus   |  porteːtis   |  portent   |
| PST.IPFV:SUBJ | portaːrem | portaːreːs | portaːret | portaːreːmus | portaːreːtis | portaːrent |

|    terːeːre   |    1SG    |    2SG     |    3SG    |     1PL      |     2PL      |    3PL     |
|---------------|-----------|------------|-----------|--------------|--------------|------------|
|    PRS:IND    |  terːeoː  |  terːeːs   |   terːet  |  terːeːmus   |  terːeːtis   |  terːent   |
|  PST.IPFV:IND | terːeːbam | terːeːbaːs | terːeːbat | terːeːbaːmus | terːeːbaːtis | terːeːbant |
|    FUT:IND    | terːeːboː | terːeːbis  | terːeːbit | terːeːbimus  | terːeːbitis  | terːeːbunt |
|    PRS:SUBJ   |  terːream |  terːeaːs  |  terːeat  |  terːeaːmus  |  terːeaːtis  |  terːeant  |
| PST.IPFV:SUBJ | terːeːrem | terːeːres  |  terːeret | terːeːreːmus | terːeːreːtis | terːeːrent |

|     petere    |   1SG    |           2SG           |     3SG     |     1PL     |      2PL      |     3PL     |
|---------------|----------|-------------------------|-------------|-------------|---------------|-------------|
|    PRS:IND    |  petoː   |          petis          |    petit    |   petimus   |    petitis    |    petunt   |
|  PST.IPFV:IND | peteːbam |         peteːbas        |   peteːbat  | peteːbaːmus |  peteːbaːtis  |  peteːbant  |
|    FUT:IND    |  petam   |          peteːs         |    petet    |   peteːmus  |    peteːtis   |    petent   |
|    PRS:SUBJ   |  petam   |          petaːs         |    petat    |   petaːmus  |    petaːtis   |    petant   |
| PST.IPFV:SUBJ | peteːbar | peteːbaːris; peteːbaːre | peteːbaːtur | peteːbaːmus | peteːbaːminiː | peteːbaːtur |

You can arrange and combine the parameters as you want.
If you want to filter a certain parameter, you can add as many `filtered_parameters` as you want, and filter for a specific value.
**If a parameter appears on none of the three axes, and not in the `filtered_parameters` list, it will be ignored completely, and `pyradigms` will simply take the first form fulfilling all criteria!** (for now)

Other options of `read_file()`:
* The option `multiple_files=True` distributes the output into multiple files, which represent the `z` axis.
* The option `display=True` prints a pretty table in the command line output.
* The options `x_sort_order` and `y_sort_order` take lists which will be used to sort the output along that axis.

An example: the following code combines person and mood on the `x` axis and uses a very idiosyncratic sort order for that axis.
Number is on the `y` axis, verbs on the `z` axis; only present tense forms are taken into account.
The output is pretty printed in the terminal;  the `z` axis is distributed across three files.

```
pd.read_file(
    "latin_verbs.csv",
    x = ["Person", "Mood"],
    y = ["Number"],
    z = ["Verb"],
    filtered_parameters = {"Tense": "PRS"}
)
pd.print_paradigms(
	name="example_output",
	display=True,
	single_file=False,
	x_sort_order=["1IND", "2IND", "3IND", "3IND", "2IND", "1IND"]
)
```

| portaːre |   1SUBJ   |   2SUBJ   |   3IND  |  3SUBJ  |    2IND   |    1IND   |
|----------|-----------|-----------|---------|---------|-----------|-----------|
|    SG    |   portem  |  porteːs  |  portat |  portet |  portaːs  |   portoː  |
|    PL    | porteːmus | porteːtis | portant | portent | portaːtis | portaːmus |

| terːeːre |   1SUBJ    |   2SUBJ    |   3IND  |  3SUBJ   |    2IND   |    1IND   |
|----------|------------|------------|---------|----------|-----------|-----------|
|    SG    |  terːream  |  terːeaːs  |  terːet | terːeat  |  terːeːs  |  terːeoː  |
|    PL    | terːeaːmus | terːeaːtis | terːent | terːeant | terːeːtis | terːeːmus |

| petere |  1SUBJ   |  2SUBJ   |  3IND  | 3SUBJ  |   2IND  |   1IND  |
|--------|----------|----------|--------|--------|---------|---------|
|   SG   |  petam   |  petaːs  | petit  | petat  |  petis  |  petoː  |
|   PL   | petaːmus | petaːtis | petunt | petant | petitis | petimus |
|--------|----------|----------|--------|--------|---------|---------|


### `print_paradigms`
If you use `pyradigms` in your own application, you might have a three-dimensional dictionary already ready for it, rather than constructing it with `pyradigms`.
In that case, you can pass the argument `tables` to `print_paradigms()`; the rest works identically.
If no `tables` argument is passed, the dictionary created by `read_file()` will be used.
Take the following dictionary of Bernese German verb forms as an example.
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

In the `.csv` file, the first layer of the three-dimensional hash is represented in the `z` dimension, i.e. paradigm tables stacked vertically, the second layer is represented in the `y` axis of the individual tables, and the third layer is represented in the `x` axis.