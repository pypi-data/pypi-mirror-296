# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_LOCAL_BISTAT_METADATA = Metadata(
    id="b85d3da1398fef0f6b5bbd999047bab426018b83.boutiques",
    name="3dLocalBistat",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dLocalBistatOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_local_bistat(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_head: OutputPathType
    """Output dataset header for AFNI format"""
    output_brik: OutputPathType
    """Output dataset BRIK for AFNI format"""


def v_3d_local_bistat(
    nbhd: str,
    stats: list[str],
    prefix: str,
    dataset1: InputPathType,
    dataset2: InputPathType,
    mask: InputPathType | None = None,
    automask: bool = False,
    weight: InputPathType | None = None,
    histpow: float | None = None,
    histbin: float | None = None,
    hclip1: list[str] | None = None,
    hclip2: list[str] | None = None,
    runner: Runner | None = None,
) -> V3dLocalBistatOutputs:
    """
    Compute statistics between 2 datasets at each voxel based on a local
    neighborhood.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dLocalBistat.html
    
    Args:
        nbhd: Specifies the neighborhood around each voxel for statistics\
            calculation. Types include: SPHERE(r), RECT(a,b,c), RHDD(r), TOHD(r).
        stats: Statistic to compute in the region around each voxel. Multiple\
            options allowed. Includes: pearson, spearman, quadrant, mutinfo,\
            normuti, jointent, hellinger, crU, crM, crA, L2slope, L1slope, num,\
            ALL.
        prefix: Prefix of the output dataset.
        dataset1: The first input dataset (e.g. data1.nii).
        dataset2: The second input dataset (e.g. data2.nii).
        mask: Read in a dataset to use as a mask. Non-zero voxels define the\
            mask region.
        automask: Compute the mask as in program 3dAutomask. Mutually exclusive\
            with -mask.
        weight: Use dataset as a weight (applies to pearson).
        histpow: Sets the exponent for the number of bins in the histogram used\
            for Hellinger, Mutual Information, and Correlation Ratio statistics.
        histbin: Sets the number of bins directly in the histogram used for\
            Hellinger, Mutual Information, and Correlation Ratio statistics.
        hclip1: Clip dataset1 to lie between specified values.
        hclip2: Clip dataset2 to lie between specified values.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dLocalBistatOutputs`).
    """
    if hclip1 is not None and (len(hclip1) != 2): 
        raise ValueError(f"Length of 'hclip1' must be 2 but was {len(hclip1)}")
    if hclip2 is not None and (len(hclip2) != 2): 
        raise ValueError(f"Length of 'hclip2' must be 2 but was {len(hclip2)}")
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_LOCAL_BISTAT_METADATA)
    cargs = []
    cargs.append("3dLocalBistat")
    cargs.extend([
        "-nbhd",
        nbhd
    ])
    cargs.extend([
        "-stat",
        *stats
    ])
    if mask is not None:
        cargs.extend([
            "-mask",
            execution.input_file(mask)
        ])
    if automask:
        cargs.append("-automask")
    if weight is not None:
        cargs.extend([
            "-weight",
            execution.input_file(weight)
        ])
    cargs.extend([
        "-prefix",
        prefix
    ])
    if histpow is not None:
        cargs.extend([
            "-histpow",
            str(histpow)
        ])
    if histbin is not None:
        cargs.extend([
            "-histbin",
            str(histbin)
        ])
    if hclip1 is not None:
        cargs.extend([
            "-hclip1",
            *hclip1
        ])
    if hclip2 is not None:
        cargs.extend([
            "-hclip2",
            *hclip2
        ])
    cargs.append(execution.input_file(dataset1))
    cargs.append(execution.input_file(dataset2))
    ret = V3dLocalBistatOutputs(
        root=execution.output_file("."),
        output_head=execution.output_file(prefix + "+orig.HEAD"),
        output_brik=execution.output_file(prefix + "+orig.BRIK"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dLocalBistatOutputs",
    "V_3D_LOCAL_BISTAT_METADATA",
    "v_3d_local_bistat",
]
