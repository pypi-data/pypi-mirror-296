# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__DJUNCT_4D_SLICES_TO_3D_VOL_METADATA = Metadata(
    id="0afbc0363e392f4340b1280a3d038fc4032fc8f8.boutiques",
    name="@djunct_4d_slices_to_3d_vol",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VDjunct4dSlicesTo3dVolOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__djunct_4d_slices_to_3d_vol(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    outfile: OutputPathType
    """Output file generated by the tool"""


def v__djunct_4d_slices_to_3d_vol(
    do_something: bool = False,
    runner: Runner | None = None,
) -> VDjunct4dSlicesTo3dVolOutputs:
    """
    Tool description goes here.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/@djunct_4d_slices_to_3d_vol.html
    
    Args:
        do_something: Do something really useful.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VDjunct4dSlicesTo3dVolOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__DJUNCT_4D_SLICES_TO_3D_VOL_METADATA)
    cargs = []
    cargs.append("@djunct_4d_slices_to_3d_vol")
    if do_something:
        cargs.append("-do-something")
    ret = VDjunct4dSlicesTo3dVolOutputs(
        root=execution.output_file("."),
        outfile=execution.output_file("output_file"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VDjunct4dSlicesTo3dVolOutputs",
    "V__DJUNCT_4D_SLICES_TO_3D_VOL_METADATA",
    "v__djunct_4d_slices_to_3d_vol",
]
