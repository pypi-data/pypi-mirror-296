# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_TCAT_METADATA = Metadata(
    id="ac1029ce7034504c2ac9eb3016c85a214df41936.boutiques",
    name="3dTcat",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dTcatOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_tcat(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    out_file: OutputPathType
    """Output image file name."""
    out_file_: OutputPathType
    """Output file."""


def v_3d_tcat(
    in_files: InputPathType,
    rlt: typing.Literal["", "+", "++"] | None = None,
    outputtype: typing.Literal["NIFTI", "AFNI", "NIFTI_GZ"] | None = None,
    verbose: bool = False,
    runner: Runner | None = None,
) -> V3dTcatOutputs:
    """
    Concatenate sub-bricks from input datasets into one big 3D+time dataset.
    TODO Replace InputMultiPath in_files with Traits.List, if possible. Current
    version adds extra whitespace.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTcat.html
    
    Args:
        in_files: Input file to 3dtcat.
        rlt: '' or '+' or '++'. Remove linear trends in each voxel time series\
            loaded from each input dataset, separately. option -rlt removes the\
            least squares fit of 'a+b*t' to each voxel time series. option -rlt+\
            adds dataset mean back in. option -rlt++ adds overall mean of all\
            dataset timeseries back in.
        outputtype: 'nifti' or 'afni' or 'nifti_gz'. Afni output filetype.
        verbose: Print out some verbose output as the program.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dTcatOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_TCAT_METADATA)
    cargs = []
    cargs.append("3dTcat")
    if rlt is not None:
        cargs.extend([
            "-rlt",
            rlt
        ])
    cargs.append(execution.input_file(in_files))
    cargs.append("[OUT_FILE]")
    if outputtype is not None:
        cargs.append(outputtype)
    if verbose:
        cargs.append("-verb")
    ret = V3dTcatOutputs(
        root=execution.output_file("."),
        out_file=execution.output_file(pathlib.Path(in_files).name + "_tcat"),
        out_file_=execution.output_file("out_file"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dTcatOutputs",
    "V_3D_TCAT_METADATA",
    "v_3d_tcat",
]
