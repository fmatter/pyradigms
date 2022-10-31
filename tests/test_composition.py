import logging
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pyradigms import Pyradigm


@pytest.fixture
def lverbs(data):
    return pd.read_csv(data / "entries_out.csv", keep_default_na=False, dtype=str)


@pytest.fixture
def usurpo(data):
    df = pd.read_csv(data / "usurpo.csv", keep_default_na=False, dtype=str, index_col=0)
    df.index.name = ""
    return df


def test_latin_verbs(lverbs, usurpo):
    pyd = Pyradigm(entries=lverbs)
    pyd.x = ["Person", "Number"]
    pyd.y = ["Mood", "Tense", "Voice"]
    pyd.z = ["Verb"]
    pyd.sort_orders = {
        "Number": ["SG", "PL"],
        "Mood": ["IND", "SBJV", "IMP"],
        "Tense": ["PRS", "PST", "FUT", "IMP", "PLUP"],
    }
    paradigms = pyd.compose_paradigm()
    paradigms["usurpo"].index.name = ""
    paradigms["usurpo"].columns.name = None
    assert_frame_equal(paradigms["usurpo"], usurpo)


df = pd.DataFrame(
    [
        ["aestus", "ajstus", "NOM", "SG"],
        ["aestus", "ajstuːs", "GEN", "SG"],
        ["aestus", "ajstuiː", "DAT", "SG"],
        ["aestus", "ajstum", "ACC", "SG"],
        ["aestus", "ajstus", "VOC", "SG"],
        ["aestus", "ajstuː", "ABL", "SG"],
        ["aestus", "ajstuːs", "NOM", "PL"],
        ["aestus", "ajstuum", "GEN", "PL"],
        ["aestus", "ajstibus", "DAT", "PL"],
        ["aestus", "ajstuːs", "ACC", "PL"],
        ["aestus", "ajstuːs", "VOC", "PL"],
        ["aestus", "ajstibus", "ABL", "PL"],
        ["aqua", "akwa", "NOM", "SG"],
        ["aqua", "akwaj", "GEN", "SG"],
        ["aqua", "akwaj", "DAT", "SG"],
        ["aqua", "akwam", "ACC", "SG"],
        ["aqua", "akwa", "VOC", "SG"],
        ["aqua", "akwaː", "ABL", "SG"],
        ["aqua", "akwaj", "NOM", "PL"],
        ["aqua", "akwaːrum", "GEN", "PL"],
        ["aqua", "akwiːs", "DAT", "PL"],
        ["aqua", "akwaːs", "ACC", "PL"],
        ["aqua", "akwaj", "VOC", "PL"],
        ["aqua", "akwiːs", "ABL", "PL"],
        ["uxor", "uksor", "NOM", "SG"],
        ["uxor", "uksoːris", "GEN", "SG"],
        ["uxor", "uksoːriː", "DAT", "SG"],
        ["uxor", "uksoːrem", "ACC", "SG"],
        ["uxor", "uksor", "VOC", "SG"],
        ["uxor", "uksoːre", "ABL", "SG"],
        ["uxor", "uksoːreːs", "NOM", "PL"],
        ["uxor", "uksoːrum", "GEN", "PL"],
        ["uxor", "uksoːribus", "DAT", "PL"],
        ["uxor", "uksoːreːs", "ACC", "PL"],
        ["uxor", "uksoːreːs", "VOC", "PL"],
        ["uxor", "uksoːribus", "ABL", "PL"],
    ],
    columns=["Lexeme", "Form", "Case", "Number"],
)


def test_simple():
    pyd = Pyradigm(df, x=["Case"], y=["Number"], filters={"Lexeme": ["aestus"]})
    table = pyd.compose_paradigm()
    assert table.loc["SG"]["ACC"] == "ajstum"


def test_filter():
    pyd = Pyradigm(
        df, x=["Case"], y=["Number", "Lexeme"], filters={"Lexeme": ["uxor", "aestus"]}
    )
    table = pyd.compose_paradigm()
    assert table.index[2] == "PL.uxor"


def test_multiple_values():
    pyd = Pyradigm(df, y=["Case"], x=["Number"])
    table = pyd.compose_paradigm(category_joiner=" A/A ")
    for i, row in table.iterrows():
        assert " A/A " in row["SG"]


def test_complex():
    pyd = Pyradigm(df, x=["Case", "Number"], y=["Lexeme"])
    table = pyd.compose_paradigm()
    assert set(table.columns) == set(
        [
            "VOC.SG",
            "DAT.PL",
            "NOM.PL",
            "VOC.PL",
            "ACC.SG",
            "GEN.PL",
            "GEN.SG",
            "ABL.SG",
            "NOM.SG",
            "DAT.SG",
            "ABL.PL",
            "ACC.PL",
        ]
    )
    assert table.loc["aqua"]["GEN.SG"] == "akwaj"


def test_missing_param():

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        pyd = Pyradigm(
            df, x=["Case"], y=["Birds aren't real"], filters={"Lexeme": ["aestus"]}
        )
        pyd.compose_paradigm()
    assert pytest_wrapped_e.type == SystemExit


