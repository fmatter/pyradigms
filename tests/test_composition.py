import pytest
from pathlib import Path
from pyradigms import Pyradigm
import pandas as pd
from pandas.testing import assert_frame_equal

@pytest.fixture
def data():
    return Path(__file__).parent / "data"

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
    pyd.z=["Verb"]
    pyd.x_sort=["1SG", "2SG", "3SG", "1PL", "2PL", "3PL"]
    pyd.y_sort=[
"IND.PRS.ACT",  
"IND.PRS.PASS", 
"IND.PST.ACT",   
"IND.FUT.ACT",  
"IND.FUT.PASS", 
"IND.IMP.ACT",
"IND.IMP.PASS", 
"IND.PLUP.ACT", 
"SBJV.PRS.ACT", 
"SBJV.PRS.PASS", 
"SBJV.PST.ACT", 
"SBJV.PLUP.ACT", 
"SBJV.IMP.ACT", 
"SBJV.IMP.PASS", 
"IMP.PRS.ACT",  
"IMP.PRS.PASS", 
"IMP.FUT.ACT",  
"IMP.FUT.PASS", 
]
    paradigms = pyd.compose_paradigm()
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

def test_multiple_values():
    pyd = Pyradigm(df, y=["Case"], x=["Number"])
    table = pyd.compose_paradigm(joiner=" A/A ")
    for i, row in table.iterrows():
        assert " A/A " in row["SG"]

def test_complex():
    pyd = Pyradigm(df, x=["Case", "Number"], y=["Lexeme"])
    table = pyd.compose_paradigm()
    assert set(table.columns) == set(['VOC.SG', 'DAT.PL', 'NOM.PL', 'VOC.PL', 'ACC.SG', 'GEN.PL', 'GEN.SG',
       'ABL.SG', 'NOM.SG', 'DAT.SG', 'ABL.PL', 'ACC.PL'])
    assert table.loc["aqua"]["GEN.SG"] == "akwaj"

def test_missing_param():
    pyd = Pyradigm(df, x=["Case"], y=["Birds aren't real"], filters={"Lexeme": ["aestus"]})
    assert pyd.compose_paradigm() == None

def test_missing_form():
    pyd = Pyradigm(df, x=["Case"], y=["Number"], filters={"Lexeme": ["aestus"]}, content_string="Value")
    assert pyd.compose_paradigm() == None

def test_string_param():
    pyd = Pyradigm(df, x="Case", y="Number", filters={"Lexeme": ["aestus"]})
    tables = pyd.compose_paradigm()
    print(tables)
test_string_param()