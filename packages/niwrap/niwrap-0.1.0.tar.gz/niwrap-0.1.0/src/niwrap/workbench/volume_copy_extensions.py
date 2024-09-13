# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

VOLUME_COPY_EXTENSIONS_METADATA = Metadata(
    id="672195e2565d266a45ebc56d42331bbbda2f500d.boutiques",
    name="volume-copy-extensions",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


class VolumeCopyExtensionsOutputs(typing.NamedTuple):
    """
    Output object returned when calling `volume_copy_extensions(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    volume_out: OutputPathType
    """the output volume"""


def volume_copy_extensions(
    data_volume: InputPathType,
    extension_volume: InputPathType,
    volume_out: str,
    opt_drop_unknown: bool = False,
    runner: Runner | None = None,
) -> VolumeCopyExtensionsOutputs:
    """
    Copy extended data to another volume file.
    
    This command copies the information in a volume file that isn't a critical
    part of the standard header or data matrix, e.g. map names, palette
    settings, label tables. If -drop-unknown is not specified, it also copies
    similar kinds of information set by other software.
    
    Author: Washington University School of Medicin
    
    Args:
        data_volume: the volume file containing the voxel data to use.
        extension_volume: the volume file containing the extensions to use.
        volume_out: the output volume.
        opt_drop_unknown: don't copy extensions that workbench doesn't\
            understand.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VolumeCopyExtensionsOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(VOLUME_COPY_EXTENSIONS_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-volume-copy-extensions")
    cargs.append(execution.input_file(data_volume))
    cargs.append(execution.input_file(extension_volume))
    cargs.append(volume_out)
    if opt_drop_unknown:
        cargs.append("-drop-unknown")
    ret = VolumeCopyExtensionsOutputs(
        root=execution.output_file("."),
        volume_out=execution.output_file(volume_out),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VOLUME_COPY_EXTENSIONS_METADATA",
    "VolumeCopyExtensionsOutputs",
    "volume_copy_extensions",
]
