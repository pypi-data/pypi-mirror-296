# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_SKULL_STRIP_METADATA = Metadata(
    id="ec73db12e1aeab296dd6c197f0ccc31ced0d7f27.boutiques",
    name="3dSkullStrip",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dSkullStripOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_skull_strip(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    out_file: OutputPathType
    """Output image file name."""
    out_file_: OutputPathType
    """Output file."""


def v_3d_skull_strip(
    in_file: InputPathType,
    outputtype: typing.Literal["NIFTI", "AFNI", "NIFTI_GZ"] | None = None,
    runner: Runner | None = None,
) -> V3dSkullStripOutputs:
    """
    A program to extract the brain from surrounding tissue from MRI T1-weighted
    images.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dSkullStrip.html
    
    Args:
        in_file: Input file to 3dskullstrip.
        outputtype: 'nifti' or 'afni' or 'nifti_gz'. Afni output filetype.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dSkullStripOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_SKULL_STRIP_METADATA)
    cargs = []
    cargs.append("3dSkullStrip")
    cargs.extend([
        "-input",
        execution.input_file(in_file)
    ])
    cargs.append("[OUT_FILE]")
    if outputtype is not None:
        cargs.append(outputtype)
    ret = V3dSkullStripOutputs(
        root=execution.output_file("."),
        out_file=execution.output_file(pathlib.Path(in_file).name + "_skullstrip"),
        out_file_=execution.output_file("out_file"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dSkullStripOutputs",
    "V_3D_SKULL_STRIP_METADATA",
    "v_3d_skull_strip",
]
