# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_NWARP_CAT_METADATA = Metadata(
    id="c34b27345b5662d5255d72d5b42d79c401a41ba7.boutiques",
    name="3dNwarpCat",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dNwarpCatOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_nwarp_cat(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_matrix: OutputPathType
    """Output matrix file when only matrix warps are provided."""
    output_dataset: OutputPathType
    """Output dataset when warp files are provided."""


def v_3d_nwarp_cat(
    output_prefix: str,
    warp1: InputPathType,
    warp2: InputPathType,
    interpolation: str | None = None,
    verbosity: bool = False,
    space_marker: str | None = None,
    additional_warps: list[InputPathType] | None = None,
    invert_final_warp: bool = False,
    extra_padding: float | None = None,
    runner: Runner | None = None,
) -> V3dNwarpCatOutputs:
    """
    Catenates (composes) 3D warps defined on a grid or via a matrix.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dNwarpCat.html
    
    Args:
        output_prefix: Prefix name for the output dataset that holds the warp.
        warp1: Specify the first warp.
        warp2: Specify the second warp.
        interpolation: Interpolation mode: linear, quintic, or wsinc5\
            (default).
        verbosity: Print various fun messages during execution.
        space_marker: Attach string 'sss' to the output dataset as its atlas\
            space marker.
        additional_warps: Additional warp files.
        invert_final_warp: Invert the final warp before output.
        extra_padding: Pad the nonlinear warps by 'PP' voxels in all\
            directions.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dNwarpCatOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_NWARP_CAT_METADATA)
    cargs = []
    cargs.append("3dNwarpCat")
    if interpolation is not None:
        cargs.extend([
            "-interp",
            interpolation
        ])
    if verbosity:
        cargs.append("-verb")
    cargs.append("-prefix")
    cargs.extend([
        "-prefix",
        output_prefix
    ])
    if space_marker is not None:
        cargs.extend([
            "-space",
            space_marker
        ])
    cargs.append("-warp1")
    cargs.extend([
        "-warp1",
        execution.input_file(warp1)
    ])
    cargs.append("-warp2")
    cargs.extend([
        "-warp2",
        execution.input_file(warp2)
    ])
    if additional_warps is not None:
        cargs.extend([execution.input_file(f) for f in additional_warps])
    if invert_final_warp:
        cargs.append("-iwarp")
    if extra_padding is not None:
        cargs.extend([
            "-expad",
            str(extra_padding)
        ])
    ret = V3dNwarpCatOutputs(
        root=execution.output_file("."),
        output_matrix=execution.output_file(output_prefix + ".aff12.1D"),
        output_dataset=execution.output_file(output_prefix + "+tlrc.HEAD"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dNwarpCatOutputs",
    "V_3D_NWARP_CAT_METADATA",
    "v_3d_nwarp_cat",
]
