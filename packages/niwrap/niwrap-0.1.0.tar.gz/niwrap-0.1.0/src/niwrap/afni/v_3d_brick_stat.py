# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_BRICK_STAT_METADATA = Metadata(
    id="cd1278790e5222b357489bd257cf57d97ce7fdbf.boutiques",
    name="3dBrickStat",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dBrickStatOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_brick_stat(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    console_output: OutputPathType
    """Console output of computed statistics"""


def v_3d_brick_stat(
    dataset: str,
    runner: Runner | None = None,
) -> V3dBrickStatOutputs:
    """
    Compute voxel statistics of an input dataset.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dBrickStat.html
    
    Args:
        dataset: Input dataset.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dBrickStatOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_BRICK_STAT_METADATA)
    cargs = []
    cargs.append("3dBrickStat")
    cargs.append("[OPTIONS]")
    cargs.append(dataset)
    ret = V3dBrickStatOutputs(
        root=execution.output_file("."),
        console_output=execution.output_file("output.txt"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dBrickStatOutputs",
    "V_3D_BRICK_STAT_METADATA",
    "v_3d_brick_stat",
]
