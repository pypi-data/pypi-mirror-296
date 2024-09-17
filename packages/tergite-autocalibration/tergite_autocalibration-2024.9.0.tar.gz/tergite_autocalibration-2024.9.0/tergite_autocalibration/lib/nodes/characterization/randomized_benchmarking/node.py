# This code is part of Tergite
#
# (C) Copyright Eleftherios Moschandreou 2024
# (C) Copyright Liangyu Chen 2024
# (C) Copyright Amr Osman 2024
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import numpy as np

from .analysis import RandomizedBenchmarkingAnalysis
from .measurement import Randomized_Benchmarking
from ....utils.node_subclasses import ParametrizedSweepNode


class Randomized_Benchmarking_Node(ParametrizedSweepNode):
    measurement_obj = Randomized_Benchmarking
    analysis_obj = RandomizedBenchmarkingAnalysis

    def __init__(self, name: str, all_qubits: list[str], **schedule_keywords):
        super().__init__(name, all_qubits, **schedule_keywords)
        self.name = name
        self.type = "parameterized_sweep"
        self.all_qubits = all_qubits
        self.schedule_keywords = schedule_keywords
        self.backup = False
        self.redis_field = ["fidelity"]
        self.schedule_keywords = {}

        self.initial_schedule_samplespace = {
            "number_of_cliffords": {
                # qubit: all_numbers for qubit in self.all_qubits
                # qubit: np.array([2, 16, 128, 256,512, 768, 1024, 0, 1]) for qubit in self.all_qubits
                qubit: np.array([0, 2, 4, 8, 16, 128, 256, 512, 1024, 0, 1, 2])
                for qubit in self.all_qubits
            },
        }

        self.external_samplespace = {
            "seeds": {qubit: np.arange(5, dtype=np.int32) for qubit in self.all_qubits}
        }

    def pre_measurement_operation(self, reduced_ext_space: dict):
        self.schedule_samplespace = (
            self.initial_schedule_samplespace | reduced_ext_space
        )
