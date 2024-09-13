# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

SURFACE_CUT_RESAMPLE_METADATA = Metadata(
    id="93215402a87998c91a070948ea0ca99c7c211f17.boutiques",
    name="surface-cut-resample",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


class SurfaceCutResampleOutputs(typing.NamedTuple):
    """
    Output object returned when calling `surface_cut_resample(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    surface_out: OutputPathType
    """the output surface file"""


def surface_cut_resample(
    surface_in: InputPathType,
    current_sphere: InputPathType,
    new_sphere: InputPathType,
    surface_out: str,
    runner: Runner | None = None,
) -> SurfaceCutResampleOutputs:
    """
    Resample a cut surface.
    
    Resamples a surface file, given two spherical surfaces that are in register.
    Barycentric resampling is used, because it is usually better for resampling
    surfaces, and because it is needed to figure out the new topology anyway.
    
    Author: Washington University School of Medicin
    
    Args:
        surface_in: the surface file to resample.
        current_sphere: a sphere surface with the mesh that the input surface\
            is currently on.
        new_sphere: a sphere surface that is in register with <current-sphere>\
            and has the desired output mesh.
        surface_out: the output surface file.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `SurfaceCutResampleOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(SURFACE_CUT_RESAMPLE_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-surface-cut-resample")
    cargs.append(execution.input_file(surface_in))
    cargs.append(execution.input_file(current_sphere))
    cargs.append(execution.input_file(new_sphere))
    cargs.append(surface_out)
    ret = SurfaceCutResampleOutputs(
        root=execution.output_file("."),
        surface_out=execution.output_file(surface_out),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "SURFACE_CUT_RESAMPLE_METADATA",
    "SurfaceCutResampleOutputs",
    "surface_cut_resample",
]
