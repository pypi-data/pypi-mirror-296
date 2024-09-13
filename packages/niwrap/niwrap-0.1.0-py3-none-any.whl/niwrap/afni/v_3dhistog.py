# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3DHISTOG_METADATA = Metadata(
    id="1b2daac11db382663e5c96c96beea0ba0cf2559b.boutiques",
    name="3dhistog",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dhistogOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3dhistog(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    histogram_output: OutputPathType
    """Histogram output when -prefix option is used"""


def v_3dhistog(
    dataset: InputPathType,
    runner: Runner | None = None,
) -> V3dhistogOutputs:
    """
    Compute histogram of a 3D dataset.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dhistog.html
    
    Args:
        dataset: Input dataset.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dhistogOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3DHISTOG_METADATA)
    cargs = []
    cargs.append("3dhistog")
    cargs.append("[EDITING_OPTIONS]")
    cargs.append("[HISTOGRAM_OPTIONS]")
    cargs.append(execution.input_file(dataset))
    ret = V3dhistogOutputs(
        root=execution.output_file("."),
        histogram_output=execution.output_file("HOUT.1D"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dhistogOutputs",
    "V_3DHISTOG_METADATA",
    "v_3dhistog",
]
