# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

FSLMERGE_METADATA = Metadata(
    id="ef048ed2cfafa159d4abdde743e604efb694c7e4.boutiques",
    name="fslmerge",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class FslmergeOutputs(typing.NamedTuple):
    """
    Output object returned when calling `fslmerge(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    outfile: OutputPathType
    """Output concatenated image file"""


def fslmerge(
    output_file: str,
    input_files: list[InputPathType],
    merge_set_tr: bool = False,
    tr_value: float | None = None,
    runner: Runner | None = None,
) -> FslmergeOutputs:
    """
    FSL tool to concatenate images in various dimensions.
    
    Author: Oxford Centre for Functional MRI of the Brain (FMRIB)
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Fslutils
    
    Args:
        output_file: Output concatenated image file.
        input_files: Input image files to concatenate.
        merge_set_tr: Concatenate images in time and set the output image tr to\
            the provided value.
        tr_value: TR value in seconds, used with the -tr flag.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `FslmergeOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(FSLMERGE_METADATA)
    cargs = []
    cargs.append("fslmerge")
    if merge_set_tr:
        cargs.append("-tr")
    cargs.append(output_file)
    cargs.extend([execution.input_file(f) for f in input_files])
    if tr_value is not None:
        cargs.append(str(tr_value))
    ret = FslmergeOutputs(
        root=execution.output_file("."),
        outfile=execution.output_file(output_file + ".nii.gz"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "FSLMERGE_METADATA",
    "FslmergeOutputs",
    "fslmerge",
]
