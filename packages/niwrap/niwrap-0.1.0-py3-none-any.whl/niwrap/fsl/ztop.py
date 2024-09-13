# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

ZTOP_METADATA = Metadata(
    id="e4c30ece98812c62571d5c880c34f6fd9b46b17f.boutiques",
    name="ztop",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class ZtopOutputs(typing.NamedTuple):
    """
    Output object returned when calling `ztop(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def ztop(
    z_score: float,
    tail_flag: bool = False,
    grf_flag: bool = False,
    number_of_resels: float | None = None,
    runner: Runner | None = None,
) -> ZtopOutputs:
    """
    Converts a z-score to a p-value.
    
    Args:
        z_score: Input z-score.
        tail_flag: Use 2-tailed conversion (default is 1-tailed).
        grf_flag: Use GRF maximum-height theory instead of Gaussian PDF.
        number_of_resels: Number of resels (resolution elements) for GRF\
            correction.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `ZtopOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(ZTOP_METADATA)
    cargs = []
    cargs.append("ztop")
    cargs.append(str(z_score))
    if tail_flag:
        cargs.append("-2")
    if grf_flag:
        cargs.append("-g")
    if number_of_resels is not None:
        cargs.append(str(number_of_resels))
    ret = ZtopOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "ZTOP_METADATA",
    "ZtopOutputs",
    "ztop",
]
