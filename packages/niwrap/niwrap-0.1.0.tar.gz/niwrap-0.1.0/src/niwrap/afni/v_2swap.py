# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_2SWAP_METADATA = Metadata(
    id="1e62c85edeb2251274dcf751c3aac90766f7d061.boutiques",
    name="2swap",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V2swapOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_2swap(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def v_2swap(
    input_files: list[InputPathType],
    quiet: bool = False,
    runner: Runner | None = None,
) -> V2swapOutputs:
    """
    Swaps byte pairs on the files listed.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/2swap.html
    
    Args:
        input_files: Input files.
        quiet: Work quietly.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V2swapOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_2SWAP_METADATA)
    cargs = []
    cargs.append("2swap")
    if quiet:
        cargs.append("-q")
    cargs.extend([execution.input_file(f) for f in input_files])
    ret = V2swapOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V2swapOutputs",
    "V_2SWAP_METADATA",
    "v_2swap",
]