def test_missing_print():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        pyd = Pyradigm(
            df,
            x=["Case"],
            y=["Number"],
            filters={"Lexeme": ["aestus"]},
            print_column="Value",
        )
        pyd.compose_paradigm()

    assert pytest_wrapped_e.type == SystemExit


def test_string_param():
    pyd = Pyradigm(df, x="Case", y="Number", filters={"Lexeme": ["aestus"]})
    tables = pyd.compose_paradigm()
    print(tables)
    # todo fix this


def test_csv(data, caplog):
    entries = pd.read_csv(data / "venire/entries.csv", dtype=str)
    pyd = Pyradigm.from_csv(data / "venire/entries.csv")
    assert_frame_equal(entries, pyd.entries)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with caplog.at_level(logging.DEBUG):
            pyd = Pyradigm.from_csv(data / "venire/entries.csv", data_format="nonsense")
        assert "Invalid format" in caplog.text
    assert pytest_wrapped_e.type == SystemExit


def test_text(data):
    path = data / "venire/entries.csv"
    entries = pd.read_csv(path, dtype=str, index_col=0)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert_frame_equal(entries, Pyradigm.from_text(text).entries)


def test_format(data, caplog):
    entries = pd.read_csv(data / "venire/entries.csv", dtype=str, index_col=0)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with caplog.at_level(logging.DEBUG):
            Pyradigm.from_dataframe(entries, data_format="unknown")
        assert "Invalid format" in caplog.text
    assert pytest_wrapped_e.type == SystemExit


def test_z(data, caplog, tmp_path):
    entries = pd.read_csv(data / "italian_entries.csv", dtype=str)
    venire = pd.read_csv(data / "venire/paradigm.csv", dtype=str, index_col=0)
    pyd = Pyradigm.from_dataframe(
        entries,
        x=["Person", "Number"],
        y=["Tense", "Mood"],
        z="Lexeme",
        ignore="ID",
        sort_orders={"Number": ["SG", "PL"], "Person": ["1", "2", "3"]},
    )
    pyd.compose_paradigm(output_folder=tmp_path)
    venire2 = pd.read_csv(tmp_path / "venire.csv", dtype=str, index_col=0)
    assert_frame_equal(venire, venire2)

    paras = pyd.compose_paradigm(x="Mood", y="Tense", z=["Lexeme", "Person", "Number"])
    assert list(paras["andare.1PL"].columns) == ["IND", "SBJV"]


def test_sorting(data, caplog):
    entries = pd.read_csv(data / "italian_entries.csv", dtype=str)
    pyd = Pyradigm.from_dataframe(
        entries,
        x=["Person", "Number"],
        y=["Tense", "Mood"],
        z="Lexeme",
        ignore="ID",
        sort_orders={"Number": ["SG", "PL"], "Person": ["1", "3"]},
    )

    with caplog.at_level(logging.DEBUG):
        pyd.compose_paradigm()
    assert "does not cover all values" in caplog.text


def test_csv_output(data, tmp_path):
    entries = pd.read_csv(data / "italian_entries.csv", dtype=str)
    pyd = Pyradigm.from_dataframe(
        entries, x=["Person", "Number"], y=["Tense", "Mood"], z="Lexeme", ignore="ID"
    )
    pyd.compose_paradigm(csv_output=tmp_path / "output.csv", with_multi_index=True)
    assert (tmp_path / "output.csv").is_file()


def test_output_folder(data, caplog, tmp_path):
    entries = pd.read_csv(data / "venire/entries.csv", dtype=str)
    pyd = Pyradigm.from_dataframe(
        entries, x=["Person", "Number"], y=["Tense", "Mood"], ignore="Lexeme"
    )
    pyd.compose_paradigm(output_folder=tmp_path)
    assert (tmp_path / "generated_paradigm.csv").is_file()


def test_markdown(caplog):
    pyd = Pyradigm.from_csv(
        "tests/data/italian_entries.csv",
        x=["Person", "Number"],
        y=["Tense", "Mood"],
        z=["Lexeme"],
    )
    assert (
        "| PRS.SBJV  | venga   | veniamo   | venga   | veniate  | venga   | vengano   |"
        in pyd.to_markdown(data_format="paradigm")
    )
    assert """<tr><td>PRS.IND  </td><td>vengo  </td><td>veniamo  </td><td>vieni  </td>\
<td>venite  </td><td>viene  </td><td>vengono  </td></tr>""" in pyd.to_markdown(
        data_format="paradigm", tablefmt="html"
    )

    pyd.filters = {"Lexeme": "venire"}
    assert "| venire-SG-1-IND-IMPF  | Form        | venivo    |" in pyd.to_markdown(
        data_format="long"
    )

    assert (
        "| venire-SG-1-SBJV-IMPF | venissi   | SG       |        1 | SBJV   | IMPF\
    | venire   |"
        in pyd.to_markdown(data_format="wide")
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with caplog.at_level(logging.DEBUG):
            pyd.to_markdown(data_format="nonsense")
        assert "Unknown format" in caplog.text
    assert pytest_wrapped_e.type == SystemExit
