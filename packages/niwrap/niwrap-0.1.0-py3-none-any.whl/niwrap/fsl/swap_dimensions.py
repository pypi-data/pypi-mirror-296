# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

SWAP_DIMENSIONS_METADATA = Metadata(
    id="6dc09ff3a2acdd106bfb6f85c7da49be2484d100.boutiques",
    name="swap_dimensions",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class SwapDimensionsOutputs(typing.NamedTuple):
    """
    Output object returned when calling `swap_dimensions(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    out_file_outfile: OutputPathType | None
    """Output name of image, if not provided, writes to standard output."""


def swap_dimensions(
    in_file: InputPathType,
    x_dims_cart: typing.Literal["x", "-x", "y", "-y", "z", "-z"] | None = None,
    x_dims_ras: typing.Literal["LR", "RL", "AP", "PA", "SI", "IS"] | None = None,
    y_dims_ras: typing.Literal["LR", "RL", "AP", "PA", "SI", "IS"] | None = None,
    z_dims_cart: typing.Literal["x", "-x", "y", "-y", "z", "-z"] | None = None,
    z_dims_ras: typing.Literal["LR", "RL", "AP", "PA", "SI", "IS"] | None = None,
    out_file: str | None = None,
    runner: Runner | None = None,
) -> SwapDimensionsOutputs:
    """
    this is an advanced tool that re-orders the data storage to permit changes
    between axial, sagittal and coronal slicing. When used in this mode the same
    left-right convention (also called coordinate handedness or
    radiological/neurological convention) will be maintained as long as no warning
    is printed.
    
    Author: Oxford Centre for Functional MRI of the Brain (FMRIB)
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Fslutils
    
    Args:
        in_file: Input image to swap dimensions of.
        x_dims_cart: Representation of new x axes in terms of old cartesian\
            axes.
        x_dims_ras: Representation of new x axes in terms of old anatomical\
            axes.
        y_dims_ras: Representation of new y axes in terms of old anatomical\
            axes.
        z_dims_cart: Representation of new z axes in terms of old cartesian\
            axes.
        z_dims_ras: Representation of new z axes in terms of old anatomical\
            axes.
        out_file: Output name of image, if not provided, writes to standard\
            output.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `SwapDimensionsOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(SWAP_DIMENSIONS_METADATA)
    cargs = []
    cargs.append("fslswapdim")
    cargs.append(execution.input_file(in_file))
    if x_dims_cart is not None:
        cargs.append(x_dims_cart)
    if x_dims_ras is not None:
        cargs.append(x_dims_ras)
    if y_dims_ras is not None:
        cargs.append(y_dims_ras)
    cargs.append("[B_RAS]")
    if z_dims_cart is not None:
        cargs.append(z_dims_cart)
    if z_dims_ras is not None:
        cargs.append(z_dims_ras)
    if out_file is not None:
        cargs.append(out_file)
    ret = SwapDimensionsOutputs(
        root=execution.output_file("."),
        out_file_outfile=execution.output_file(out_file) if (out_file is not None) else None,
    )
    execution.run(cargs)
    return ret


__all__ = [
    "SWAP_DIMENSIONS_METADATA",
    "SwapDimensionsOutputs",
    "swap_dimensions",
]
