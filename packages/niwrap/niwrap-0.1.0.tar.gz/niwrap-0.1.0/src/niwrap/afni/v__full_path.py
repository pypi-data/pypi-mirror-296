# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__FULL_PATH_METADATA = Metadata(
    id="55bb0db57c89c2fd7e600f678ea6686fbb3e35f7.boutiques",
    name="@FullPath",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VFullPathOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__full_path(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def v__full_path(
    input_file: InputPathType,
    runner: Runner | None = None,
) -> VFullPathOutputs:
    """
    Changes relative path to absolute one.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/@FullPath.html
    
    Args:
        input_file: Input file with relative path.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VFullPathOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__FULL_PATH_METADATA)
    cargs = []
    cargs.append("@FullPath")
    cargs.append(execution.input_file(input_file))
    ret = VFullPathOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VFullPathOutputs",
    "V__FULL_PATH_METADATA",
    "v__full_path",
]
