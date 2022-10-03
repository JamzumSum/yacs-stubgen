from pathlib import Path
from typing import Union

import yaml
from yacs.config import CfgNode


def _to_py_obj(cfg: CfgNode, cls_name: str):
    classes = {}
    d = {}
    for k, v in cfg.items():
        if isinstance(v, CfgNode):
            _clsname = str.capitalize(k)
            clss, _ = _to_py_obj(v, _clsname)
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
    """Generate a stub file (*.pyi) for the given config object.

    :param cfg: the `CfgNode` object to generate stub.
    :param path: the stub file output path or the cfg module file path. The suffix will be override.
    :param cls_name: Generated name of the root config class. You can assign an alias of `CfgNode` to this param.
    :param var_name: name of the `cfg` object. You should passin this param correctly.
    """
    assert cls_name != var_name, "class name should not be the same with var name"
    d, _ = _to_py_obj(cfg, cls_name)
    d[var_name] = cls_name
    path = Path(path)
    with open(path.with_suffix(".pyi"), "w") as f:
        # f.write("from typing import *\n")
        f.write("from yacs.config import CfgNode as CN\n\n")
        yaml.safe_dump(d, f, sort_keys=False)
