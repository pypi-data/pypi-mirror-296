# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_XYZCAT_METADATA = Metadata(
    id="67f42fa386d9d8b7c0ce29a5eefb7066d6a13ca5.boutiques",
    name="3dXYZcat",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dXyzcatOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_xyzcat(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_brainfile: OutputPathType | None
    """Output concatenated dataset."""
    output_headerfile: OutputPathType | None
    """Output concatenated dataset header."""


def v_3d_xyzcat(
    datasets: list[InputPathType],
    direction: str | None = None,
    prefix: str | None = None,
    verbose: bool = False,
    runner: Runner | None = None,
) -> V3dXyzcatOutputs:
    """
    Catenates datasets spatially.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dXYZcat.html
    
    Args:
        datasets: Input datasets to concatenate.
        direction: Catenate along direction 'Q' (X, Y, Z, or their synonyms I,\
            J, K).
        prefix: Use 'pname' for the output dataset prefix name.
        verbose: Print out some verbositiness as the program proceeds.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dXyzcatOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_XYZCAT_METADATA)
    cargs = []
    cargs.append("3dXYZcat")
    if direction is not None:
        cargs.extend([
            "-dir",
            direction
        ])
    if prefix is not None:
        cargs.extend([
            "-prefix",
            prefix
        ])
    if verbose:
        cargs.append("-verb")
    cargs.extend([execution.input_file(f) for f in datasets])
    ret = V3dXyzcatOutputs(
        root=execution.output_file("."),
        output_brainfile=execution.output_file(prefix + "+orig.BRIK") if (prefix is not None) else None,
        output_headerfile=execution.output_file(prefix + "+orig.HEAD") if (prefix is not None) else None,
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dXyzcatOutputs",
    "V_3D_XYZCAT_METADATA",
    "v_3d_xyzcat",
]
