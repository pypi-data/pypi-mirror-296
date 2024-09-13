# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

FILMBABE_METADATA = Metadata(
    id="5aeaa63a2b4af0df1c495362f58a31832031b867.boutiques",
    name="filmbabe",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class FilmbabeOutputs(typing.NamedTuple):
    """
    Output object returned when calling `filmbabe(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_dir: OutputPathType
    """Output directory"""


def filmbabe(
    datafile_alias: InputPathType,
    mask_alias: InputPathType,
    designfile_alias_2: InputPathType,
    frf: InputPathType,
    verbose_flag_alias: bool = False,
    debug_level_alias_2: str | None = None,
    timing_on_flag: bool = False,
    help_flag_alias: bool = False,
    flobs_prior_off_alias: bool = False,
    flobs_dir: str | None = None,
    prior_covar_file_alias: InputPathType | None = None,
    prior_mean_file_alias: InputPathType | None = None,
    log_dir_alias_2: str | None = None,
    num_iterations: int | None = 5,
    temporal_ar_mrf_prec_alias: float | None = -1,
    temporal_ar_flag: bool = False,
    num_trace_samples_alias: int | None = 0,
    temporal_ar_order: int | None = 3,
    runner: Runner | None = None,
) -> FilmbabeOutputs:
    """
    FILM with MCMC-based Bayesian Analysis for fMRI.
    
    Author: FMRIB Analysis Group, Oxford University, UK
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/
    
    Args:
        datafile_alias: Data file.
        mask_alias: Mask file.
        designfile_alias_2: Design matrix file.
        frf: File indicating which regressors belong to which original EV\
            design matrix file (a -1 label indicates a non-flobs regressor).
        verbose_flag_alias: Switch on diagnostic messages.
        debug_level_alias_2: Set debug level.
        timing_on_flag: Turn timing on.
        help_flag_alias: Display help message.
        flobs_prior_off_alias: Turn FLOBS prior off.
        flobs_dir: FLOBS directory; required when using FLOBS constraints.
        prior_covar_file_alias: Prior covariance matrix file.
        prior_mean_file_alias: Prior mean matrix file.
        log_dir_alias_2: Log directory.
        num_iterations: Number of VB iterations; default is 5.
        temporal_ar_mrf_prec_alias: MRF precision to impose on temporal AR\
            maps, default is -1 for a proper full Bayes approach.
        temporal_ar_flag: Impose ARD/MRF on temporal AR.
        num_trace_samples_alias: Number of samples to take to estimate trace;\
            default is 0 (uses only diagonal elements of precision matrix to\
            estimate trace).
        temporal_ar_order: Order of temporal AR; default is 3.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `FilmbabeOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(FILMBABE_METADATA)
    cargs = []
    cargs.append("filmbabe")
    cargs.extend([
        "--datafile",
        execution.input_file(datafile_alias)
    ])
    cargs.extend([
        "--mask",
        execution.input_file(mask_alias)
    ])
    cargs.extend([
        "--designfile",
        execution.input_file(designfile_alias_2)
    ])
    cargs.extend([
        "--frf",
        execution.input_file(frf)
    ])
    if verbose_flag_alias:
        cargs.append("--verbose")
    if debug_level_alias_2 is not None:
        cargs.extend([
            "--debuglevel",
            debug_level_alias_2
        ])
    if timing_on_flag:
        cargs.append("--to")
    if help_flag_alias:
        cargs.append("--help")
    if flobs_prior_off_alias:
        cargs.append("--flobsprioroff")
    if flobs_dir is not None:
        cargs.extend([
            "--fd",
            flobs_dir
        ])
    if prior_covar_file_alias is not None:
        cargs.extend([
            "--priorcovarfile",
            execution.input_file(prior_covar_file_alias)
        ])
    if prior_mean_file_alias is not None:
        cargs.extend([
            "--priormeanfile",
            execution.input_file(prior_mean_file_alias)
        ])
    if log_dir_alias_2 is not None:
        cargs.extend([
            "--logdir",
            log_dir_alias_2
        ])
    if num_iterations is not None:
        cargs.extend([
            "--ni",
            str(num_iterations)
        ])
    if temporal_ar_mrf_prec_alias is not None:
        cargs.extend([
            "--tarmrfprec",
            str(temporal_ar_mrf_prec_alias)
        ])
    if temporal_ar_flag:
        cargs.append("--tarard")
    if num_trace_samples_alias is not None:
        cargs.extend([
            "--ntracesamps",
            str(num_trace_samples_alias)
        ])
    if temporal_ar_order is not None:
        cargs.extend([
            "--ntar",
            str(temporal_ar_order)
        ])
    ret = FilmbabeOutputs(
        root=execution.output_file("."),
        output_dir=execution.output_file("output"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "FILMBABE_METADATA",
    "FilmbabeOutputs",
    "filmbabe",
]
