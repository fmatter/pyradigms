import pandas as pd
import re
import numpy as np

cols = [
    "Verb_Form",
    "Mood",
    "Tense",
    "Aspect",
    "Voice",
    "Person",
    "Number",
    "Case",
    "Gender",
]
col_map = {i: x for i, x in enumerate(cols)}


def get_map(row, i):
    return row["PoSTag:features"].split("+")[i]


latin = pd.read_csv("/Users/florianm/Dropbox/Stuff/LatInfLexi1.1-verbs.csv")
for i, colname in col_map.items():
    print(f"{i}: {colname}")
    latin[colname] = latin.apply(get_map, i=i, axis=1)

latin["Verb_Form"].replace(
    {
        "VERB:Fin": "FIN",
        "VERB:Inf": "INF",
        "VERB:Ger": "GER",
        "VERB:Gdv": "GDV",
        "VERB:Part": "PTCP",
        "VERB:Sup": "SUP",
    },
    inplace=True,
)
latin["Mood"].replace({"Ind": "IND", "Sub": "SBJV", "Imp": "IMP"}, inplace=True)
latin["Tense"].replace(
    {"Pres": "PRS", "Imp": "IMP", "Fut": "FUT", "Past": "PST", "Pqp": "PLUP"},
    inplace=True,
)
latin["Aspect"].replace({"Imp": "IMP", "Perf": "PFV"}, inplace=True)
latin["Aspect"].replace({"Ind": "IND", "Sub": "SBJV", "Imp": "IMP"}, inplace=True)
latin["Voice"].replace({"Act": "ACT", "Pass": "PASS"}, inplace=True)
latin["Number"].replace({"Sing": "SG", "Plur": "PL"}, inplace=True)
latin["Case"] = latin["Case"].str.upper()
latin["Gender"].replace({"Masc": "M", "Fem": "F", "Neut": "N"}, inplace=True)

latin.drop(
    axis=1,
    columns=[
        "PoSTag:features",
        "freqTFTL",
        "freqAntiquitas",
        "freqAetasPatrum",
        "freqMediumAeuum",
        "freqRecentiorLatinitas",
        "form",
    ],
    inplace=True,
)
latin.rename(mapper={"lexeme": "Verb", "form_IPA": "Form"}, axis=1, inplace=True)
latin = latin.applymap(lambda x: re.sub(r"^-$", "", x))
latin.to_csv("latin_verb_entries_long.csv", index=False)
