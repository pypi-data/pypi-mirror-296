# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

FSLSPLIT_METADATA = Metadata(
    id="0437d7a80ec1e0e35ca9e21fabd9655c69b443b2.boutiques",
    name="fslsplit",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class FslsplitOutputs(typing.NamedTuple):
    """
    Output object returned when calling `fslsplit(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    outfiles: OutputPathType | None
    """Output volumes/slices"""


def fslsplit(
    infile: InputPathType,
    output_basename: str | None = "vol",
    separation_z: bool = False,
    runner: Runner | None = None,
) -> FslsplitOutputs:
    """
    Split a 4D image into separate volumes or a 3D image into separate slices.
    
    Author: Oxford Centre for Functional MRI of the Brain (FMRIB)
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Fslutils
    
    Args:
        infile: Input image (e.g. img.nii.gz).
        output_basename: Output basename (default: vol).
        separation_z: Separate images in the z direction.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `FslsplitOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(FSLSPLIT_METADATA)
    cargs = []
    cargs.append("fslsplit")
    cargs.append(execution.input_file(infile))
    if output_basename is not None:
        cargs.append(output_basename)
    if separation_z:
        cargs.append("-z")
    ret = FslsplitOutputs(
        root=execution.output_file("."),
        outfiles=execution.output_file(output_basename + "????.nii.gz") if (output_basename is not None) else None,
    )
    execution.run(cargs)
    return ret


__all__ = [
    "FSLSPLIT_METADATA",
    "FslsplitOutputs",
    "fslsplit",
]
