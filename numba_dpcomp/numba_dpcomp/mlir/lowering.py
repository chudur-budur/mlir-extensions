# Copyright 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Define lowering and related passes.
"""

from .passes import MlirDumpPlier, MlirBackend
from .settings import USE_MLIR

from numba.core.compiler_machinery import register_pass

from numba.core.lowering import Lower as orig_Lower
from numba.core.typed_passes import NativeLowering as orig_NativeLowering

# looks like that we don't need it but it is inherited from BaseLower too
# from numba.core.pylowering import PyLower as orig_PyLower

from .runtime import *
from .math_runtime import *
from .numba_runtime import *
from .gpu_runtime import *

import llvmlite.binding as llvm


class mlir_lower(orig_Lower):
    def lower(self):
        if USE_MLIR:
            self.emit_environment_object()
            self.genlower = None
            self.lower_normal_function(self.fndesc)
            self.context.post_lowering(self.module, self.library)
        else:
            orig_Lower.lower(self)

    def lower_normal_function(self, fndesc):
        if USE_MLIR:
            self.setup_function(fndesc)

            # Skip check that all numba symbols defined
            setattr(self.library, "_verify_declare_only_symbols", lambda: None)
            func_ptr = self.metadata.pop("mlir_func_ptr")
            func_name = self.metadata.pop("mlir_func_name")

            # TODO: Construct new ir module instead of globally registering symbol
            llvm.add_symbol(func_name, func_ptr)
        else:
            orig_Lower.lower_normal_function(self, desc)


@register_pass(mutates_CFG=True, analysis_only=False)
class mlir_NativeLowering(orig_NativeLowering):
    def __init__(self):
        orig_NativeLowering.__init__(self)

    def run_pass(self, state):
        import numba.core.lowering

        numba.core.lowering.Lower = mlir_lower
        try:
            res = orig_NativeLowering.run_pass(self, state)
        finally:
            numba.core.lowering.Lower = orig_Lower
        return res
