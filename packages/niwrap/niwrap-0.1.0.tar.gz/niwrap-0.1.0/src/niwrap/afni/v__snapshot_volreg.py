# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__SNAPSHOT_VOLREG_METADATA = Metadata(
    id="e41cf6ba6d044ca81ae9c6d2ad2f6e1d5280c6d3.boutiques",
    name="@snapshot_volreg",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VSnapshotVolregOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__snapshot_volreg(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_jpeg: OutputPathType | None
    """JPEG image showing the edges of the EPI dataset overlayed on the
    anatomical dataset"""


def v__snapshot_volreg(
    anatdataset: InputPathType,
    epidataset: InputPathType,
    jname: str | None = None,
    xdisplay: str | None = None,
    runner: Runner | None = None,
) -> VSnapshotVolregOutputs:
    """
    Create a JPEG image showing the edges of an EPI dataset overlayed on an
    anatomical dataset to judge 3D registration quality.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/@snapshot_volreg.html
    
    Args:
        anatdataset: Anatomical dataset file.
        epidataset: EPI dataset file.
        jname: Name for the output JPEG file.
        xdisplay: Display number of an already running Xvfb instance.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VSnapshotVolregOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__SNAPSHOT_VOLREG_METADATA)
    cargs = []
    cargs.append("@snapshot_volreg")
    cargs.append(execution.input_file(anatdataset))
    cargs.append(execution.input_file(epidataset))
    if jname is not None:
        cargs.append(jname)
    if xdisplay is not None:
        cargs.append(xdisplay)
    ret = VSnapshotVolregOutputs(
        root=execution.output_file("."),
        output_jpeg=execution.output_file(jname + ".jpg") if (jname is not None) else None,
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VSnapshotVolregOutputs",
    "V__SNAPSHOT_VOLREG_METADATA",
    "v__snapshot_volreg",
]
