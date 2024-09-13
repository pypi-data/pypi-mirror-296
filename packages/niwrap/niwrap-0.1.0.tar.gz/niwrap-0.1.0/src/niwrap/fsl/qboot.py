# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

QBOOT_METADATA = Metadata(
    id="719956ac6e06444e87fb8bebc3ba3438af528fd3.boutiques",
    name="qboot",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class QbootOutputs(typing.NamedTuple):
    """
    Output object returned when calling `qboot(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_files: OutputPathType
    """Output files saved in the specified log directory"""


def qboot(
    data_file: InputPathType,
    mask_file: InputPathType,
    bvecs_file: InputPathType,
    bvals_file: InputPathType,
    log_dir: str | None = None,
    forcedir_flag: bool = False,
    q_file: InputPathType | None = None,
    model_type: int | None = None,
    lmax_order: int | None = None,
    npeaks: int | None = None,
    threshold: float | None = None,
    num_samples: int | None = None,
    lambda_param: float | None = None,
    delta_param: float | None = None,
    alpha_param: float | None = None,
    seed_param: int | None = None,
    gfa_flag: bool = False,
    savecoeff_flag: bool = False,
    savemeancoeff_flag: bool = False,
    verbose_flag: bool = False,
    help_flag: bool = False,
    runner: Runner | None = None,
) -> QbootOutputs:
    """
    Tool for computing q-ball ODFs using bootstrap samples.
    
    Author: Oxford Centre for Functional MRI of the Brain (FMRIB)
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/
    
    Args:
        data_file: Data file.
        mask_file: Mask file.
        bvecs_file: b vectors file.
        bvals_file: b values file.
        log_dir: Output directory (default is logdir).
        forcedir_flag: Use the actual directory name given - i.e. don't add +\
            to make a new directory.
        q_file: File provided with multi-shell data. Indicates the number of\
            directions for each shell.
        model_type: Which model to use. 1=Tuch's ODFs, 2=CSA ODFs (default),\
            3=multi-shell CSA ODFs.
        lmax_order: Maximum spherical harmonic order employed (must be even,\
            default=4).
        npeaks: Maximum number of ODF peaks to be detected (default 2).
        threshold: Minimum threshold for a local maxima to be considered an ODF\
            peak. Expressed as a fraction of the maximum ODF value (default 0.4).
        num_samples: Number of bootstrap samples (default is 50).
        lambda_param: Laplace-Beltrami regularization parameter (default is 0).
        delta_param: Signal attenuation regularization parameter for models=2,3\
            (default is 0.01).
        alpha_param: Laplacian sharpening parameter for model=1 (default is 0,\
            should be smaller than 1).
        seed_param: Seed for pseudo-random number generator.
        gfa_flag: Compute a generalised FA, using the mean ODF in each voxel.
        savecoeff_flag: Save the ODF coefficients instead of the peaks.\
            WARNING: These can be huge files, please use a few bootstrap samples\
            and a low lmax!.
        savemeancoeff_flag: Save the mean ODF coefficients across all samples.
        verbose_flag: Switch on diagnostic messages.
        help_flag: Display this help message.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `QbootOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(QBOOT_METADATA)
    cargs = []
    cargs.append("qboot")
    cargs.extend([
        "-k",
        execution.input_file(data_file)
    ])
    cargs.extend([
        "-m",
        execution.input_file(mask_file)
    ])
    cargs.extend([
        "-r",
        execution.input_file(bvecs_file)
    ])
    cargs.extend([
        "-b",
        execution.input_file(bvals_file)
    ])
    if log_dir is not None:
        cargs.extend([
            "--ld",
            log_dir
        ])
    if forcedir_flag:
        cargs.append("--forcedir")
    if q_file is not None:
        cargs.extend([
            "--q",
            execution.input_file(q_file)
        ])
    if model_type is not None:
        cargs.extend([
            "--model",
            str(model_type)
        ])
    if lmax_order is not None:
        cargs.extend([
            "--lmax",
            str(lmax_order)
        ])
    if npeaks is not None:
        cargs.extend([
            "--npeaks",
            str(npeaks)
        ])
    if threshold is not None:
        cargs.extend([
            "--thr",
            str(threshold)
        ])
    if num_samples is not None:
        cargs.extend([
            "--ns",
            str(num_samples)
        ])
    if lambda_param is not None:
        cargs.extend([
            "--lambda",
            str(lambda_param)
        ])
    if delta_param is not None:
        cargs.extend([
            "--delta",
            str(delta_param)
        ])
    if alpha_param is not None:
        cargs.extend([
            "--alpha",
            str(alpha_param)
        ])
    if seed_param is not None:
        cargs.extend([
            "--seed",
            str(seed_param)
        ])
    if gfa_flag:
        cargs.append("--gfa")
    if savecoeff_flag:
        cargs.append("--savecoeff")
    if savemeancoeff_flag:
        cargs.append("--savemeancoeff")
    if verbose_flag:
        cargs.append("-V")
    if help_flag:
        cargs.append("-h")
    ret = QbootOutputs(
        root=execution.output_file("."),
        output_files=execution.output_file("logdir/*"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "QBOOT_METADATA",
    "QbootOutputs",
    "qboot",
]
