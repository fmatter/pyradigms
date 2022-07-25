import pytest
from pathlib import Path
from pyradigms import Pyradigm
import pandas as pd
from pandas.testing import assert_frame_equal

par_cols = ["Mood", "Tense", "Number", "Person", "Lexeme"]


def sort_entries(df):
    df = df.copy()
    df["Tense"] = pd.Categorical(df["Tense"], ["PRS", "IMPF"])
    df["Number"] = pd.Categorical(df["Number"], ["SG", "PL"])
    df.sort_values(by=par_cols, inplace=True)
    df.reset_index(inplace=True, drop=True)
    df = df[["Form"] + par_cols]
    return df


def test_roundtrip(data):

    # long to wide
    long_df = pd.read_csv(data / "venire/long.csv")
    gen_entries = Pyradigm.from_dataframe(long_df, data_format="long").entries
    entries = pd.read_csv(data / "venire/entries.csv", dtype=str)
    assert_frame_equal(sort_entries(entries), sort_entries(gen_entries))

    # wide to paradigm
    pyd = Pyradigm(entries)
    gen_paradigm = pyd.compose_paradigm(
        y=["Tense", "Mood"],
        x=["Person", "Number"],
        z="Lexeme",
        sort_orders={"Number": ["SG", "PL"], "Person": ["1", "2", "3"]},
    )

    paradigm = pd.read_csv(data / "venire/paradigm.csv", dtype=str, index_col=0)

    paradigm.index.name = None
    gen_paradigm.index.name = None
    gen_paradigm.columns.name = None
    assert_frame_equal(paradigm, gen_paradigm)

    # paradigm to long
    pyd = Pyradigm.from_csv(
        data / "venire/paradigm.csv",
        data_format="paradigm",
        x=["Person", "Number"],
        y=["Tense", "Mood"],
        z="Lexeme",
    )
    pyd.entries = sort_entries(pyd.entries)
    gen_long = pyd.to_long()

    gen_long = gen_long.sort_values(by=["ID", "Parameter", "Value"])
    long_df = long_df.sort_values(by=["ID", "Parameter", "Value"])

    gen_long.reset_index(drop=True, inplace=True)
    long_df.reset_index(drop=True, inplace=True)

    assert_frame_equal(gen_long, long_df)
