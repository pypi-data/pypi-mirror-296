# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_KRUSKAL_WALLIS_METADATA = Metadata(
    id="5080047819136bf7ee4c9b16179180cf5ae64cf2.boutiques",
    name="3dKruskalWallis",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dKruskalWallisOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_kruskal_wallis(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    outfile_prefix: OutputPathType
    """Output file containing Kruskal-Wallis statistics"""


def v_3d_kruskal_wallis(
    levels: int,
    datasets: list[str],
    output: str,
    workmem: int | None = None,
    voxel: int | None = None,
    runner: Runner | None = None,
) -> V3dKruskalWallisOutputs:
    """
    This program performs nonparametric Kruskal-Wallis test for comparison of
    multiple treatments.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dKruskalWallis.html
    
    Args:
        levels: Number of treatments.
        datasets: Data set for treatment #1 through to treatment #s. Specify\
            sub-brick if more than one present.
        output: Kruskal-Wallis statistics are written to file prefixname.
        workmem: Number of megabytes of RAM to use for statistical workspace.
        voxel: Screen output for voxel # num.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dKruskalWallisOutputs`).
    """
    if not (2 <= levels): 
        raise ValueError(f"'levels' must be greater than 2 <= x but was {levels}")
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_KRUSKAL_WALLIS_METADATA)
    cargs = []
    cargs.append("3dKruskalWallis")
    cargs.extend([
        "-levels",
        str(levels)
    ])
    cargs.extend([
        "-dset",
        *datasets
    ])
    if workmem is not None:
        cargs.extend([
            "-workmem",
            str(workmem)
        ])
    if voxel is not None:
        cargs.extend([
            "-voxel",
            str(voxel)
        ])
    cargs.extend([
        "-out",
        output
    ])
    ret = V3dKruskalWallisOutputs(
        root=execution.output_file("."),
        outfile_prefix=execution.output_file(output + "+tlrc"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dKruskalWallisOutputs",
    "V_3D_KRUSKAL_WALLIS_METADATA",
    "v_3d_kruskal_wallis",
]
