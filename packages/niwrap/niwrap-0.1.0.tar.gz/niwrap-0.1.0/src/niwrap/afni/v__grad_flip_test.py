# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__GRAD_FLIP_TEST_METADATA = Metadata(
    id="9d0fc0de1e554a35c574767a25f1d88ddcf067e2.boutiques",
    name="@GradFlipTest",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VGradFlipTestOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__grad_flip_test(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_file: OutputPathType | None
    """Text file that stores recommended flip option"""
    temp_directory: OutputPathType
    """Temporary working directory to store intermediate files"""


def v__grad_flip_test(
    dwi: InputPathType,
    grad_col_mat_t: InputPathType | None = None,
    grad_col_mat_t_: InputPathType | None = None,
    grad_col_mat_t_2: InputPathType | None = None,
    grad_col_mat_t_3: InputPathType | None = None,
    mask: InputPathType | None = None,
    bvals: InputPathType | None = None,
    thresh_fa: float | None = None,
    thresh_len: float | None = None,
    prefix: str | None = None,
    check_abs_min: float | None = None,
    scale_out_1000: bool = False,
    wdir: str | None = None,
    do_clean: bool = False,
    runner: Runner | None = None,
) -> VGradFlipTestOutputs:
    """
    Script to test the correct flip for a data set when using 1dDW_Grad_o_Mat++.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/@GradFlipTest.html
    
    Args:
        dwi: Set of DWIs (N total volumes).
        grad_col_mat_t: Set of column-wise g- or b-matrix elements\
            ("TORTOISE"-style format, "row-first").
        grad_col_mat_t_: Set of column-wise g- or b-matrix elements\
            ("TORTOISE"-style format, "row-first").
        grad_col_mat_t_2: Set of column-wise g- or b-matrix elements\
            ("TORTOISE"-style format, "row-first").
        grad_col_mat_t_3: Set of column-wise g- or b-matrix elements\
            ("TORTOISE"-style format, "row-first").
        mask: Optional mask (probably whole brain); otherwise, automasking is\
            performed.
        bvals: Can input bvals, if necessary (but shouldn't be necessary?).
        thresh_fa: Set minimum FA value for tracking (default X=0.2).
        thresh_len: Set minimum tract length to keep a tract when propagating\
            (default L=30mm).
        prefix: Output name of text file that stores recommended flip option.
        check_abs_min: Handle tiny negative values in gradient vectors.
        scale_out_1000: Scale output to 1000, as in 3dDWItoDT (probably not\
            necessary).
        wdir: Rename working directory output; useful if running multiple\
            iterations.
        do_clean: Remove temporary directory.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VGradFlipTestOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__GRAD_FLIP_TEST_METADATA)
    cargs = []
    cargs.append("@GradFlipTest")
    cargs.extend([
        "-in_dwi",
        execution.input_file(dwi)
    ])
    if grad_col_mat_t is not None:
        cargs.extend([
            "-in_col_matT",
            execution.input_file(grad_col_mat_t)
        ])
    if grad_col_mat_t_ is not None:
        cargs.extend([
            "-in_col_matT",
            execution.input_file(grad_col_mat_t_)
        ])
    if grad_col_mat_t_2 is not None:
        cargs.extend([
            "-in_col_matT",
            execution.input_file(grad_col_mat_t_2)
        ])
    if grad_col_mat_t_3 is not None:
        cargs.extend([
            "-in_col_matT",
            execution.input_file(grad_col_mat_t_3)
        ])
    if mask is not None:
        cargs.extend([
            "-mask",
            execution.input_file(mask)
        ])
    if bvals is not None:
        cargs.extend([
            "-in_bvals",
            execution.input_file(bvals)
        ])
    if thresh_fa is not None:
        cargs.extend([
            "-alg_Thresh_FA",
            str(thresh_fa)
        ])
    if thresh_len is not None:
        cargs.extend([
            "-alg_Thresh_Len",
            str(thresh_len)
        ])
    if prefix is not None:
        cargs.extend([
            "-prefix",
            prefix
        ])
    if check_abs_min is not None:
        cargs.extend([
            "-check_abs_min",
            str(check_abs_min)
        ])
    if scale_out_1000:
        cargs.append("-scale_out_1000")
    if wdir is not None:
        cargs.extend([
            "-wdir",
            wdir
        ])
    if do_clean:
        cargs.append("-do_clean")
    ret = VGradFlipTestOutputs(
        root=execution.output_file("."),
        output_file=execution.output_file(prefix + ".txt") if (prefix is not None) else None,
        temp_directory=execution.output_file("_tmp_TESTFLIP"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VGradFlipTestOutputs",
    "V__GRAD_FLIP_TEST_METADATA",
    "v__grad_flip_test",
]
