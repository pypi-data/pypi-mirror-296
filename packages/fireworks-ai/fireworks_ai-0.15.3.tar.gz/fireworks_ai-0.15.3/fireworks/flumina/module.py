import torch
import enum
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Dict, Optional
from safetensors.torch import save_model
import tempfile


class FluminaModule(torch.nn.Module):
    pass


def path(path: str):
    def wrapper(fn):
        fn._flumina_path = path
        return fn

    return wrapper


@dataclass
class _ExportedModule:
    serialized_weights: bytes
    path_to_method_name: Dict[str, str]


class _ExecMode(enum.Enum):
    NONE = 0
    EXPORT = 1
    SERVE = 2


_exec_mode = _ExecMode.NONE
_exported_module: Optional[_ExportedModule] = None


def _get_exported_module():
    global _exported_module
    em = _exported_module
    _exported_module = None
    return em


@contextmanager
def _with_exec_mode(mode):
    global _exec_mode
    old_mode = _exec_mode
    _exec_mode = mode
    try:
        yield
    finally:
        _exec_mode = old_mode


_initialized_module: Optional[FluminaModule] = None


def _get_initialized_module():
    global _initialized_module
    mod = _initialized_module
    _initialized_module = None
    return mod


def main(m: FluminaModule):
    if _exec_mode == _ExecMode.NONE:
        pass
    elif _exec_mode == _ExecMode.EXPORT:
        assert isinstance(
            m, FluminaModule
        ), "Argument to flumina.main() must be an instance of FluminaModule"
        path_to_method_name: Dict[str, str] = {}
        for k in dir(m):
            v = getattr(m, k)
            if hasattr(v, "_flumina_path"):
                path_to_method_name[v._flumina_path] = k

        with tempfile.NamedTemporaryFile() as ntf:
            save_model(m, ntf.name)
            with open(ntf.name, "rb") as f:
                serialized_weights = f.read()

        global _exported_module
        _exported_module = _ExportedModule(
            serialized_weights=serialized_weights,
            path_to_method_name=path_to_method_name,
        )
    elif _exec_mode == _ExecMode.SERVE:
        global _initialized_module
        _initialized_module = m
    else:
        raise NotImplementedError("Unsupported ExecMode", _exec_mode)
