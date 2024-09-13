# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

SURFACE_SET_COORDINATES_METADATA = Metadata(
    id="10e4622894f35be8d799c6136071fb0e1a9d5ed1.boutiques",
    name="surface-set-coordinates",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


class SurfaceSetCoordinatesOutputs(typing.NamedTuple):
    """
    Output object returned when calling `surface_set_coordinates(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    surface_out: OutputPathType
    """the new surface"""


def surface_set_coordinates(
    surface_in: InputPathType,
    coord_metric: InputPathType,
    surface_out: str,
    runner: Runner | None = None,
) -> SurfaceSetCoordinatesOutputs:
    """
    Modify coordinates of a surface.
    
    Takes the topology from an existing surface file, and uses values from a
    metric file as coordinates to construct a new surface file.
    
    See -surface-coordinates-to-metric for how to get surface coordinates as a
    metric file, such that you can then modify them via metric commands, etc.
    
    Author: Washington University School of Medicin
    
    Args:
        surface_in: the surface to use for the topology.
        coord_metric: the new coordinates, as a 3-column metric file.
        surface_out: the new surface.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `SurfaceSetCoordinatesOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(SURFACE_SET_COORDINATES_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-surface-set-coordinates")
    cargs.append(execution.input_file(surface_in))
    cargs.append(execution.input_file(coord_metric))
    cargs.append(surface_out)
    ret = SurfaceSetCoordinatesOutputs(
        root=execution.output_file("."),
        surface_out=execution.output_file(surface_out),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "SURFACE_SET_COORDINATES_METADATA",
    "SurfaceSetCoordinatesOutputs",
    "surface_set_coordinates",
]
