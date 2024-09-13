# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_1DPLOT_METADATA = Metadata(
    id="5c20ed814370f7a719a7f440848c6bf24b99c20d.boutiques",
    name="1dplot",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V1dplotOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_1dplot(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def v_1dplot(
    tsfiles: list[InputPathType],
    runner: Runner | None = None,
) -> V1dplotOutputs:
    """
    Graphs the columns of a *.1D time series file to the X11 screen, or to an image
    file (.jpg or .png).
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/1dplot.html
    
    Args:
        tsfiles: Input time series files (*.1D) to be plotted.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V1dplotOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_1DPLOT_METADATA)
    cargs = []
    cargs.append("1dplot")
    cargs.append("[OPTIONS]")
    cargs.extend([execution.input_file(f) for f in tsfiles])
    ret = V1dplotOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V1dplotOutputs",
    "V_1DPLOT_METADATA",
    "v_1dplot",
]
