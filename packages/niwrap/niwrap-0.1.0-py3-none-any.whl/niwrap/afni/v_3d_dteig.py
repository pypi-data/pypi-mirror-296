# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_DTEIG_METADATA = Metadata(
    id="9bdc110c1aa425f5867b362872318f6ae6a347db.boutiques",
    name="3dDTeig",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dDteigOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_dteig(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_dataset: OutputPathType
    """Output dataset with computed eigenvalues, eigenvectors, FA, and MD"""
    output_lambda: OutputPathType
    """Output dataset for eigenvalues"""
    output_eigvec: OutputPathType
    """Output dataset for eigenvectors"""
    output_fa: OutputPathType
    """Output dataset for fractional anisotropy"""
    output_md: OutputPathType
    """Output dataset for mean diffusivity"""


def v_3d_dteig(
    input_dataset: str,
    runner: Runner | None = None,
) -> V3dDteigOutputs:
    """
    Computes eigenvalues and eigenvectors for an input dataset of tensors.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dDTeig.html
    
    Args:
        input_dataset: Input dataset of Dxx, Dxy, Dyy, Dxz, Dyz, Dzz sub-bricks.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dDteigOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_DTEIG_METADATA)
    cargs = []
    cargs.append("3dDTeig")
    cargs.append("[OPTIONS]")
    cargs.append(input_dataset)
    ret = V3dDteigOutputs(
        root=execution.output_file("."),
        output_dataset=execution.output_file("[PREFIX].nii.gz"),
        output_lambda=execution.output_file("[PREFIX]_lambda.nii.gz"),
        output_eigvec=execution.output_file("[PREFIX]_eigvec.nii.gz"),
        output_fa=execution.output_file("[PREFIX]_FA.nii.gz"),
        output_md=execution.output_file("[PREFIX]_MD.nii.gz"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dDteigOutputs",
    "V_3D_DTEIG_METADATA",
    "v_3d_dteig",
]
