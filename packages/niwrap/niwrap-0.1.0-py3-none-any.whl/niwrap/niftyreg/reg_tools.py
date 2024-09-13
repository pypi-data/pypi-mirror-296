# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

REG_TOOLS_METADATA = Metadata(
    id="8bf4e740f2ac7414b43e404dbbfdd4ff20327bbf.boutiques",
    name="reg_tools",
    package="niftyreg",
    container_image_tag="vnmd/niftyreg_1.4.0:20220819",
)


class RegToolsOutputs(typing.NamedTuple):
    """
    Output object returned when calling `reg_tools(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_image_file: OutputPathType | None
    """File containing the output image"""


def reg_tools(
    input_image: InputPathType,
    output_image: str | None = None,
    runner: Runner | None = None,
) -> RegToolsOutputs:
    """
    A versatile tool for manipulating and processing medical images.
    
    Author: Marc Modat
    
    URL: http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftyReg
    
    Args:
        input_image: Filename of the input image.
        output_image: Filename of the output image.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `RegToolsOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(REG_TOOLS_METADATA)
    cargs = []
    cargs.append("reg_tools")
    cargs.extend([
        "-in",
        execution.input_file(input_image)
    ])
    if output_image is not None:
        cargs.extend([
            "-out",
            output_image
        ])
    cargs.append("[OPTIONS]")
    ret = RegToolsOutputs(
        root=execution.output_file("."),
        output_image_file=execution.output_file(output_image) if (output_image is not None) else None,
    )
    execution.run(cargs)
    return ret


__all__ = [
    "REG_TOOLS_METADATA",
    "RegToolsOutputs",
    "reg_tools",
]
