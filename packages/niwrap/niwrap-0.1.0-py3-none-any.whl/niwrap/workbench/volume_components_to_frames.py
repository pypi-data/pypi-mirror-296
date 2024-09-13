# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

VOLUME_COMPONENTS_TO_FRAMES_METADATA = Metadata(
    id="e45133eca7d56860fb9bc6a395802c220898015d.boutiques",
    name="volume-components-to-frames",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


class VolumeComponentsToFramesOutputs(typing.NamedTuple):
    """
    Output object returned when calling `volume_components_to_frames(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output: OutputPathType
    """the input volume converted to multiple frames of scalar type"""


def volume_components_to_frames(
    input_: InputPathType,
    output: str,
    runner: Runner | None = None,
) -> VolumeComponentsToFramesOutputs:
    """
    Convert rgb/complex volume to frames.
    
    RGB and complex datatypes are not always well supported, this command allows
    separating them into standard subvolumes for better support.
    
    Author: Washington University School of Medicin
    
    Args:
        input_: the RGB/complex-type volume.
        output: the input volume converted to multiple frames of scalar type.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VolumeComponentsToFramesOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(VOLUME_COMPONENTS_TO_FRAMES_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-volume-components-to-frames")
    cargs.append(execution.input_file(input_))
    cargs.append(output)
    ret = VolumeComponentsToFramesOutputs(
        root=execution.output_file("."),
        output=execution.output_file(output),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VOLUME_COMPONENTS_TO_FRAMES_METADATA",
    "VolumeComponentsToFramesOutputs",
    "volume_components_to_frames",
]
