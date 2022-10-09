// Copyright 2022 Intel Corporation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#include <memory>

namespace mlir {
class MLIRContext;
class Pass;
class RewritePatternSet;
} // namespace mlir

namespace gpu_runtime {
void populateMakeBarriersUniformPatterns(mlir::MLIRContext &context,
                                         mlir::RewritePatternSet &patterns);

/// gpu barriers ops require uniform control flow, this pass tries to rearrange
/// control flow in a way to satisfy this requirement.
std::unique_ptr<mlir::Pass> createMakeBarriersUniformPass();
} // namespace gpu_runtime