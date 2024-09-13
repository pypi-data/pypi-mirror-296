# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_MANN_WHITNEY_METADATA = Metadata(
    id="bc4e85f7d5f25d592e756262956031e23953be5a.boutiques",
    name="3dMannWhitney",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dMannWhitneyOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_mann_whitney(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_files: OutputPathType
    """Output files for the estimated population delta and Wilcoxon-Mann-Whitney
    statistics."""


def v_3d_mann_whitney(
    dset1_x: list[str],
    dset2_y: list[str],
    output_prefix: str,
    workmem: int | None = None,
    voxel_num: int | None = None,
    runner: Runner | None = None,
) -> V3dMannWhitneyOutputs:
    """
    Performs nonparametric Mann-Whitney two-sample test.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dMannWhitney.html
    
    Args:
        dset1_x: Data set for X observations. Must specify 1 and only 1\
            sub-brick.
        dset2_y: Data set for Y observations. Must specify 1 and only 1\
            sub-brick.
        output_prefix: Estimated population delta and Wilcoxon-Mann-Whitney\
            statistics written to file.
        workmem: Number of megabytes of RAM to use for statistical workspace.
        voxel_num: Screen output for voxel # num.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dMannWhitneyOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_MANN_WHITNEY_METADATA)
    cargs = []
    cargs.append("3dMannWhitney")
    cargs.extend([
        "-dset 1",
        *dset1_x
    ])
    cargs.extend([
        "-dset 2",
        *dset2_y
    ])
    cargs.extend([
        "-out",
        output_prefix
    ])
    if workmem is not None:
        cargs.extend([
            "-workmem",
            str(workmem)
        ])
    if voxel_num is not None:
        cargs.extend([
            "-voxel",
            str(voxel_num)
        ])
    ret = V3dMannWhitneyOutputs(
        root=execution.output_file("."),
        output_files=execution.output_file(output_prefix + "*"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dMannWhitneyOutputs",
    "V_3D_MANN_WHITNEY_METADATA",
    "v_3d_mann_whitney",
]
