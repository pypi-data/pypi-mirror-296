# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_1D_ASTRIP_METADATA = Metadata(
    id="9068ca7039fa3defb693625b26ce4071a91d5347.boutiques",
    name="1dAstrip",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V1dAstripOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_1d_astrip(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    outfile: OutputPathType
    """Output file with only numeric characters."""


def v_1d_astrip(
    infile: InputPathType,
    runner: Runner | None = None,
) -> V1dAstripOutputs:
    """
    Strips non-numeric characters from a file.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/1dAstrip.html
    
    Args:
        infile: Input file from which non-numeric characters will be stripped.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V1dAstripOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_1D_ASTRIP_METADATA)
    cargs = []
    cargs.append("1dAstrip")
    cargs.append("<" + "< " + execution.input_file(infile) + ">")
    cargs.append("[OUTPUT_FILE]")
    ret = V1dAstripOutputs(
        root=execution.output_file("."),
        outfile=execution.output_file("[OUTPUT_FILE]"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V1dAstripOutputs",
    "V_1D_ASTRIP_METADATA",
    "v_1d_astrip",
]
