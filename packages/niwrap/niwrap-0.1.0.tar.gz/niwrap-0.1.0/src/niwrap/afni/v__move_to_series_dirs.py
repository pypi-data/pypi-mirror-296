# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__MOVE_TO_SERIES_DIRS_METADATA = Metadata(
    id="8517e78bc427c837d03316920c32177dfecc5fe3.boutiques",
    name="@move.to.series.dirs",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VMoveToSeriesDirsOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__move_to_series_dirs(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def v__move_to_series_dirs(
    runner: Runner | None = None,
) -> VMoveToSeriesDirsOutputs:
    """
    Partition DICOM files into series directories by copying or moving them to new
    series directories.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/@move.to.series.dirs.html
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VMoveToSeriesDirsOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__MOVE_TO_SERIES_DIRS_METADATA)
    cargs = []
    cargs.append("@move.to.series.dirs")
    cargs.append("[OPTIONS]")
    cargs.append("DICOM_FILES")
    ret = VMoveToSeriesDirsOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VMoveToSeriesDirsOutputs",
    "V__MOVE_TO_SERIES_DIRS_METADATA",
    "v__move_to_series_dirs",
]
