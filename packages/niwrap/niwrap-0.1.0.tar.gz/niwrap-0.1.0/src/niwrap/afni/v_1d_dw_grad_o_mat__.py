# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_1D_DW_GRAD_O_MAT___METADATA = Metadata(
    id="1b134b48311299bc6a0c83db7d4184e0a750ef98.boutiques",
    name="1dDW_Grad_o_Mat++",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V1dDwGradOMatOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_1d_dw_grad_o_mat__(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    outfile: OutputPathType
    """Output file of gradients or matrices"""
    out_row_bval_file: OutputPathType
    """Output b-values file in a single row"""
    out_col_bval_file: OutputPathType
    """Output b-values file in a single column"""


def v_1d_dw_grad_o_mat__(
    no_flip: bool = False,
    runner: Runner | None = None,
) -> V1dDwGradOMatOutputs:
    """
    Manipulation of diffusion-weighted (DW) gradient vector files, b-value files,
    and b- or g-matrices with various input and output configurations.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/1dDW_Grad_o_Mat++.html
    
    Args:
        no_flip: Don't change any gradient/matrix signs (default behavior).
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V1dDwGradOMatOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_1D_DW_GRAD_O_MAT___METADATA)
    cargs = []
    cargs.append("1dDW_Grad_o_Mat++")
    cargs.append("[INPUT_OPTION]")
    cargs.append("INFILE")
    if no_flip:
        cargs.append("-no_flip")
    cargs.append("[OUTPUT_OPTION]")
    cargs.append("OUTFILE")
    cargs.append("[ADDITIONAL_OPTIONS]")
    ret = V1dDwGradOMatOutputs(
        root=execution.output_file("."),
        outfile=execution.output_file("[OUTFILE]"),
        out_row_bval_file=execution.output_file("[BB]"),
        out_col_bval_file=execution.output_file("[BB]"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V1dDwGradOMatOutputs",
    "V_1D_DW_GRAD_O_MAT___METADATA",
    "v_1d_dw_grad_o_mat__",
]
