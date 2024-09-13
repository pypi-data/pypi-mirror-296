# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

STRBLAST_METADATA = Metadata(
    id="5d0ef9b106739ab35046cccfe77a8538e51aeb84.boutiques",
    name="strblast",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class StrblastOutputs(typing.NamedTuple):
    """
    Output object returned when calling `strblast(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def strblast(
    runner: Runner | None = None,
) -> StrblastOutputs:
    """
    Finds exact copies of the target string in each of the input files, and replaces
    all characters with some junk string.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/strblast.html
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `StrblastOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(STRBLAST_METADATA)
    cargs = []
    cargs.append("strblast")
    cargs.append("[OPTIONS]")
    cargs.append("TARGETSTRING")
    cargs.append("[INPUT_FILES...]")
    ret = StrblastOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "STRBLAST_METADATA",
    "StrblastOutputs",
    "strblast",
]
