# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3DRENAME_METADATA = Metadata(
    id="b0285c183586ba4a78541b10fe878ba3fba50dd4.boutiques",
    name="3drename",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3drenameOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3drename(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def v_3drename(
    old_prefix: str,
    new_prefix: str,
    runner: Runner | None = None,
) -> V3drenameOutputs:
    """
    Tool to rename AFNI datasets by changing the dataset prefix.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3drename.html
    
    Args:
        old_prefix: Old prefix of the datasets to rename.
        new_prefix: New prefix for the datasets.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3drenameOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3DRENAME_METADATA)
    cargs = []
    cargs.append("3drename")
    cargs.append(old_prefix)
    cargs.append(new_prefix)
    ret = V3drenameOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3drenameOutputs",
    "V_3DRENAME_METADATA",
    "v_3drename",
]
