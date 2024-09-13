# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

TTOZ_METADATA = Metadata(
    id="a909a0eee6e1f0850e3a86e6e4ffa8ff91713090.boutiques",
    name="ttoz",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class TtozOutputs(typing.NamedTuple):
    """
    Output object returned when calling `ttoz(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_zvol: OutputPathType
    """Output Z-statistic volume"""


def ttoz(
    runner: Runner | None = None,
) -> TtozOutputs:
    """
    Tool to convert a T-statistic image to a Z-statistic image.
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `TtozOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(TTOZ_METADATA)
    cargs = []
    cargs.append("ttoz")
    cargs.append("[OPTIONS]")
    cargs.append("<varsfile>")
    cargs.append("<cbsfile>")
    cargs.append("<dof>")
    ret = TtozOutputs(
        root=execution.output_file("."),
        output_zvol=execution.output_file("[OUTPUTVOL].nii.gz"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "TTOZ_METADATA",
    "TtozOutputs",
    "ttoz",
]
