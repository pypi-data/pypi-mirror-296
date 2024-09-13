# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

PNM_EVS_METADATA = Metadata(
    id="415a4b0e63f6c87fa510da1a15528fc5136f88c7.boutiques",
    name="pnm_evs",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class PnmEvsOutputs(typing.NamedTuple):
    """
    Output object returned when calling `pnm_evs(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_file: OutputPathType
    """Output confound/EV matrix file"""


def pnm_evs(
    input_file: InputPathType,
    output_file: str,
    tr_value: float,
    cardiac_file: InputPathType | None = None,
    respiratory_file: InputPathType | None = None,
    order_cardiac: float | None = 2,
    order_respiratory: float | None = 1,
    order_mult_cardiac: float | None = 0,
    order_mult_respiratory: float | None = 0,
    csf_mask: InputPathType | None = None,
    rvt_file: InputPathType | None = None,
    heartrate_file: InputPathType | None = None,
    rvt_smooth: float | None = 0,
    heartrate_smooth: float | None = None,
    slice_direction: str | None = "z",
    slice_order: str | None = None,
    slice_timing_file: InputPathType | None = None,
    debug_flag: bool = False,
    verbose_flag: bool = False,
    help_flag: bool = False,
    runner: Runner | None = None,
) -> PnmEvsOutputs:
    """
    PNM EVs: Generates physiological noise regressors for fMRI data.
    
    Author: University of Oxford (Mark Jenkinson)
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/PNM
    
    Args:
        input_file: Input image filename (4D functional/EPI data).
        output_file: Output filename (for confound/EV matrix).
        tr_value: TR of fMRI volumes (in seconds).
        cardiac_file: Input filename for cardiac values (1 or 2 columns: time\
            [phase]).
        respiratory_file: Input filename for respiratory phase values (1 or 2\
            columns: time [phase]).
        order_cardiac: Order of basic cardiac regressors (number of Fourier\
            pairs).
        order_respiratory: Order of basic respiratory regressors (number of\
            Fourier pairs).
        order_mult_cardiac: Order of multiplicative cardiac terms (also need to\
            set --multr).
        order_mult_respiratory: Order of multiplicative respiratory terms (also\
            need to set --multc).
        csf_mask: Filename of CSF mask image (and generate CSF regressor).
        rvt_file: Input filename of RVT data (2 columns: time value).
        heartrate_file: Input filename for heart rate data (2 columns: time\
            value).
        rvt_smooth: Optional smoothing of RVT regressor (in seconds).
        heartrate_smooth: Optional smoothing of heart rate regressor (in\
            seconds).
        slice_direction: Specify slice direction (x/y/z).
        slice_order: Specify slice ordering\
            (up/down/interleaved_up/interleaved_down).
        slice_timing_file: Specify slice timing via an external file.
        debug_flag: Turn on debugging output.
        verbose_flag: Switch on diagnostic messages.
        help_flag: Display help message.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `PnmEvsOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(PNM_EVS_METADATA)
    cargs = []
    cargs.append("pnm_evs")
    cargs.extend([
        "--in",
        execution.input_file(input_file)
    ])
    cargs.extend([
        "--out",
        output_file
    ])
    cargs.extend([
        "--tr",
        str(tr_value)
    ])
    if cardiac_file is not None:
        cargs.extend([
            "--cardiac",
            execution.input_file(cardiac_file)
        ])
    if respiratory_file is not None:
        cargs.extend([
            "--respiratory",
            execution.input_file(respiratory_file)
        ])
    if order_cardiac is not None:
        cargs.extend([
            "--oc",
            str(order_cardiac)
        ])
    if order_respiratory is not None:
        cargs.extend([
            "--or",
            str(order_respiratory)
        ])
    if order_mult_cardiac is not None:
        cargs.extend([
            "--multc",
            str(order_mult_cardiac)
        ])
    if order_mult_respiratory is not None:
        cargs.extend([
            "--multr",
            str(order_mult_respiratory)
        ])
    if csf_mask is not None:
        cargs.extend([
            "--csfmask",
            execution.input_file(csf_mask)
        ])
    if rvt_file is not None:
        cargs.extend([
            "--rvt",
            execution.input_file(rvt_file)
        ])
    if heartrate_file is not None:
        cargs.extend([
            "--heartrate",
            execution.input_file(heartrate_file)
        ])
    if rvt_smooth is not None:
        cargs.extend([
            "--rvtsmooth",
            str(rvt_smooth)
        ])
    if heartrate_smooth is not None:
        cargs.extend([
            "--heartratesmooth",
            str(heartrate_smooth)
        ])
    if slice_direction is not None:
        cargs.extend([
            "--slicedir",
            slice_direction
        ])
    if slice_order is not None:
        cargs.extend([
            "--sliceorder",
            slice_order
        ])
    if slice_timing_file is not None:
        cargs.extend([
            "--slicetiming",
            execution.input_file(slice_timing_file)
        ])
    if debug_flag:
        cargs.append("--debug")
    if verbose_flag:
        cargs.append("--verbose")
    if help_flag:
        cargs.append("--help")
    ret = PnmEvsOutputs(
        root=execution.output_file("."),
        output_file=execution.output_file(output_file),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "PNM_EVS_METADATA",
    "PnmEvsOutputs",
    "pnm_evs",
]
