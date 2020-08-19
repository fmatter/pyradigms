import pyradigms

pd = pyradigms.Pyradigms("example_output.csv")
pd.create_hash(
    "latin_verbs.csv",
    x = ["Number","Person"],
    y = ["Tense"],
    z = [],
    filtered_parameters = {"Verb": "portaːre", "Mood": "IND"}
)
pd.print_paradigms(single_file=True)
