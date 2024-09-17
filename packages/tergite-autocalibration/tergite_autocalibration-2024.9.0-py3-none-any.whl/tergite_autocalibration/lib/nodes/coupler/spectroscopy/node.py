# This code is part of Tergite
#
# (C) Copyright Eleftherios Moschandreou 2023, 2024
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from pathlib import Path

import numpy as np
from scipy import optimize as optimize

from tergite_autocalibration.utils.dto.enums import MeasurementMode
from tergite_autocalibration.utils.hardware_utils import SpiDAC
from tergite_autocalibration.utils.user_input import qubit_samples, resonator_samples
from .analysis import (
    CouplerSpectroscopyAnalysis,
)
from ...qubit_control.spectroscopy.measurement import (
    Two_Tones_Multidim,
)
from ...readout.resonator_spectroscopy.measurement import Resonator_Spectroscopy
from ....base.node import BaseNode


class Coupler_Spectroscopy_Node(BaseNode):
    measurement_obj = Two_Tones_Multidim
    analysis_obj = CouplerSpectroscopyAnalysis

    def __init__(
        self, name: str, all_qubits: list[str], couplers: list[str], **schedule_keywords
    ):
        super().__init__(name, all_qubits, **schedule_keywords)
        self.name = name
        self.all_qubits = all_qubits  # this is a Base attr, delete it here
        self.couplers = couplers
        self.redis_field = ["parking_current"]
        self.qubit_state = 0
        self.type = "spi_and_cluster_simple_sweep"
        # perform 2 tones while biasing the current
        self.coupled_qubits = self.get_coupled_qubits()
        self.coupler = self.couplers[0]
        mode = MeasurementMode.real
        self.spi_dac = SpiDAC(mode)
        self.dac = self.spi_dac.create_spi_dac(self.coupler)

        self.all_qubits = self.coupled_qubits

        self.schedule_samplespace = {
            "spec_frequencies": {
                qubit: qubit_samples(qubit) for qubit in self.all_qubits
            }
        }

        self.external_samplespace = {
            "dc_currents": {self.coupler: np.arange(-2.5e-3, 2.5e-3, 150e-6)},
        }
        # self.validate()

    def get_coupled_qubits(self) -> list:
        if len(self.couplers) > 1:
            print("Multiple couplers, lets work with only one")
        coupled_qubits = self.couplers[0].split(sep="_")
        self.coupler = self.couplers[0]
        return coupled_qubits

    def pre_measurement_operation(self, reduced_ext_space):
        iteration_dict = reduced_ext_space["dc_currents"]
        # there is some redundancy tha all qubits have the same
        # iteration index, that's why we keep the first value->

        this_iteration_value = list(iteration_dict.values())[0]
        print(f"{ this_iteration_value = }")
        self.spi_dac.set_dac_current(self.dac, this_iteration_value)

    def calibrate(self, data_path: Path, lab_ic, cluster_status):
        print("Performing optimized Sweep")
        compiled_schedule = self.precompile(data_path)

        optimization_element = "q13_q14"

        optimization_guess = 100e-6

        spi = SpiDAC()
        dac = spi.create_spi_dac(optimization_element)

        def set_optimizing_parameter(optimizing_parameter):
            if self.name == "cz_chevron_optimize":
                spi.set_dac_current(dac, optimizing_parameter)

        def single_sweep(optimizing_parameter) -> float:
            set_optimizing_parameter(optimizing_parameter)

            result_dataset = self.measure_node(
                compiled_schedule,
                lab_ic,
                data_path,
                cluster_mode=MeasurementMode.real,
            )

            measurement_result_ = self.post_process(result_dataset, data_path=data_path)

            optimization_quantity = measurement_result_[optimization_element][
                self.optimization_field
            ]

            return optimization_quantity

        optimize.minimize(
            single_sweep,
            optimization_guess,
            method="Nelder-Mead",
            bounds=[(80e-6, 120e-6)],
            options={"maxiter": 2},
        )

        # TODO MERGE-CZ-GATE: I guess this is under active development, so, we do not have a measurement_result?
        return None


class Coupler_Resonator_Spectroscopy_Node(BaseNode):
    measurement_obj = Resonator_Spectroscopy
    analysis_obj = CouplerSpectroscopyAnalysis

    def __init__(
        self, name: str, all_qubits: list[str], couplers: list[str], **schedule_keywords
    ):
        super().__init__(name, all_qubits, **schedule_keywords)
        self.redis_field = ["resonator_flux_quantum"]
        self.qubit_state = 0
        self.couplers = couplers
        self.coupler = self.couplers[0]
        mode = MeasurementMode.real
        self.spi_dac = SpiDAC(mode)
        self.dac = self.spi_dac.create_spi_dac(self.coupler)
        self.coupled_qubits = self.get_coupled_qubits()

        self.all_qubits = self.coupled_qubits

        self.schedule_samplespace = {
            "ro_frequencies": {
                qubit: resonator_samples(qubit) for qubit in self.all_qubits
            }
        }

        self.external_samplespace = {
            "dc_currents": {self.coupler: np.arange(-2.5e-3, 2.5e-3, 500e-6)},
        }

    def get_coupled_qubits(self) -> list:
        if len(self.couplers) > 1:
            print("Multiple couplers, lets work with only one")
        coupled_qubits = self.couplers[0].split(sep="_")
        self.coupler = self.couplers[0]
        return coupled_qubits

    def pre_measurement_operation(self, reduced_ext_space):
        iteration_dict = reduced_ext_space["dc_currents"]
        # there is some redundancy tha all qubits have the same
        # iteration index, that's why we keep the first value->

        this_iteration_value = list(iteration_dict.values())[0]
        print(f"{ this_iteration_value = }")
        self.spi_dac.set_dac_current(self.dac, this_iteration_value)
