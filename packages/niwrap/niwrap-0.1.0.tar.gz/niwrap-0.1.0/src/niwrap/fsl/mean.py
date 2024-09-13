# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

MEAN_METADATA = Metadata(
    id="1424870e91d19288bcbeea39891f90d34a006af4.boutiques",
    name="mean",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class MeanOutputs(typing.NamedTuple):
    """
    Output object returned when calling `mean(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_log: OutputPathType
    """Output log of mean computation"""


def mean(
    datafile: InputPathType,
    maskfile: InputPathType,
    verbose_flag: bool = False,
    debug_level: float | None = None,
    timing_flag: bool = False,
    log_dir: str | None = None,
    forcedir_flag: bool = False,
    inference_tech: str | None = None,
    num_jumps: float | None = None,
    num_burnin: float | None = None,
    num_sample_every: float | None = None,
    num_update_proposalevery: float | None = None,
    acceptance_rate: float | None = None,
    seed: float | None = None,
    error_precision: float | None = None,
    noamp_flag: bool = False,
    prior_mean: float | None = None,
    prior_std: float | None = None,
    runner: Runner | None = None,
) -> MeanOutputs:
    """
    Diagnostic tool for analyzing and computing mean values for FSL data.
    
    Author: Oxford Centre for Functional MRI of the Brain (FMRIB)
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/
    
    Args:
        datafile: Regressor data file.
        maskfile: Mask file.
        verbose_flag: Switch on diagnostic messages.
        debug_level: Set debug level.
        timing_flag: Turn timing on.
        log_dir: Log directory (default is logdir).
        forcedir_flag: Use the actual directory name given - i.e. don't add +\
            to make a new directory.
        inference_tech: Inference technique: mcmc or laplace (default is mcmc).
        num_jumps: Number of jumps to be made by MCMC (default is 5000).
        num_burnin: Number of jumps at start of MCMC to be discarded (default\
            is 500).
        num_sample_every: Number of jumps for each sample (MCMC) (default is 1).
        num_update_proposalevery: Number of jumps for each update to the\
            proposal density std (MCMC) (default is 40).
        acceptance_rate: Acceptance rate to aim for (MCMC) (default is 0.6).
        seed: Seed for pseudo random number generator.
        error_precision: Value to fix error precision to (default is -1, which\
            means error precision is not fixed).
        noamp_flag: Turn off Analytical Marginalisation of error Precision.
        prior_mean: Prior mean.
        prior_std: Prior standard deviation.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `MeanOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(MEAN_METADATA)
    cargs = []
    cargs.append("mean")
    cargs.extend([
        "--data",
        execution.input_file(datafile)
    ])
    cargs.extend([
        "--mask",
        execution.input_file(maskfile)
    ])
    if verbose_flag:
        cargs.append("--verbose")
    if debug_level is not None:
        cargs.extend([
            "--debug",
            str(debug_level)
        ])
    if timing_flag:
        cargs.append("--to")
    if log_dir is not None:
        cargs.extend([
            "--ld",
            log_dir
        ])
    if forcedir_flag:
        cargs.append("--forcedir")
    if inference_tech is not None:
        cargs.extend([
            "--inf",
            inference_tech
        ])
    if num_jumps is not None:
        cargs.extend([
            "--nj",
            str(num_jumps)
        ])
    if num_burnin is not None:
        cargs.extend([
            "--bi",
            str(num_burnin)
        ])
    if num_sample_every is not None:
        cargs.extend([
            "--se",
            str(num_sample_every)
        ])
    if num_update_proposalevery is not None:
        cargs.extend([
            "--upe",
            str(num_update_proposalevery)
        ])
    if acceptance_rate is not None:
        cargs.extend([
            "--arate",
            str(acceptance_rate)
        ])
    if seed is not None:
        cargs.extend([
            "--seed",
            str(seed)
        ])
    if error_precision is not None:
        cargs.extend([
            "--prec",
            str(error_precision)
        ])
    if noamp_flag:
        cargs.append("--noamp")
    if prior_mean is not None:
        cargs.extend([
            "--pm",
            str(prior_mean)
        ])
    if prior_std is not None:
        cargs.extend([
            "--ps",
            str(prior_std)
        ])
    ret = MeanOutputs(
        root=execution.output_file("."),
        output_log=execution.output_file("logdir/mean_output.txt"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "MEAN_METADATA",
    "MeanOutputs",
    "mean",
]
