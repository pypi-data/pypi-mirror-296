# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__FAST_ROI_METADATA = Metadata(
    id="d82e70f9b79282b8ff3c6e78d4cd767916e2773a.boutiques",
    name="@fast_roi",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VFastRoiOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__fast_roi(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    roi_output: OutputPathType
    """ROI output volume with the specified prefix."""


def v__fast_roi(
    region: list[str],
    anat: InputPathType,
    base: InputPathType,
    roi_grid: InputPathType,
    prefix: str,
    drawn_roi: InputPathType | None = None,
    anat_ns: InputPathType | None = None,
    time_: bool = False,
    twopass: bool = False,
    help_: bool = False,
    runner: Runner | None = None,
) -> VFastRoiOutputs:
    """
    Creates Atlas-based ROI masked in ANAT's original space. The script executes
    rapidly for realtime fMRI applications.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/@fast_roi.html
    
    Args:
        region: Symbolic atlas-based region name. Use repeated instances to\
            specify a mask of numerous regions. Each region is assigned a power of\
            2 integer in the output mask.
        anat: ANAT is the volume to be put in standard space. If ANAT is\
            already in TLRC space, there is no need for -base option.
        base: Name of the reference TLRC volume.
        roi_grid: The volume that defines the final ROI's grid.
        prefix: Prefix used to tag the names the ROIs output.
        drawn_roi: A user drawn ROI in standard (tlrc) space. This ROI gets\
            added with the REGION ROI.
        anat_ns: Same as -anat, but indicates that the skull has been removed\
            already.
        time_: Output elapsed time reports.
        twopass: Make TLRC transformation more robust. Use it if TLRC transform\
            step fails.
        help_: Output help message.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VFastRoiOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__FAST_ROI_METADATA)
    cargs = []
    cargs.append("fast_roi")
    cargs.extend([
        "-region",
        *region
    ])
    if drawn_roi is not None:
        cargs.extend([
            "-drawn_roi",
            execution.input_file(drawn_roi)
        ])
    cargs.extend([
        "-anat",
        execution.input_file(anat)
    ])
    if anat_ns is not None:
        cargs.extend([
            "-anat_ns",
            execution.input_file(anat_ns)
        ])
    cargs.extend([
        "-base",
        execution.input_file(base)
    ])
    cargs.extend([
        "-roi_grid",
        execution.input_file(roi_grid)
    ])
    cargs.extend([
        "-prefix",
        prefix
    ])
    if time_:
        cargs.append("--time")
    if twopass:
        cargs.append("--twopass")
    if help_:
        cargs.append("--help")
    ret = VFastRoiOutputs(
        root=execution.output_file("."),
        roi_output=execution.output_file("ROI." + prefix + "+orig"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VFastRoiOutputs",
    "V__FAST_ROI_METADATA",
    "v__fast_roi",
]
