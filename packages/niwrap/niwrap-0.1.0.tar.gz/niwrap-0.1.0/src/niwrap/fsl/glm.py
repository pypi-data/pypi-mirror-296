# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

GLM_METADATA = Metadata(
    id="cc6bf673df5819d6a362ac568217c6f4e0faf99a.boutiques",
    name="glm",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class GlmOutputs(typing.NamedTuple):
    """
    Output object returned when calling `glm(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    out_file: OutputPathType
    """Filename for glm parameter estimates (glm betas)."""
    out_cope_outfile: OutputPathType | None
    """Output file name for copes (either as text file or image)."""
    out_data: OutputPathType
    """Output file for preprocessed data."""
    out_f: OutputPathType
    """Output file name for f-value of full model fit."""
    out_file_: OutputPathType
    """File name of glm parameters (if generated)."""
    out_p: OutputPathType
    """Output file name for p-values of z-stats (either as text file or
    image)."""
    out_pf: OutputPathType
    """Output file name for p-value for full model fit."""
    out_res: OutputPathType
    """Output file name for residuals."""
    out_sigsq: OutputPathType
    """Output file name for residual noise variance sigma-square."""
    out_t: OutputPathType
    """Output file name for t-stats (either as text file or image)."""
    out_varcb: OutputPathType
    """Output file name for variance of copes."""
    out_vnscales: OutputPathType
    """Output file name for scaling factors for variance normalisation."""
    out_z: OutputPathType
    """Output file name for copes (either as text file or image)."""


def glm(
    in_file: InputPathType,
    design: InputPathType,
    contrasts: InputPathType | None = None,
    dat_norm: bool = False,
    demean: bool = False,
    des_norm: bool = False,
    dof: int | None = None,
    mask: InputPathType | None = None,
    out_cope: InputPathType | None = None,
    out_data_name: InputPathType | None = None,
    out_f_name: InputPathType | None = None,
    out_p_name: InputPathType | None = None,
    out_pf_name: InputPathType | None = None,
    out_res_name: InputPathType | None = None,
    out_sigsq_name: InputPathType | None = None,
    out_t_name: InputPathType | None = None,
    out_varcb_name: InputPathType | None = None,
    out_vnscales_name: InputPathType | None = None,
    out_z_name: InputPathType | None = None,
    output_type: typing.Literal["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"] | None = None,
    var_norm: bool = False,
    runner: Runner | None = None,
) -> GlmOutputs:
    """
    FSL GLM.
    
    Author: Nipype (interface)
    
    Args:
        in_file: Input file name (text matrix or 3d/4d image file).
        design: File name of the glm design matrix (text time courses for\
            temporal regression or an image file for spatial regression).
        contrasts: Matrix of t-statics contrasts.
        dat_norm: Switch on normalization of the data time series to unit std\
            deviation.
        demean: Switch on demeaining of design and data.
        des_norm: Switch on normalization of the design matrix columns to unit\
            std deviation.
        dof: Set degrees of freedom explicitly.
        mask: Mask image file name if input is image.
        out_cope: Output file name for cope (either as txt or image.
        out_data_name: Output file name for pre-processed data.
        out_f_name: Output file name for f-value of full model fit.
        out_p_name: Output file name for p-values of z-stats (either as text\
            file or image).
        out_pf_name: Output file name for p-value for full model fit.
        out_res_name: Output file name for residuals.
        out_sigsq_name: Output file name for residual noise variance\
            sigma-square.
        out_t_name: Output file name for t-stats (either as txt or image.
        out_varcb_name: Output file name for variance of copes.
        out_vnscales_name: Output file name for scaling factors for variance\
            normalisation.
        out_z_name: Output file name for z-stats (either as txt or image.
        output_type: 'nifti' or 'nifti_pair' or 'nifti_gz' or 'nifti_pair_gz'.\
            Fsl output type.
        var_norm: Perform melodic variance-normalisation on data.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `GlmOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(GLM_METADATA)
    cargs = []
    cargs.append("GLM")
    cargs.extend([
        "-i",
        execution.input_file(in_file)
    ])
    cargs.extend([
        "-d",
        execution.input_file(design)
    ])
    cargs.append("[OUT_FILE]")
    if contrasts is not None:
        cargs.extend([
            "-c",
            execution.input_file(contrasts)
        ])
    if dat_norm:
        cargs.append("--dat_norm")
    if demean:
        cargs.append("--demean")
    if des_norm:
        cargs.append("--des_norm")
    if dof is not None:
        cargs.append("--dof=" + str(dof))
    if mask is not None:
        cargs.extend([
            "-m",
            execution.input_file(mask)
        ])
    if out_cope is not None:
        cargs.append("--out_cope=" + execution.input_file(out_cope))
    if out_data_name is not None:
        cargs.append("--out_data=" + execution.input_file(out_data_name))
    if out_f_name is not None:
        cargs.append("--out_f=" + execution.input_file(out_f_name))
    if out_p_name is not None:
        cargs.append("--out_p=" + execution.input_file(out_p_name))
    if out_pf_name is not None:
        cargs.append("--out_pf=" + execution.input_file(out_pf_name))
    if out_res_name is not None:
        cargs.append("--out_res=" + execution.input_file(out_res_name))
    if out_sigsq_name is not None:
        cargs.append("--out_sigsq=" + execution.input_file(out_sigsq_name))
    if out_t_name is not None:
        cargs.append("--out_t=" + execution.input_file(out_t_name))
    if out_varcb_name is not None:
        cargs.append("--out_varcb=" + execution.input_file(out_varcb_name))
    if out_vnscales_name is not None:
        cargs.append("--out_vnscales=" + execution.input_file(out_vnscales_name))
    if out_z_name is not None:
        cargs.append("--out_z=" + execution.input_file(out_z_name))
    if output_type is not None:
        cargs.append(output_type)
    if var_norm:
        cargs.append("--vn")
    ret = GlmOutputs(
        root=execution.output_file("."),
        out_file=execution.output_file(pathlib.Path(in_file).name + "_glm"),
        out_cope_outfile=execution.output_file(pathlib.Path(out_cope).name) if (out_cope is not None) else None,
        out_data=execution.output_file("out_data"),
        out_f=execution.output_file("out_f"),
        out_file_=execution.output_file("out_file"),
        out_p=execution.output_file("out_p"),
        out_pf=execution.output_file("out_pf"),
        out_res=execution.output_file("out_res"),
        out_sigsq=execution.output_file("out_sigsq"),
        out_t=execution.output_file("out_t"),
        out_varcb=execution.output_file("out_varcb"),
        out_vnscales=execution.output_file("out_vnscales"),
        out_z=execution.output_file("out_z"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "GLM_METADATA",
    "GlmOutputs",
    "glm",
]
