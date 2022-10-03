from yacs.config import CfgNode as CN

_C = CN()

_C.SYSTEM = CN()
_C.SYSTEM.DEVICE = "cpu"
_C.SYSTEM.DEVICEID = (2, 3)

_C.SOLVER = CN()
_C.SOLVER.NUM_WORKERS = 8
_C.SOLVER.BASE_LR = 1e-4
_C.SOLVER.CHANNEL_LAST = True

_C.LOGDIR = "./results"


from yacs_stubgen import build_pyi

build_pyi(_C, __file__, var_name="_C")
