# This code is part of Tergite
#
# (C) Copyright Eleftherios Moschandreou 2023, 2024
# (C) Copyright Liangyu Chen 2023, 2024
# (C) Copyright Stefan Hill 2024
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import abc
import collections
import json
import threading
import time
import warnings
from collections.abc import Iterable
from pathlib import Path
from typing import List, Optional

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import tqdm
import xarray
import xarray as xr
from colorama import Fore
from colorama import Style
from colorama import init as colorama_init
from quantify_scheduler.backends import SerialCompiler
from quantify_scheduler.device_under_test.quantum_device import QuantumDevice
from quantify_scheduler.instrument_coordinator.instrument_coordinator import (
    CompiledSchedule,
)
from quantify_scheduler.json_utils import SchedulerJSONEncoder
from quantify_scheduler.json_utils import pathlib

from tergite_autocalibration.config import settings
from tergite_autocalibration.config.settings import REDIS_CONNECTION, HARDWARE_CONFIG
from tergite_autocalibration.experimental.tof_analysis import analyze_tof
from tergite_autocalibration.lib.base.analysis import BaseAnalysis
from tergite_autocalibration.lib.base.measurement import BaseMeasurement
from tergite_autocalibration.lib.utils.demod_channels import ParallelDemodChannels
from tergite_autocalibration.lib.utils.redis import (
    load_redis_config,
    load_redis_config_coupler,
)
from tergite_autocalibration.tools.mss.convert import structured_redis_storage
from tergite_autocalibration.utils.dataset_utils import (
    configure_dataset,
    retrieve_dummy_dataset,
    save_dataset,
)
from tergite_autocalibration.utils.dto.enums import DataStatus
from tergite_autocalibration.utils.dto.enums import MeasurementMode
from tergite_autocalibration.utils.extended_coupler_edge import CompositeSquareEdge
from tergite_autocalibration.utils.extended_transmon_element import ExtendedTransmon
from tergite_autocalibration.utils.logger.tac_logger import logger
from tergite_autocalibration.utils.post_processing_utils import manage_plots

colorama_init()


with open(HARDWARE_CONFIG) as hw:
    hw_config = json.load(hw)

matplotlib.use(settings.PLOTTING_BACKEND)


