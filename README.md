# pyradigms

Creates paradigms from a table of entries with parameters.

## Usage

### print_paradigms
The `print_paradigms` method takes an argument `tables`, which is a three-dimensional hash, and prints them to the specified `.csv` output file.
It can be used to create paradigm representations of hashes.
Take the following hash as an example.
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
Thus, with the following command, the example hash above is created from the example `.csv` structure above:
```
pyradigms.create_hash(
    "bernese_verbs.csv",
    x = ["Verb"],
    y = ["Number"],
    z = ["Person"]
)
```

When multiple strings are given for one dimension, the parameters are combined in the resulting paradigm.
