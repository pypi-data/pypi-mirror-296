# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_TRFIX_METADATA = Metadata(
    id="92993d180d096fd8c02ca5246a1f6bcc8544e559.boutiques",
    name="3dTRfix",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dTrfixOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_trfix(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_file_head: OutputPathType
    """Output dataset header file"""
    output_file_brik: OutputPathType
    """Output dataset brik file"""


def v_3d_trfix(
    input_file: InputPathType,
    prefix: str,
    tr_list: InputPathType | None = None,
    time_list: InputPathType | None = None,
    output_tr: float | None = None,
    runner: Runner | None = None,
) -> V3dTrfixOutputs:
    """
    Re-sample dataset with irregular time grid to regular time grid via linear
    interpolation.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTRfix.html
    
    Args:
        input_file: Input dataset.
        prefix: Prefix name for output dataset.
        tr_list: File of time gaps between sub-bricks in input dataset.
        time_list: File with times at each sub-brick in the input dataset.
        output_tr: TR value for output dataset (in seconds).
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dTrfixOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_TRFIX_METADATA)
    cargs = []
    cargs.append("3dTRfix")
    cargs.append("-input")
    cargs.extend([
        "-input",
        execution.input_file(input_file)
    ])
    cargs.append("-TRlist")
    if tr_list is not None:
        cargs.extend([
            "-TRlist",
            execution.input_file(tr_list)
        ])
    cargs.append("-TIMElist")
    if time_list is not None:
        cargs.extend([
            "-TIMElist",
            execution.input_file(time_list)
        ])
    cargs.append("-prefix")
    cargs.extend([
        "-prefix",
        prefix
    ])
    cargs.append("-TRout")
    if output_tr is not None:
        cargs.extend([
            "-TRout",
            str(output_tr)
        ])
    ret = V3dTrfixOutputs(
        root=execution.output_file("."),
        output_file_head=execution.output_file(prefix + "+orig.HEAD"),
        output_file_brik=execution.output_file(prefix + "+orig.BRIK"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dTrfixOutputs",
    "V_3D_TRFIX_METADATA",
    "v_3d_trfix",
]
