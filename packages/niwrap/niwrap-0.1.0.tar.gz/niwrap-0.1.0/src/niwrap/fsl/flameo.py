# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

FLAMEO_METADATA = Metadata(
    id="9745eb3554f097df3abe6c51ae3c2812def42029.boutiques",
    name="flameo",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class FlameoOutputs(typing.NamedTuple):
    """
    Output object returned when calling `flameo(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    dummy_output: OutputPathType


def flameo(
    runner: Runner | None = None,
) -> FlameoOutputs:
    """
    Automatic nipype2boutiques conversion failed.
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `FlameoOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(FLAMEO_METADATA)
    cargs = []
    cargs.append("dummy")
    ret = FlameoOutputs(
        root=execution.output_file("."),
        dummy_output=execution.output_file("dummy_output.txt"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "FLAMEO_METADATA",
    "FlameoOutputs",
    "flameo",
]
