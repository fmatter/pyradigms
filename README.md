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
    "SG": {"1": "kɑː",
        "2": "kɛjʃ",
        "3": "kɛjtː"},
    "PL": {"1": "kœː",
        "2":"kœːtː",
        "3":"kœː"}
    }
}
```
With `print_paradigms(bernese_verbs)`, the following `.csv` file is produced:

| to go | 1  | 2  | 3  
| ----- | ----- | ----
| SG | kɑː | kɛjʃ | kɛjtː
| PL | kœː | kœːtː | kœː

to say | 1 | 2 | 3
| ----- | ----- | ------
SG | kɑː | kɛjʃ | kɛjtː
PL | kœː | kœːtː | kœː

### create_hash
The `create_hash` method takes an argument