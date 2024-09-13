# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

INV_WARP_METADATA = Metadata(
    id="148ebf84cd4bfc0240a3090f1e3b9452eb7b5ee3.boutiques",
    name="inv_warp",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class InvWarpOutputs(typing.NamedTuple):
    """
    Output object returned when calling `inv_warp(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    inverse_warp: OutputPathType
    """Name of output file, containing warps that are the "reverse" of those in
    --warp. this will be a field-file (rather than a file of spline
    coefficients), and it will have any affine component included as part of the
    displacements."""


def inv_warp(
    warp: InputPathType,
    out_img: str,
    ref_img: InputPathType,
    absolute: bool = False,
    relative: bool = False,
    noconstraint: bool = False,
    jacobian_min: float | None = None,
    jacobian_max: float | None = None,
    debug: bool = False,
    runner: Runner | None = None,
) -> InvWarpOutputs:
    """
    
    Use FSL Invwarp to invert a FNIRT warp.
    
    Author: Nipype (interface)
    
    Args:
        warp: Filename for warp/shiftmap transform (volume).
        out_img: Filename for output (inverse warped) image.
        ref_img: Filename for new reference image.
        absolute: Use absolute warp convention (default): x' = w(x).
        relative: Use relative warp convention (default): x' = x + w(x).
        noconstraint: Do not apply jacobian constraint.
        jacobian_min: Minimum acceptable jacobian value for constraint (default\
            0.01).
        jacobian_max: Maximum acceptable jacobian value for constraint (default\
            100.0).
        debug: Turn on debugging output.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `InvWarpOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(INV_WARP_METADATA)
    cargs = []
    cargs.append("invwarp")
    cargs.append("--warp=" + execution.input_file(warp))
    cargs.append("--out=" + out_img)
    cargs.append("--ref=" + execution.input_file(ref_img))
    if absolute:
        cargs.append("--abs")
    if relative:
        cargs.append("--rel")
    if noconstraint:
        cargs.append("--noconstraint")
    if jacobian_min is not None:
        cargs.append("--jmin=" + str(jacobian_min))
    if jacobian_max is not None:
        cargs.append("--jmax=" + str(jacobian_max))
    if debug:
        cargs.append("--debug")
    ret = InvWarpOutputs(
        root=execution.output_file("."),
        inverse_warp=execution.output_file(out_img),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "INV_WARP_METADATA",
    "InvWarpOutputs",
    "inv_warp",
]
