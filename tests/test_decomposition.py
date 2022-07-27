import logging
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pyradigms import Pyradigm


def test_venire(data):
    pyd = Pyradigm()
    df = pd.read_csv(data / "venire/paradigm.csv", index_col=0, dtype=str)
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


def test_too_many_params(caplog, data):
    pyd = Pyradigm()
    with caplog.at_level(logging.DEBUG):
        df = pd.read_csv(data / "venire/paradigm.csv", index_col=0, dtype=str)
        df = pyd.decompose_paradigm(
            df, x=["Person", "Number", "Too much"], y=["Tense", "Mood"], z="Lexeme"
        )
    assert "than specified" in caplog.text


def test_too_few_params(caplog, data):
    pyd = Pyradigm()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with caplog.at_level(logging.DEBUG):
            df = pd.read_csv(data / "venire/paradigm.csv", index_col=0, dtype=str)
            df = pyd.decompose_paradigm(
                df, x=["Person"], y=["Tense", "Mood"], z="Lexeme"
            )
        assert "More values than specified" in caplog.text
    assert pytest_wrapped_e.type == SystemExit
