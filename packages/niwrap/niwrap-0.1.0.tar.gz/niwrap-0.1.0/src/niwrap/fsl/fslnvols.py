# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

FSLNVOLS_METADATA = Metadata(
    id="3a2d3f7f4ac51c2cdbc37faf865b81554d950f93.boutiques",
    name="fslnvols",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class FslnvolsOutputs(typing.NamedTuple):
    """
    Output object returned when calling `fslnvols(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def fslnvols(
    infile: InputPathType,
    runner: Runner | None = None,
) -> FslnvolsOutputs:
    """
    Retrieve the number of volumes in a 4D NIfTI file.
    
    Author: FMRIB Centre, University of Oxford
    
    Args:
        infile: Input NIfTI file (e.g., fmri.nii.gz).
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `FslnvolsOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(FSLNVOLS_METADATA)
    cargs = []
    cargs.append("fslnvols")
    cargs.append(execution.input_file(infile))
    ret = FslnvolsOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "FSLNVOLS_METADATA",
    "FslnvolsOutputs",
    "fslnvols",
]
