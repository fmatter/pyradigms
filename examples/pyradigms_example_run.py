import pyradigms
pd = pyradigms.Pyradigms()
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
	x_sort_order=["1IND", "2IND", "3IND", "3SUBJ", "2SUBJ", "1SUBJ"]
)
