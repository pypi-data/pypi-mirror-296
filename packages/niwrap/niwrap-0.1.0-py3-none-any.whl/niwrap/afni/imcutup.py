# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

IMCUTUP_METADATA = Metadata(
    id="ae7436cecf52feb92be9f38fea9b36005b397005.boutiques",
    name="imcutup",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class ImcutupOutputs(typing.NamedTuple):
    """
    Output object returned when calling `imcutup(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_files: OutputPathType | None
    """Output smaller images with the specified prefix numbering format."""


def imcutup(
    nx: int,
    ny: int,
    input_file: InputPathType,
    prefix: str | None = None,
    xynum: bool = False,
    yxnum: bool = False,
    xynum_format: bool = False,
    yxnum_format: bool = False,
    runner: Runner | None = None,
) -> ImcutupOutputs:
    """
    Breaks up larger images into smaller image files of user-defined size.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/imcutup.html
    
    Args:
        nx: Number of pixels along the x-dimension for the smaller images.
        ny: Number of pixels along the y-dimension for the smaller images.
        input_file: Input image filename. Must be a single 2D image.
        prefix: Prefix the output files with the provided string.
        xynum: Number the output images in x-first, then y (default behavior).
        yxnum: Number the output images in y-first, then x.
        xynum_format: 2D numbering in x.y format.
        yxnum_format: 2D numbering in y.x format.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `ImcutupOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(IMCUTUP_METADATA)
    cargs = []
    cargs.append("imcutup")
    if prefix is not None:
        cargs.extend([
            "-prefix",
            prefix
        ])
    if xynum:
        cargs.append("-xynum")
    if yxnum:
        cargs.append("-yxnum")
    if xynum_format:
        cargs.append("-x.ynum")
    if yxnum_format:
        cargs.append("-y.xnum")
    cargs.append(str(nx))
    cargs.append(str(ny))
    cargs.append(execution.input_file(input_file))
    ret = ImcutupOutputs(
        root=execution.output_file("."),
        output_files=execution.output_file(prefix + "*") if (prefix is not None) else None,
    )
    execution.run(cargs)
    return ret


__all__ = [
    "IMCUTUP_METADATA",
    "ImcutupOutputs",
    "imcutup",
]
