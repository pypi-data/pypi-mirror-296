# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_ABOVERLAP_METADATA = Metadata(
    id="6175363576e79b72e146afb18751c0b4daed0799.boutiques",
    name="3dABoverlap",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dAboverlapOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_aboverlap(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def v_3d_aboverlap(
    dataset_a: InputPathType,
    dataset_b: InputPathType,
    runner: Runner | None = None,
) -> V3dAboverlapOutputs:
    """
    Counts various metrics about how the automasks of datasets A and B overlap or
    don't overlap.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dABoverlap.html
    
    Args:
        dataset_a: First input dataset.
        dataset_b: Second input dataset.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dAboverlapOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_ABOVERLAP_METADATA)
    cargs = []
    cargs.append("3dABoverlap")
    cargs.append("[OPTIONS]")
    cargs.append(execution.input_file(dataset_a))
    cargs.append(execution.input_file(dataset_b))
    ret = V3dAboverlapOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dAboverlapOutputs",
    "V_3D_ABOVERLAP_METADATA",
    "v_3d_aboverlap",
]
