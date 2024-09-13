# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__ROI_CORR_MAT_METADATA = Metadata(
    id="93306081b2aa4d941532f5a06e179689e35bced4.boutiques",
    name="@ROI_Corr_Mat",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VRoiCorrMatOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__roi_corr_mat(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    matrix_1d: OutputPathType
    """Correlation matrix in .1D format"""
    matrix_brick: OutputPathType
    """Correlation matrix in .BRIK format"""


def v__roi_corr_mat(
    runner: Runner | None = None,
) -> VRoiCorrMatOutputs:
    """
    Script to produce an NxN ROI correlation matrix of N ROIs.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/@ROI_Corr_Mat.html
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VRoiCorrMatOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__ROI_CORR_MAT_METADATA)
    cargs = []
    cargs.append("@ROI_Corr_Mat")
    cargs.append("<-ts")
    cargs.append("TimeSeriesVol>")
    cargs.append("<-roi")
    cargs.append("ROIVol>")
    cargs.append("<-prefix")
    cargs.append("output>")
    cargs.append("[<-roisel")
    cargs.append("ROISEL>]")
    cargs.append("[-zval]")
    cargs.append("[-mat")
    cargs.append("FULL,")
    cargs.append("TRI,")
    cargs.append("TRI_ND]")
    cargs.append("[-verb]")
    cargs.append("[-dirty]")
    ret = VRoiCorrMatOutputs(
        root=execution.output_file("."),
        matrix_1d=execution.output_file("[output]_matrix.1D"),
        matrix_brick=execution.output_file("[output]_matrix.BRIK"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VRoiCorrMatOutputs",
    "V__ROI_CORR_MAT_METADATA",
    "v__roi_corr_mat",
]
