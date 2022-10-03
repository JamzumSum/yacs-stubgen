# yacs-stubgen

Add typing support for your yacs config by generating stub file.

## Install

<details>

```sh
pip install yacs-stubgen
```

or install from this repo:

```sh
pip install git+github.com/JamzumSum/yacs-stubgen.git
```

</details>

## Usage

Add typing support for your yacs config by appending two lines:

```py
_C.MODEL.DEVICE = 'cuda'
...
# your config items above

from yacs_stubgen import build_pyi
# this line can be moved to the import header
build_pyi(_C, __file__, var_name='_C')
# _C is the CfgNode object, "_C" should be its name correctly
```

**After** any run/import of this file, a stub file (*.pyi) will be generated.
Then you will get typing and auto-complete support **if your IDE supports stub files**.

## License

- MIT
