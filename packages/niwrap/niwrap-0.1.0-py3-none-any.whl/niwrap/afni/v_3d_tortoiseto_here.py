# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_TORTOISETO_HERE_METADATA = Metadata(
    id="face4ad09f678714416dfda6cb399110cbb37e83.boutiques",
    name="3dTORTOISEtoHere",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dTortoisetoHereOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_tortoiseto_here(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_dt_file: OutputPathType
    """Output AFNI-style DT file with the following ordering of the 6 bricks:
    Dxx, Dxy, Dyy, Dxz, Dyz, Dzz."""


def v_3d_tortoiseto_here(
    dt_tort: InputPathType,
    prefix: str,
    scale_factor: float | None = None,
    flip_x: bool = False,
    flip_y: bool = False,
    flip_z: bool = False,
    runner: Runner | None = None,
) -> V3dTortoisetoHereOutputs:
    """
    Convert standard TORTOISE DTs (diagonal-first format) to standard AFNI (lower
    triangular, row-wise) format.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTORTOISEtoHere.html
    
    Args:
        dt_tort: Diffusion tensor file with six bricks of DT components ordered\
            in the TORTOISE manner (Dxx, Dyy, Dzz, Dxy, Dxz, Dyz).
        prefix: Output file name prefix. Will have N+1 bricks when GRADFILE has\
            N rows of gradients.
        scale_factor: Optional switch to rescale the DT elements, dividing by a\
            number X>0.
        flip_x: Change sign of the first element of (inner) eigenvectors.
        flip_y: Change sign of the second element of (inner) eigenvectors.
        flip_z: Change sign of the third element of (inner) eigenvectors.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dTortoisetoHereOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_TORTOISETO_HERE_METADATA)
    cargs = []
    cargs.append("3dTORTOISEtoHere")
    cargs.append("-dt_tort")
    cargs.extend([
        "-dt_tort",
        execution.input_file(dt_tort)
    ])
    cargs.append("-prefix")
    cargs.extend([
        "-prefix",
        prefix
    ])
    if scale_factor is not None:
        cargs.extend([
            "-scale_fac",
            str(scale_factor)
        ])
    if flip_x:
        cargs.append("-flip_x")
    if flip_y:
        cargs.append("-flip_y")
    if flip_z:
        cargs.append("-flip_z")
    ret = V3dTortoisetoHereOutputs(
        root=execution.output_file("."),
        output_dt_file=execution.output_file(prefix + ".nii.gz"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dTortoisetoHereOutputs",
    "V_3D_TORTOISETO_HERE_METADATA",
    "v_3d_tortoiseto_here",
]
