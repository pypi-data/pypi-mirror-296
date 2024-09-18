from .module import (
    _with_exec_mode,
    _ExecMode,
    _get_exported_module,
    _get_initialized_module,
)

import builtins
from functools import partial

import torch
import os
import sys


ALLOWED_EXTERNAL_DEPS = set(sys.builtin_module_names).union(
    {
        "accelerate",
        "contextlib",
        "fireworks",
        "flux",
        "transformers",
        "diffusers",
        "torch",
        "torchaudio",
        "torchvision",
        "PIL",
        "pydantic",
        "io",
        "fastapi",
        "logging",
        "numpy",
        "pandas",
    }
)


def restricted_import(
    name,
    globals=None,
    locals=None,
    fromlist=(),
    level=0,
    orig_import=None,
):
    # HACK: only restrict imports on user's main module
    #
    # At this point we might actually just want to parse the file's AST
    # and match imports that way...
    is_main_mod = (globals is not None) and globals["__file__"] == "__fw_special__.py"
    first_atom = name.split(".")[0]
    if (not is_main_mod) or first_atom in ALLOWED_EXTERNAL_DEPS:
        assert orig_import is not None
        return orig_import(name, globals, locals, fromlist, level)
    else:
        raise ImportError(f"Import of module {name} is not allowed")


def exec_flumina_script(
    file_path: os.PathLike, exec_mode=_ExecMode.EXPORT, device="cuda"
):
    if not os.path.isfile(file_path):
        raise RuntimeError(f"File {file_path} does not exist.")
    with open(file_path, "r") as file:
        code = file.read()
    orig_import = builtins.__import__
    builtins.__import__ = partial(restricted_import, orig_import=orig_import)
    try:
        with _with_exec_mode(exec_mode), torch.device(device):
            code_obj = compile(code, file_path, "exec")
            restricted_globals = {
                "__builtins__": builtins,
                "__name__": "__flumina_main__",
                "__import__": restricted_import,
                "__file__": "__fw_special__.py",
            }
            exec(code_obj, restricted_globals)
    finally:
        builtins.__import__ = orig_import

    if exec_mode == _ExecMode.EXPORT:
        return _get_exported_module(), code
    elif exec_mode == _ExecMode.SERVE:
        return _get_initialized_module(), code
    else:
        raise NotImplementedError("Unsupported exec_mode", exec_mode)
