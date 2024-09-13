# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

SUMA_GLXDINO_METADATA = Metadata(
    id="02ab6f18ff4f92881679815a097a59e685328a87.boutiques",
    name="SUMA_glxdino",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class SumaGlxdinoOutputs(typing.NamedTuple):
    """
    Output object returned when calling `suma_glxdino(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def suma_glxdino(
    verbose: bool = False,
    runner: Runner | None = None,
) -> SumaGlxdinoOutputs:
    """
    A simple openGL test program using GLX. If it does not run, then SUMA certainly
    won't.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/SUMA_glxdino.html
    
    Args:
        verbose: Switch on diagnostic messages.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `SumaGlxdinoOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(SUMA_GLXDINO_METADATA)
    cargs = []
    cargs.append("SUMA_glxdino")
    if verbose:
        cargs.append("-v")
    ret = SumaGlxdinoOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "SUMA_GLXDINO_METADATA",
    "SumaGlxdinoOutputs",
    "suma_glxdino",
]
