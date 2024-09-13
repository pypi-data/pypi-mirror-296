# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

IMAND_METADATA = Metadata(
    id="7e28460aace134af85c4b4bfdbb0625baab1cd47.boutiques",
    name="imand",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class ImandOutputs(typing.NamedTuple):
    """
    Output object returned when calling `imand(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    outfile: OutputPathType
    """The resulting output image file."""


def imand(
    input_images: list[InputPathType],
    output_image: InputPathType,
    runner: Runner | None = None,
) -> ImandOutputs:
    """
    Image AND operation tool. Only pixels nonzero in all input images (and above the
    threshold, if given) will be output.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/imand.html
    
    Args:
        input_images: Input images to be processed. Multiple input images can\
            be specified.
        output_image: Output image file.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `ImandOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(IMAND_METADATA)
    cargs = []
    cargs.append("imand")
    cargs.append("[--thresh")
    cargs.append("THRESHOLD]")
    cargs.extend([execution.input_file(f) for f in input_images])
    cargs.append(execution.input_file(output_image))
    ret = ImandOutputs(
        root=execution.output_file("."),
        outfile=execution.output_file(pathlib.Path(output_image).name),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "IMAND_METADATA",
    "ImandOutputs",
    "imand",
]
