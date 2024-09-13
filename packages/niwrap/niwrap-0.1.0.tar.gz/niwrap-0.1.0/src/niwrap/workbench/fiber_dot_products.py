# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

FIBER_DOT_PRODUCTS_METADATA = Metadata(
    id="2b1bb65a01491d04d74ebeca003acd1eba81f885.boutiques",
    name="fiber-dot-products",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


class FiberDotProductsOutputs(typing.NamedTuple):
    """
    Output object returned when calling `fiber_dot_products(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    dot_metric: OutputPathType
    """the metric of dot products"""
    f_metric: OutputPathType
    """a metric of the f values of the fiber distributions"""


def fiber_dot_products(
    white_surf: InputPathType,
    fiber_file: InputPathType,
    max_dist: float,
    direction: str,
    dot_metric: str,
    f_metric: str,
    runner: Runner | None = None,
) -> FiberDotProductsOutputs:
    """
    Compute dot products of fiber orientations with surface normals.
    
    For each vertex, this command finds the closest fiber population that
    satisfies the <direction> test, and computes the absolute value of the dot
    product of the surface normal and the normalized mean direction of each
    fiber. The <direction> test must be one of INSIDE, OUTSIDE, or ANY, which
    causes the command to only use fiber populations that are inside the
    surface, outside the surface, or to not care which direction it is from the
    surface. Each fiber population is output in a separate metric column.
    
    Author: Washington University School of Medicin
    
    Args:
        white_surf: the white/gray boundary surface.
        fiber_file: the fiber orientation file.
        max_dist: the maximum distance from any surface vertex a fiber\
            population may be, in mm.
        direction: test against surface for whether a fiber population should\
            be used.
        dot_metric: the metric of dot products.
        f_metric: a metric of the f values of the fiber distributions.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `FiberDotProductsOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(FIBER_DOT_PRODUCTS_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-fiber-dot-products")
    cargs.append(execution.input_file(white_surf))
    cargs.append(execution.input_file(fiber_file))
    cargs.append(str(max_dist))
    cargs.append(direction)
    cargs.append(dot_metric)
    cargs.append(f_metric)
    ret = FiberDotProductsOutputs(
        root=execution.output_file("."),
        dot_metric=execution.output_file(dot_metric),
        f_metric=execution.output_file(f_metric),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "FIBER_DOT_PRODUCTS_METADATA",
    "FiberDotProductsOutputs",
    "fiber_dot_products",
]
