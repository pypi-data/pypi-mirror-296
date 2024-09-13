# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_INTRACRANIAL_METADATA = Metadata(
    id="9fa3ac80b0a74be0ff2b130a1522990d5d89a98f.boutiques",
    name="3dIntracranial",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dIntracranialOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_intracranial(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    segmented_image: OutputPathType
    """Output file containing segmented image"""


def v_3d_intracranial(
    infile: InputPathType,
    prefix: str,
    min_val: float | None = None,
    max_val: float | None = None,
    min_conn: float | None = None,
    max_conn: float | None = None,
    no_smooth: bool = False,
    mask: bool = False,
    quiet: bool = False,
    runner: Runner | None = None,
) -> V3dIntracranialOutputs:
    """
    Performs automatic segmentation of intracranial region.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dIntracranial.html
    
    Args:
        infile: Filename of anat dataset to be segmented.
        prefix: Prefix name for file to contain segmented image.
        min_val: Minimum voxel intensity limit. Default is internal PDF\
            estimate for lower bound.
        max_val: Maximum voxel intensity limit. Default is internal PDF\
            estimate for upper bound.
        min_conn: Minimum voxel connectivity to enter. Default is 4.
        max_conn: Maximum voxel connectivity to leave. Default is 2.
        no_smooth: Suppress spatial smoothing of segmentation mask.
        mask: Generate functional image mask (complement). Default is to\
            generate anatomical image.
        quiet: Suppress output to screen.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dIntracranialOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_INTRACRANIAL_METADATA)
    cargs = []
    cargs.append("3dIntracranial")
    cargs.append("-anat")
    cargs.append(execution.input_file(infile))
    cargs.append("-prefix")
    cargs.append(prefix)
    if min_val is not None:
        cargs.extend([
            "-min_val",
            str(min_val)
        ])
    if max_val is not None:
        cargs.extend([
            "-max_val",
            str(max_val)
        ])
    if min_conn is not None:
        cargs.extend([
            "-min_conn",
            str(min_conn)
        ])
    if max_conn is not None:
        cargs.extend([
            "-max_conn",
            str(max_conn)
        ])
    if no_smooth:
        cargs.append("-nosmooth")
    if mask:
        cargs.append("-mask")
    if quiet:
        cargs.append("-quiet")
    ret = V3dIntracranialOutputs(
        root=execution.output_file("."),
        segmented_image=execution.output_file(prefix + "+orig"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dIntracranialOutputs",
    "V_3D_INTRACRANIAL_METADATA",
    "v_3d_intracranial",
]
