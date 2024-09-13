# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

MYGET_METADATA = Metadata(
    id="d5f031775f5d1ca0a0787b1ee69ac5daafd730c8.boutiques",
    name="myget",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class MygetOutputs(typing.NamedTuple):
    """
    Output object returned when calling `myget(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_file: OutputPathType
    """The filename to save the downloaded file"""


def myget(
    url: str,
    protocol_version: typing.Literal["-1", "-1.1"] | None = None,
    runner: Runner | None = None,
) -> MygetOutputs:
    """
    A simple file downloader from a URL.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/myget.html
    
    Args:
        url: The URL to download the file from.
        protocol_version: Specify protocol version. You can choose between -1\
            or -1.1.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `MygetOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(MYGET_METADATA)
    cargs = []
    cargs.append("myget")
    if protocol_version is not None:
        cargs.append(protocol_version)
    cargs.append(url)
    cargs.append(">")
    cargs.append("[OUTPUT_FILE]")
    ret = MygetOutputs(
        root=execution.output_file("."),
        output_file=execution.output_file("[OUTPUT_FILE]"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "MYGET_METADATA",
    "MygetOutputs",
    "myget",
]
