import pyradigms
pd = pyradigms.Pyradigms()
pd.read_file(
    "latin_verbs.csv",
    x = ["Person", "Number"],
    y = ["Tense"],
    z = ["Verb"],
    filtered_parameters = {"Mood": "IND"}
)
pd.print_paradigms(name="example_output", display=True, single_file=False)
