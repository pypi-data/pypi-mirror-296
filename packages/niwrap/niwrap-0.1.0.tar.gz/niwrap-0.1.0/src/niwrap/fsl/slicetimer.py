# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

SLICETIMER_METADATA = Metadata(
    id="4720d9135dcde74cc0db05cf9e44c6a1d33e2f76.boutiques",
    name="slicetimer",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class SlicetimerOutputs(typing.NamedTuple):
    """
    Output object returned when calling `slicetimer(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_timeseries: OutputPathType
    """Output timeseries"""


def slicetimer(
    infile: InputPathType,
    runner: Runner | None = None,
) -> SlicetimerOutputs:
    """
    FMRIB's Interpolation for Slice Timing.
    
    Author: University of Oxford, FMRIB
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Slicetimer
    
    Args:
        infile: Filename of input timeseries.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `SlicetimerOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(SLICETIMER_METADATA)
    cargs = []
    cargs.append("slicetimer")
    cargs.append("-i")
    cargs.extend([
        "-i",
        execution.input_file(infile)
    ])
    cargs.append("[-o")
    cargs.append("OUTPUT_FILE]")
    cargs.append("[--down]")
    cargs.append("[-r")
    cargs.append("TR_VALUE]")
    cargs.append("[-d")
    cargs.append("DIRECTION]")
    cargs.append("[--odd]")
    cargs.append("[--tcustom")
    cargs.append("TCUSTOM_FILE]")
    cargs.append("[--tglobal")
    cargs.append("TGLOBAL_VALUE]")
    cargs.append("[--ocustom")
    cargs.append("OCUSTOM_FILE]")
    cargs.append("[-v]")
    ret = SlicetimerOutputs(
        root=execution.output_file("."),
        output_timeseries=execution.output_file("[OUTPUT_FILE]"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "SLICETIMER_METADATA",
    "SlicetimerOutputs",
    "slicetimer",
]
