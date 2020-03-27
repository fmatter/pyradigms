import pyradigms

pd = pyradigms.Pyradigms("example_output.csv")
pd.create_hash(
    "latin_verbs.csv",
    x = ["Person", "Number"],
    y = ["Tense", "Mood"],
    z = ["Verb"]
)
pd.print_paradigms(single_file=False)
