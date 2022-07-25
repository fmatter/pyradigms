from pyradigms import Pyradigm
import pandas as pd
from pandas.testing import assert_frame_equal


def test_venire(data):
    pyd = Pyradigm()
    df = pd.read_csv(data / "venire.csv", index_col=0, dtype=str)
    df = pyd.decompose_paradigm(
        df, x=["Person", "Number"], y=["Tense", "Mood"], z="Lexeme"
    )
    entries = pd.read_csv(data / "italian_entries.csv", dtype=str)
    entries.drop(columns=["ID"], inplace=True)
    entries = entries[entries["Lexeme"] == "venire"]

    df = df.reindex(sorted(df.columns), axis=1)
    entries = entries.reindex(sorted(df.columns), axis=1)

    df.sort_values(by=["Form", "Person", "Number"], inplace=True)
    entries.sort_values(by=["Form", "Person", "Number"], inplace=True)

    df = df.reset_index(drop=True)
    entries = entries.reset_index(drop=True)

    assert_frame_equal(df, entries)
