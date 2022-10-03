import argparse
import importlib
import logging
import sys
from pathlib import Path
from typing import Iterable

from yacs.config import CfgNode

from yacs_stubgen import build_pyi

logging.basicConfig(level="INFO", format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def inspect_module(mod_path: Path, ROOT: Path):
    assert mod_path.exists()
    rel_path = mod_path.relative_to(ROOT)
    if rel_path.stem == "__init__":
        rel_path = rel_path.parent
    package = rel_path.with_suffix("").as_posix().replace("/", ".").replace("-", "_")

    try:
        mod = importlib.import_module(package)
    except ImportError as e:
        log.error(e)
        return False

    clsname = varname = ""
    cfg = None
    for k, v in mod.__dict__.items():
        if isinstance(v, CfgNode):
            cfg = v
            varname = k
        elif isinstance(v, type):
            if k != "CN" and issubclass(v, CfgNode):
                clsname = k
        if clsname and varname:
            break

    if cfg and varname:
        if clsname:
            build_pyi(cfg, mod_path, cls_name=clsname, var_name=varname)
        else:
            build_pyi(cfg, mod_path, var_name=varname)
            log.warning(
                "You haven't set an alias for CfgNode, the config class cannot be imported."
            )
        return True
    return False


def ibuild_pyi(pathes: Iterable[Path], ROOT: Path):
    sys.path.insert(0, str(ROOT.absolute()))

    try:
        for py in pathes:
            if any(i.startswith(".") for i in py.parts):
                continue
            if inspect_module(py, ROOT):
                pyi = py.with_suffix(".pyi")
                assert pyi.exists()
                log.info(f"Generated {pyi.as_posix()}")
    finally:
        sys.path.pop(0)


def rbuild_pyi(dir: Path):
    return ibuild_pyi(dir.rglob("*.py"), dir)


def main():
    psr = argparse.ArgumentParser()
    psr.add_argument("dir", nargs="?", default=".", type=Path)
    args = psr.parse_args()

    ROOT: Path = args.dir
    if ROOT.is_dir():
        rbuild_pyi(ROOT)
    elif ROOT.is_file():
        ibuild_pyi((ROOT,), ROOT.parent)


if __name__ == "__main__":
    main()
