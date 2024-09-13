# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__PURIFY_1_D_METADATA = Metadata(
    id="813b07d61e5f245a5171c379d84ac0cea433dad8.boutiques",
    name="@Purify_1D",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VPurify1DOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__purify_1_d(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def v__purify_1_d(
    input_files: list[InputPathType],
    sub_brick: str | None = None,
    suffix: str | None = None,
    runner: Runner | None = None,
) -> VPurify1DOutputs:
    """
    Purifies a series of 1D files for faster I/O into matlab.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/@Purify_1D.html
    
    Args:
        input_files: Input 1D dataset files.
        sub_brick: The sub-brick selection mode to output a select number of\
            columns, following AFNI conventions.
        suffix: STRING is attached to the output prefix which is formed from\
            the input names.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VPurify1DOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__PURIFY_1_D_METADATA)
    cargs = []
    cargs.append("@Purify_1D")
    if sub_brick is not None:
        cargs.extend([
            "-sub",
            sub_brick
        ])
    if suffix is not None:
        cargs.extend([
            "-suf",
            suffix
        ])
    cargs.extend([execution.input_file(f) for f in input_files])
    ret = VPurify1DOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VPurify1DOutputs",
    "V__PURIFY_1_D_METADATA",
    "v__purify_1_d",
]
