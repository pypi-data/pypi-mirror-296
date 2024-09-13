# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3DDELAY_METADATA = Metadata(
    id="7507c9110b505056676cecc587845fd4335d9ef8.boutiques",
    name="3ddelay",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3ddelayOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3ddelay(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_brick: OutputPathType | None
    """Primary output results Brick for Delay"""
    output_asc: OutputPathType | None
    """Output ASCII file for results"""
    output_asc_log: OutputPathType | None
    """Log file containing parameter settings and warnings"""
    output_asc_ts: OutputPathType | None
    """Output ASCII file with time series"""


def v_3ddelay(
    input_file: InputPathType,
    reference_file: InputPathType,
    sampling_freq: float,
    stim_period: float,
    prefix: str | None = None,
    polort: float | None = None,
    nodtrnd: bool = False,
    units_seconds: bool = False,
    units_degrees: bool = False,
    units_radians: bool = False,
    phzwrp: bool = False,
    nophzwrp: bool = False,
    phzreverse: bool = False,
    phzscale: float | None = None,
    bias: bool = False,
    nobias: bool = False,
    dsamp: bool = False,
    nodsamp: bool = False,
    mask: InputPathType | None = None,
    nfirst: float | None = None,
    nlast: float | None = None,
    co: float | None = None,
    asc: str | None = None,
    ascts: str | None = None,
    runner: Runner | None = None,
) -> V3ddelayOutputs:
    """
    Estimates the time delay between each voxel time series in a 3D+time dataset and
    a reference time series.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3ddelay.html
    
    Args:
        input_file: Filename of the input 3D+time dataset.
        reference_file: Input ideal time series file name.
        sampling_freq: Sampling frequency in Hz. of data time series (1/TR).
        stim_period: Stimulus period in seconds. Set to 0 if stimulus is not\
            periodic.
        prefix: The prefix for the results Brick.
        polort: Detrend input time series with polynomial of specified order.\
            Default is -1 for auto selection.
        nodtrnd: Remove only the mean (equivalent to polort 0).
        units_seconds: Units for delay estimates in seconds.
        units_degrees: Units for delay estimates in degrees. Requires Tstim > 0.
        units_radians: Units for delay estimates in radians. Requires Tstim > 0.
        phzwrp: Wrap delay (or phase) values.
        nophzwrp: Do not wrap phase (default).
        phzreverse: Reverse phase such that phase -> (T-phase).
        phzscale: Scale phase: phase -> phase*SC (default no scaling).
        bias: Do not correct for the bias in the estimates.
        nobias: Correct for the bias in the estimates (default).
        dsamp: Correct for slice timing differences (default).
        nodsamp: Do not correct for slice timing differences.
        mask: Filename of mask dataset. Only voxels with non-zero values in the\
            mask will be considered.
        nfirst: Number of first dataset image to use in the delay estimate.
        nlast: Number of last dataset image to use in the delay estimate.
        co: Cross Correlation Coefficient threshold value to limit ascii output.
        asc: Write the results to an ascii file for voxels with cross\
            correlation coefficients larger than CCT.
        ascts: Write the results and time series to an ascii file for voxels\
            with cross correlation coefficients larger than CCT.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3ddelayOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3DDELAY_METADATA)
    cargs = []
    cargs.append("3ddelay")
    cargs.append(execution.input_file(input_file))
    cargs.append(execution.input_file(reference_file))
    cargs.extend([
        "-fs",
        str(sampling_freq)
    ])
    cargs.extend([
        "-T",
        str(stim_period)
    ])
    if prefix is not None:
        cargs.extend([
            "-prefix",
            prefix
        ])
    if polort is not None:
        cargs.extend([
            "-polort",
            str(polort)
        ])
    if nodtrnd:
        cargs.append("-nodtrnd")
    if units_seconds:
        cargs.append("-uS")
    if units_degrees:
        cargs.append("-uD")
    if units_radians:
        cargs.append("-uR")
    if phzwrp:
        cargs.append("-phzwrp")
    if nophzwrp:
        cargs.append("-nophzwrp")
    if phzreverse:
        cargs.append("-phzreverse")
    if phzscale is not None:
        cargs.extend([
            "-phzscale",
            str(phzscale)
        ])
    if bias:
        cargs.append("-bias")
    if nobias:
        cargs.append("-nobias")
    if dsamp:
        cargs.append("-dsamp")
    if nodsamp:
        cargs.append("-nodsamp")
    if mask is not None:
        cargs.extend([
            "-mask",
            execution.input_file(mask)
        ])
    if nfirst is not None:
        cargs.extend([
            "-nfirst",
            str(nfirst)
        ])
    if nlast is not None:
        cargs.extend([
            "-nlast",
            str(nlast)
        ])
    if co is not None:
        cargs.extend([
            "-co",
            str(co)
        ])
    if asc is not None:
        cargs.extend([
            "-asc",
            asc
        ])
    if ascts is not None:
        cargs.extend([
            "-ascts",
            ascts
        ])
    ret = V3ddelayOutputs(
        root=execution.output_file("."),
        output_brick=execution.output_file(prefix + ".DEL+orig.BRIK") if (prefix is not None) else None,
        output_asc=execution.output_file(prefix + ".ASC") if (prefix is not None) else None,
        output_asc_log=execution.output_file(prefix + ".ASC.log") if (prefix is not None) else None,
        output_asc_ts=execution.output_file(prefix + ".ASC.ts") if (prefix is not None) else None,
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3ddelayOutputs",
    "V_3DDELAY_METADATA",
    "v_3ddelay",
]
