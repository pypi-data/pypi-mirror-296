# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_1D_BPORT_METADATA = Metadata(
    id="01b482fa8f60ea7e37aea665b40cbc47eab52f74.boutiques",
    name="1dBport",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V1dBportOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_1d_bport(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    stdout: OutputPathType
    """Standard output file written by the tool"""


def v_1d_bport(
    band: list[float],
    invert: bool = False,
    noconst: bool = False,
    quad: bool = False,
    input_dataset: InputPathType | None = None,
    input_1d_file: InputPathType | None = None,
    nodata: list[float] | None = None,
    tr: float | None = None,
    concat: InputPathType | None = None,
    runner: Runner | None = None,
) -> V1dBportOutputs:
    """
    Creates a set of columns of sines and cosines for bandpassing via regression.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/1dBport.html
    
    Args:
        band: Specify lowest and highest frequencies in the passband.
        invert: Invert the selection after computing which frequency indexes\
            correspond to the input band(s).
        noconst: Same as -nozero. Do NOT generate the 0 frequency (constant)\
            component when fbot = 0.
        quad: Add regressors for linear and quadratic trends.
        input_dataset: Specify the dataset input.
        input_1d_file: Specify the 1D input file.
        nodata: Specify the number of time points and optionally TR value for\
            the simulation.
        tr: Set the time step duration.
        concat: Specify the list of start indexes for concatenated runs.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V1dBportOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_1D_BPORT_METADATA)
    cargs = []
    cargs.append("1dBport")
    cargs.extend([
        "-band",
        *map(str, band)
    ])
    if invert:
        cargs.append("-invert")
    if noconst:
        cargs.append("-noconst")
    if quad:
        cargs.append("-quad")
    if input_dataset is not None:
        cargs.extend([
            "-input",
            execution.input_file(input_dataset)
        ])
    if input_1d_file is not None:
        cargs.extend([
            "-input1D",
            execution.input_file(input_1d_file)
        ])
    if nodata is not None:
        cargs.extend([
            "-nodata",
            *map(str, nodata)
        ])
    if tr is not None:
        cargs.extend([
            "-TR",
            str(tr)
        ])
    if concat is not None:
        cargs.extend([
            "-concat",
            execution.input_file(concat)
        ])
    ret = V1dBportOutputs(
        root=execution.output_file("."),
        stdout=execution.output_file("stdout"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V1dBportOutputs",
    "V_1D_BPORT_METADATA",
    "v_1d_bport",
]