class BaseNode(abc.ABC):
    measurement_obj: "BaseMeasurement"
    analysis_obj: "BaseAnalysis"

    def __init__(self, name: str, all_qubits: list[str], **node_dictionary):
        self.name = name
        self.all_qubits = all_qubits
        self.node_dictionary = node_dictionary
        self.backup = False
        self.type = "simple_sweep"  # TODO better as Enum type
        self.qubit_state = 0  # can be 0 or 1 or 2
        self.plots_per_qubit = 1  # can be 0 or 1 or 2
        self.build_demod_channels()

        self.redis_field: List[str]
        self.coupler: Optional[List[str]]

        self.lab_instr_coordinator = None

        self.schedule_samplespace = {}
        self.external_samplespace = {}
        self.initial_schedule_samplespace = {}
        self.schedule_keywords = {}
        self.reduced_external_samplespace = {}

        self.samplespace = self.schedule_samplespace | self.external_samplespace

    def pre_measurement_operation(self):
        """
        To be implemented by the child measurement nodes
        """
        pass

    @property
    def dimensions(self) -> list:
        """
        array of dimensions used for raw dataset reshaping
        in utills/dataset_utils.py. some nodes have peculiar dimensions
        e.g. randomized benchmarking and need dimension definition in their class
        """
        schedule_settable_quantities = self.schedule_samplespace.keys()

        # no schedule_samplespace applies on to sc_qubit_spectroscopy
        if len(list(schedule_settable_quantities)) == 0:
            return [1]

        # keeping the first element, ASSUMING that all settable elements
        # have the same dimensions on their samplespace

        first_settable = list(schedule_settable_quantities)[0]
        measured_elements = self.schedule_samplespace[first_settable].keys()
        first_element = list(measured_elements)[0]

        dimensions = []

        for quantity in schedule_settable_quantities:
            settable_values = self.schedule_samplespace[quantity][first_element]
            if not isinstance(settable_values, Iterable):
                settable_values = np.array([settable_values])
            dimensions.append(len(settable_values))

        if self.external_samplespace != {} and self.initial_schedule_samplespace == {}:
            dimensions = dimensions + [1]
        return dimensions

    @property
    def external_dimensions(self) -> list:
        """
        array of dimensions used for raw dataset reshaping
        in utills/dataset_utils.py. some nodes have peculiar dimensions
        e.g. randomized benchmarking and need dimension definition in their class
        """
        external_settable_quantities = self.external_samplespace.keys()

        # keeping the first element, ASSUMING that all settable elements
        # have the same dimensions on their samplespace
        # i.e. all qubits have the same number of ro frequency samples in readout spectroscopy
        first_settable = list(external_settable_quantities)[0]
        measured_elements = self.external_samplespace[first_settable].keys()
        first_element = list(measured_elements)[0]

        dimensions = []
        if len(dimensions) > 1:
            raise NotImplementedError("Multidimensional External Samplespace")
        for quantity in external_settable_quantities:
            dimensions.append(len(self.external_samplespace[quantity][first_element]))
        return dimensions

    def build_demod_channels(self):
        """
        The default demodulation channels are multiplexed single-qubit channels,
        which means that you only readout one qubit in parallel.
        It works when you only calibrate single qubits.
        In many cases, you also need jointly readout multiple qubits such as quantum
        state tomography.
        Rewrite this method in these nodes.

        TODO: Add parameters to the global variables
        """
        self.demod_channels = (
            ParallelDemodChannels.build_multiplexed_single_demod_channel(
                self.all_qubits, ["0", "1"], "IQ", REDIS_CONNECTION
            )
        )

    def calibrate(self, data_path: Path, lab_ic, cluster_status):
        compiled_schedule = self.precompile(data_path)

        if self.external_samplespace == {}:
            """
            This correspond to simple cluster schedules
            """
            result_dataset = self.measure_node(
                compiled_schedule,
                lab_ic,
                data_path,
                cluster_status=cluster_status,
            )
        else:
            pre_measurement_operation = self.pre_measurement_operation

            # node.external_dimensions is defined in the node_base
            iterations = self.external_dimensions[0]

            result_dataset = xarray.Dataset()

            # example of external_samplespace:
            # external_samplespace = {
            #       'cw_frequencies': {
            #          'q1': np.array(4.0e9, 4.1e9, 4.2e9),
            #          'q2': np.array(4.5e9, 4.6e9, 4.7e9),
            #        }
            # }

            # e.g. 'cw_frequencies':
            external_settable = list(self.external_samplespace.keys())[0]

            for current_iteration in range(iterations):
                reduced_external_samplespace = {}
                qubit_values = {}
                # elements may refer to qubits or couplers
                elements = self.external_samplespace[external_settable].keys()
                for element in elements:
                    qubit_specific_values = self.external_samplespace[
                        external_settable
                    ][element]
                    external_value = qubit_specific_values[current_iteration]
                    qubit_values[element] = external_value

                # example of reduced_external_samplespace:
                # reduced_external_samplespace = {
                #     'cw_frequencies': {
                #          'q1': np.array(4.2e9),
                #          'q2': np.array(4.7e9),
                #     }
                # }
                reduced_external_samplespace[external_settable] = qubit_values
                self.reduced_external_samplespace = reduced_external_samplespace
                pre_measurement_operation(
                    reduced_ext_space=reduced_external_samplespace
                )

                ds = self.measure_node(
                    compiled_schedule,
                    lab_ic,
                    data_path,
                    cluster_status,
                    measurement=(current_iteration, iterations),
                )
                result_dataset = xarray.merge([result_dataset, ds])

        logger.info("measurement completed")
        measurement_result = self.post_process(result_dataset, data_path=data_path)
        logger.info("analysis completed")
        return measurement_result

    def precompile(
        self, data_path: Path, bin_mode: str = None, repetitions: int = None
    ):
        if self.name == "tof":
            return None, 1
        qubits = self.all_qubits

        # backup old parameter values
        # TODO:
        if self.backup:
            fields = self.redis_field
            for field in fields:
                field_backup = field + "_backup"
                for qubit in qubits:
                    key = f"transmons:{qubit}"
                    if field in REDIS_CONNECTION.hgetall(key).keys():
                        value = REDIS_CONNECTION.hget(key, field)
                        REDIS_CONNECTION.hset(key, field_backup, value)
                        REDIS_CONNECTION.hset(key, field, "nan")
                        structured_redis_storage(field_backup, qubit.strip("q"), value)
                        REDIS_CONNECTION.hset(key, field, "nan")
                        structured_redis_storage(field, qubit.strip("q"), None)
                if getattr(self, "coupler", None) is not None:
                    couplers = self.coupler
                    for coupler in couplers:
                        key = f"couplers:{coupler}"
                        if field in REDIS_CONNECTION.hgetall(key).keys():
                            value = REDIS_CONNECTION.hget(key, field)
                            REDIS_CONNECTION.hset(key, field_backup, value)
                            structured_redis_storage(field_backup, coupler, value)
                            REDIS_CONNECTION.hset(key, field, "nan")
                            structured_redis_storage(key, coupler, value)

        device = QuantumDevice(f"Loki_{self.name}")
        device.hardware_config(hw_config)

        transmons = {}
        for channel, qubit in enumerate(qubits):
            transmon = ExtendedTransmon(qubit)
            transmon = load_redis_config(transmon, channel)
            device.add_element(transmon)
            transmons[qubit] = transmon

        # Creating coupler edge
        # bus_list = [ [qubits[i],qubits[i+1]] for i in range(len(qubits)-1) ]
        if hasattr(self, "edges"):
            couplers = self.edges
            edges = {}
            for bus in couplers:
                control, target = bus.split(sep="_")
                coupler = CompositeSquareEdge(control, target)
                load_redis_config_coupler(coupler)
                device.add_edge(coupler)
                edges[bus] = coupler

        if hasattr(self, "edges") or self.name in [
            "cz_chevron",
            "cz_calibration",
            "cz_calibration_ssro",
            "cz_calibration_swap_ssro",
            "cz_dynamic_phase",
            "cz_dynamic_phase_swap",
            "reset_chevron",
            "reset_calibration_ssro",
            "tqg_randomized_benchmarking",
            "tqg_randomized_benchmarking_interleaved",
        ]:
            coupler = self.coupler
            node_class = self.measurement_obj(transmons, edges, self.qubit_state)
        else:
            node_class = self.measurement_obj(transmons, self.qubit_state)
        if self.name in [
            "ro_amplitude_three_state_optimization",
            "cz_calibration_ssro",
            "cz_calibration_swap_ssro",
            "reset_calibration_ssro",
        ]:
            device.cfg_sched_repetitions(1)  # for single-shot readout
        if bin_mode is not None:
            node_class.set_bin_mode(bin_mode)

        schedule_function = node_class.schedule_function

        compiler = SerialCompiler(name=f"{self.name}_compiler")

        schedule_samplespace = self.schedule_samplespace
        external_samplespace = self.external_samplespace
        schedule_keywords = self.schedule_keywords

        schedule = schedule_function(**schedule_samplespace, **schedule_keywords)
        compilation_config = device.generate_compilation_config()

        # save_serial_device(device, data_path)

        # create a transmon with the same name but with updated config
        # get the transmon template in dictionary form
        serialized_device = json.dumps(device, cls=SchedulerJSONEncoder)
        decoded_device = json.loads(serialized_device)
        serial_device = {}
        for element, element_config in decoded_device["data"]["elements"].items():
            serial_config = json.loads(element_config)
            serial_device[element] = serial_config

        data_path.mkdir(parents=True, exist_ok=True)
        with open(f"{data_path}/{self.name}.json", "w") as f:
            json.dump(serial_device, f, indent=4)

        device.close()

        # after the compilation_config is acquired, free the transmon resources
        for extended_transmon in transmons.values():
            extended_transmon.close()
        if hasattr(self, "edges"):
            for extended_edge in edges.values():
                extended_edge.close()

        logger.info("Starting Compiling")

        compiled_schedule = compiler.compile(
            schedule=schedule, config=compilation_config
        )

        return compiled_schedule

    def measure_node(
        self,
        compiled_schedule: CompiledSchedule,
        lab_ic,
        data_path: pathlib.Path,
        cluster_status=MeasurementMode.real,
        measurement=(1, 1),
    ):
        schedule_duration = compiled_schedule.get_schedule_duration()
        if "loop_repetitions" in self.node_dictionary:
            schedule_duration *= self.node_dictionary["loop_repetitions"]

        measurement_message = ""
        if measurement[1] > 1:
            measurement_message = (
                f". Measurement {measurement[0] + 1} of {measurement[1]}"
            )
        message = f"{schedule_duration:.2f} sec" + measurement_message
        print(
            f"schedule_duration = {Fore.CYAN}{Style.BRIGHT}{message}{Style.RESET_ALL}"
        )

        raw_dataset = self.execute_schedule(
            compiled_schedule, lab_ic, schedule_duration, cluster_status
        )

        if cluster_status == MeasurementMode.real:
            result_dataset = configure_dataset(raw_dataset, self)
            save_dataset(result_dataset, self.name, data_path)
        else:
            result_dataset = retrieve_dummy_dataset(self)

        logger.info("Finished measurement")
        return result_dataset

    def execute_schedule(
        self,
        compiled_schedule: CompiledSchedule,
        lab_ic,
        schedule_duration: float,
        cluster_status,
    ) -> xarray.Dataset:
        # TODO: Could move to helper function, because is static

        logger.info("Starting measurement")

        def run_measurement() -> None:
            lab_ic.prepare(compiled_schedule)
            lab_ic.start()
            lab_ic.wait_done(timeout_sec=3600)

        def display_progress():
            steps = int(schedule_duration * 5)
            if cluster_status == MeasurementMode.dummy:
                progress_sleep = 0.004
            elif cluster_status == MeasurementMode.real:
                progress_sleep = 0.2
            for _ in tqdm.tqdm(
                range(steps), desc=compiled_schedule.name, colour="blue"
            ):
                time.sleep(progress_sleep)

        thread_tqdm = threading.Thread(target=display_progress)
        thread_tqdm.start()
        thread_lab = threading.Thread(target=run_measurement)
        thread_lab.start()
        thread_lab.join()
        thread_tqdm.join()

        raw_dataset: xarray.Dataset = lab_ic.retrieve_acquisition()
        lab_ic.stop()
        logger.info("Raw dataset acquired")

        return raw_dataset

    def post_process(self, result_dataset: xr.Dataset, data_path: Path):
        if self.name == "tof":
            tof = analyze_tof(result_dataset, True)
            return

        column_grid = 5
        fig, axs = manage_plots(result_dataset, column_grid, self.plots_per_qubit)

        qoi: list
        data_status: DataStatus

        data_vars_dict = collections.defaultdict(set)
        for var in result_dataset.data_vars:
            this_qubit = result_dataset[var].attrs["qubit"]
            data_vars_dict[this_qubit].add(var)

        all_results = {}
        for indx, var in enumerate(result_dataset.data_vars):
            # this refers to the qubit whose resonator was used for the measurement
            # not necessarily the element where the settable was applied
            this_qubit = result_dataset[var].attrs["qubit"]
            this_element = this_qubit
            # print(f'{result_dataset = }')

            ds = xr.Dataset()
            for var in data_vars_dict[this_qubit]:
                ds = xr.merge([ds, result_dataset[var]])

            ds.attrs["qubit"] = this_qubit
            ds.attrs["node"] = self.name
            # print(f'{ds = }')
            # detect the element_type on which the settables act
            for settable in ds.coords:
                # print(f'{settable = }')
                # print(f'{ds[settable].attrs = }')
                try:
                    if ds[settable].attrs["element_type"] == "coupler":
                        element_type = "coupler"
                        # print(f'{ds[settable].attrs[element_type] = }')
                        this_element = ds[settable].attrs[element_type]
                        # print(f'{this_element = }')
                except:
                    print(f"No element_type for {settable}")
                    # pass

            primary_plot_row = self.plots_per_qubit * (indx // column_grid)
            primary_axis = axs[primary_plot_row, indx % column_grid]

            redis_field = self.redis_field
            analysis_kwargs = getattr(self, "analysis_kwargs", dict())
            node_analysis = self.analysis_obj(ds, **analysis_kwargs)
            qoi = node_analysis.run_fitting()

            node_analysis.qoi = qoi

            if self.type == "adaptive_sweep":
                # TODO: Is there even an adaptive sweep anywere?
                # fetch relative kwargs, e.g. known minima in motzoi calibration
                qubit_adaptive_kwargs = self.adaptive_kwargs[this_qubit]
                # every adaptive iteration should update the samplespace ...
                new_qubit_samplespace = node_analysis.updated_qubit_samplespace(
                    **qubit_adaptive_kwargs
                )
                for settable_key in new_qubit_samplespace.keys():
                    self.samplespace[settable_key].update(
                        new_qubit_samplespace[settable_key]
                    )
                # every adaptive iteration should also update the relevant kwargs
                self.adaptive_kwargs[this_qubit] = node_analysis.updated_kwargs
                if self.measurement_is_completed:
                    node_analysis.update_redis_trusted_values(
                        self.name, this_qubit, redis_field
                    )
            # print(f'{this_element = }')
            node_analysis.update_redis_trusted_values(
                self.name, this_element, redis_field
            )
            all_results[this_element] = dict(zip(redis_field, qoi))

            if self.plots_per_qubit > 1:
                list_of_secondary_axes = []
                for plot_indx in range(1, self.plots_per_qubit):
                    secondary_plot_row = primary_plot_row + plot_indx
                    list_of_secondary_axes.append(
                        axs[secondary_plot_row, indx % column_grid]
                    )
                node_analysis.plotter(
                    primary_axis, secondary_axes=list_of_secondary_axes
                )
            else:
                node_analysis.plotter(primary_axis)
            handles, labels = primary_axis.get_legend_handles_labels()

            patch = mpatches.Patch(color="red", label=f"{this_qubit}")
            handles.append(patch)
            primary_axis.legend(handles=handles, fontsize="small")
            if self.plots_per_qubit > 1:
                for secondary_ax in list_of_secondary_axes:
                    secondary_ax.legend()

        fig = plt.gcf()
        fig.set_tight_layout(True)
        try:
            fig.savefig(f"{data_path}/{self.name}.png", bbox_inches="tight", dpi=400)
            fig.savefig(
                f"{data_path}/{self.name}_preview.png", bbox_inches="tight", dpi=100
            )
        except FileNotFoundError:
            warnings.warn("File Not existing")
            pass
        plt.show(block=False)
        plt.pause(5)
        plt.close()
        if self != "tof":
            all_results.update({"measurement_dataset": result_dataset.to_dict()})

        return all_results

    def __str__(self):
        return f"Node representation for {self.name} on qubits {self.all_qubits}"

    def __format__(self, message):
        return f"Node representation for {self.name} on qubits {self.all_qubits}"

    def __repr__(self):
        return f"Node({self.name}, {self.all_qubits})"
