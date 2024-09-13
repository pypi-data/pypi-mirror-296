# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_1D_TOOL_PY_METADATA = Metadata(
    id="29ac72eff5de4e478010309bcc7d43ce29550d2f.boutiques",
    name="1d_tool.py",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V1dToolPyOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_1d_tool_py(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    outfile: OutputPathType
    """Resulting 1D file"""


def v_1d_tool_py(
    runner: Runner | None = None,
) -> V1dToolPyOutputs:
    """
    A tool for manipulating and evaluating 1D files.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/1d_tool.py.html
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V1dToolPyOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_1D_TOOL_PY_METADATA)
    cargs = []
    cargs.append("1d_tool.py")
    cargs.append("[OPTIONS]")
    ret = V1dToolPyOutputs(
        root=execution.output_file("."),
        outfile=execution.output_file("[OUTPUT_FILE]"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V1dToolPyOutputs",
    "V_1D_TOOL_PY_METADATA",
    "v_1d_tool_py",
]
