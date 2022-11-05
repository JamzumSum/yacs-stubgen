import pytest
from yacs.config import CfgNode as CN

from yacs_stubgen import _CfgTyper as Typer
from yacs_stubgen import _cls_def as cls_def


@pytest.fixture
def typer():
    return Typer("_C", "AutoConfig")


def test_var_cls_name(typer: Typer):
    assert typer.classes == dict(_C="AutoConfig")


def test_basic_type(typer: Typer):
    cfg = CN()
    cfg.FLOAT = 1.0
    cfg.INT = 1
    cfg.BOOL = False
    cfg.LIST = [1, 2]
    cfg.TUPLE = (1, 2)
    cfg.STR = "hello"
    cfg.MODEL = CN()

    d = typer.add_cfg(cfg)
    assert d[cls_def(typer.cls_name)]["FLOAT"] == "float"
    assert d[cls_def(typer.cls_name)]["INT"] == "int"
    assert d[cls_def(typer.cls_name)]["BOOL"] == "bool"
    assert d[cls_def(typer.cls_name)]["LIST"] == "T.Sequence"
    assert d[cls_def(typer.cls_name)]["TUPLE"] == "T.Sequence"
    assert d[cls_def(typer.cls_name)]["STR"] == "str"
    assert cls_def("Model") in d


def test_none_type(typer: Typer):
    """`None` default value will be typed as `Any`. See #1."""
    cfg = CN()
    cfg.NONE = None

    d = typer.add_cfg(cfg)
    assert d[cls_def(typer.cls_name)]["NONE"] == "T.Any"


def test_dup(typer: Typer):
    """Duplicated class names. See #2."""
    cfg = CN()
    cfg.P1 = CN()
    cfg.P2 = CN()
    cfg.P3 = CN()
    cfg.P1.DUP = CN()
    cfg.P2.DUP = CN()
    cfg.P3.DUP = CN()
    cfg.P1.DUP.VAR1 = 1
    cfg.P2.DUP.VAR2 = "another"
    cfg.P3.DUP.VAR1 = False

    d = typer.add_cfg(cfg)
    assert d[cls_def("P1")]["DUP"] == "Dup"
    assert d[cls_def("P2")]["DUP"] == "Dup_1"
    assert d[cls_def("P3")]["DUP"] == "Dup_2"

    assert d[cls_def("Dup")]["VAR1"] == "int"
    assert d[cls_def("Dup_1")]["VAR2"] == "str"
    assert d[cls_def("Dup_2")]["VAR1"] == "bool"
