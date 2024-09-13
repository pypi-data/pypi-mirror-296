# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3DPC_METADATA = Metadata(
    id="2ca991097ca258f9139795385db58ddbb0bb2f3e.boutiques",
    name="3dpc",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dpcOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3dpc(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_dataset: OutputPathType
    """Output dataset file"""
    output_header: OutputPathType
    """Output dataset header file"""
    output_eig: OutputPathType
    """File with computed eigenvalues"""
    output_vec: OutputPathType
    """File with all eigen-timeseries"""
    output_individual_vec: OutputPathType
    """File with individual eigenvalue timeseries"""


def v_3dpc(
    runner: Runner | None = None,
) -> V3dpcOutputs:
    """
    Principal Component Analysis of 3D Datasets.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dpc.html
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dpcOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3DPC_METADATA)
    cargs = []
    cargs.append("3dpc")
    cargs.append("[OPTIONS]")
    cargs.append("[INPUT_DATASETS...]")
    ret = V3dpcOutputs(
        root=execution.output_file("."),
        output_dataset=execution.output_file("[PREFIX]+orig.BRIK"),
        output_header=execution.output_file("[PREFIX]+orig.HEAD"),
        output_eig=execution.output_file("[PREFIX]_eig.1D"),
        output_vec=execution.output_file("[PREFIX]_vec.1D"),
        output_individual_vec=execution.output_file("[PREFIX][NN].1D"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dpcOutputs",
    "V_3DPC_METADATA",
    "v_3dpc",
]
