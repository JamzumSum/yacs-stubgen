from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml
from yacs.config import CfgNode

typo_map = {
    list: "T.Sequence",
    tuple: "T.Sequence",
    type(None): "T.Any",
}


def _cls_def(name: str):
    return f"class {name}(CN)"


class _CfgTyper:
    def __init__(self, var_name: str, cls_name: str) -> None:
        self.classes: Dict[str, Any] = {var_name: cls_name}
        self.dup_fmt = "{name}_{id}"
        self.cls_name = cls_name

    def __select_name(self, name: str) -> str:
        if _cls_def(name) not in self.classes:
            return name

        idx = 1
        while True:
            name_id = self.dup_fmt.format(name=name, id=idx)
            if _cls_def(name_id) not in self.classes:
                return name_id
            idx += 1

    def add_cfg(self, cfg: CfgNode, cls_name: Optional[str] = None):
        d = {}
        for k, v in cfg.items():
            if isinstance(v, CfgNode):
                _clsname = self.__select_name(str.capitalize(k))
                self.add_cfg(v, _clsname)
                d[k] = _clsname
            else:
                d[k] = typo_map.get(type(v), type(v).__name__)

        self.classes[_cls_def(cls_name or self.cls_name)] = d
        return self.classes


class _BlackDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


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
    d = _CfgTyper(var_name=var_name, cls_name=cls_name).add_cfg(cfg, cls_name)

    with open(Path(path).with_suffix(".pyi"), "w") as f:
        f.write("import typing as T\n\n")
        f.write("from yacs.config import CfgNode as CN\n\n")
        yaml.dump(
            d,
            f,
            Dumper=_BlackDumper,
            indent=4,
            default_flow_style=False,
            canonical=False,
            sort_keys=False,
        )
