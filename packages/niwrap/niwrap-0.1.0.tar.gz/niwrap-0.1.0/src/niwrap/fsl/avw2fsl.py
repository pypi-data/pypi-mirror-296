# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

AVW2FSL_METADATA = Metadata(
    id="3110b2aae1aa53c6a38d7d7ec34da42b9d6614c8.boutiques",
    name="avw2fsl",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class Avw2fslOutputs(typing.NamedTuple):
    """
    Output object returned when calling `avw2fsl(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_dest: OutputPathType
    """Destination file or directory where the source is copied."""


def avw2fsl(
    runner: Runner | None = None,
) -> Avw2fslOutputs:
    """
    Processing script to copy files and directories.
    
    Author: GNU coreutils
    
    URL: http://www.gnu.org/software/coreutils/
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `Avw2fslOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(AVW2FSL_METADATA)
    cargs = []
    cargs.append("/bin/cp")
    cargs.append("[OPTIONS]")
    cargs.append("[SOURCE")
    cargs.append("DEST]")
    ret = Avw2fslOutputs(
        root=execution.output_file("."),
        output_dest=execution.output_file("[DEST]"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "AVW2FSL_METADATA",
    "Avw2fslOutputs",
    "avw2fsl",
]
