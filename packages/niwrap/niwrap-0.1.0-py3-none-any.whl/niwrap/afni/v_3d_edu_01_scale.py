# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_EDU_01_SCALE_METADATA = Metadata(
    id="c66287a408ad22ad53962773e55f53c7ce868763.boutiques",
    name="3dEdu_01_scale",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dEdu01ScaleOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_edu_01_scale(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    outfile: OutputPathType
    """Output scaled and/or masked copy of the [0]th volume of the input
    dataset"""


def v_3d_edu_01_scale(
    input_: InputPathType,
    mask: InputPathType | None = None,
    mult_factors: list[float] | None = None,
    option_flag: bool = False,
    runner: Runner | None = None,
) -> V3dEdu01ScaleOutputs:
    """
    Educational program to create a new AFNI program. Scales and masks dataset
    volumes.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dEdu_01_scale.html
    
    Args:
        input_: Input dataset.
        mask: Mask dataset on same grid/data structure as the input dataset.
        mult_factors: Numerical factors for multiplying each voxel; each voxel\
            is multiplied by both A and B.
        option_flag: Option flag to do something.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dEdu01ScaleOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_EDU_01_SCALE_METADATA)
    cargs = []
    cargs.append("3dEdu_01_scale")
    cargs.append(execution.input_file(input_))
    if mask is not None:
        cargs.extend([
            "-mask",
            execution.input_file(mask)
        ])
    if mult_factors is not None:
        cargs.extend([
            "-mult_facs",
            *map(str, mult_factors)
        ])
    if option_flag:
        cargs.append("-some_opt")
    ret = V3dEdu01ScaleOutputs(
        root=execution.output_file("."),
        outfile=execution.output_file("OUT_edu_[1-9]*"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dEdu01ScaleOutputs",
    "V_3D_EDU_01_SCALE_METADATA",
    "v_3d_edu_01_scale",
]
