from pathlib import Path
from typing import Union

import yaml
from yacs.config import CfgNode


def to_py_obj(cfg: CfgNode, cls_name: str):
    classes = {}
    d = {}
    for k, v in cfg.items():
        if isinstance(v, CfgNode):
            _clsname = str.capitalize(k)
            clss, _ = to_py_obj(v, _clsname)
            classes.update(clss)
            d[k] = _clsname
        else:
            assert str.isidentifier(type(v).__name__)
            d[k] = type(v).__name__
    classes[f"class {cls_name}(CN)"] = d
    return classes, d


def build_pyi(
    cfg: CfgNode, path: Union[Path, str], cls_name="AutoConfig", var_name="cfg"
):
    d, _ = to_py_obj(cfg, cls_name)
    d[var_name] = cls_name
    path = Path(path)
    with open(path.with_suffix(".pyi"), "w") as f:
        # f.write("from typing import *\n")
        f.write("from yacs.config import CfgNode as CN\n\n")
        yaml.safe_dump(d, f, sort_keys=False)
