# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

FSLANIMATE_METADATA = Metadata(
    id="0c9b52cf6ff1f6b9170640b9650385ae43ab9954.boutiques",
    name="fslanimate",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class FslanimateOutputs(typing.NamedTuple):
    """
    Output object returned when calling `fslanimate(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_animation: OutputPathType
    """The resulting animation file"""


def fslanimate(
    input_file: InputPathType,
    output_file: str,
    tmp_dir: str | None = None,
    runner: Runner | None = None,
) -> FslanimateOutputs:
    """
    Tool for creating animations from imaging data.
    
    Author: Oxford Centre for Functional MRI of the Brain (FMRIB)
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki
    
    Args:
        input_file: Input image file (e.g., input.nii.gz).
        output_file: Output file (e.g., output.gif).
        tmp_dir: Temporary directory for intermediate files.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `FslanimateOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(FSLANIMATE_METADATA)
    cargs = []
    cargs.append("fslanimate")
    cargs.append(execution.input_file(input_file))
    cargs.append(output_file)
    if tmp_dir is not None:
        cargs.append(tmp_dir)
    ret = FslanimateOutputs(
        root=execution.output_file("."),
        output_animation=execution.output_file(output_file),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "FSLANIMATE_METADATA",
    "FslanimateOutputs",
    "fslanimate",
]
