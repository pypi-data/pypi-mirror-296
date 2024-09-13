# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_CLUST_COUNT_METADATA = Metadata(
    id="0c61eab7e3dd1ba960105baacb7691a7039c8be4.boutiques",
    name="3dClustCount",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dClustCountOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_clust_count(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    clustcount_niml: OutputPathType
    """Summed results file in NIML format."""
    clustcount_1_d: OutputPathType
    """Summed results file in 1D format (when '-final' is used)."""
    final_clustcount_niml: OutputPathType
    """Summed results file in NIML format (when '-final' is used)."""


def v_3d_clust_count(
    runner: Runner | None = None,
) -> V3dClustCountOutputs:
    """
    This program takes as input 1 or more datasets, thresholds them at various
    levels, and counts up the number of clusters of various sizes.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dClustCount.html
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dClustCountOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_CLUST_COUNT_METADATA)
    cargs = []
    cargs.append("3dClustCount")
    cargs.append("[OPTIONS]")
    cargs.append("DATASETS")
    ret = V3dClustCountOutputs(
        root=execution.output_file("."),
        clustcount_niml=execution.output_file("[PREFIX].clustcount.niml"),
        clustcount_1_d=execution.output_file("[PREFIX].1D"),
        final_clustcount_niml=execution.output_file("[PREFIX].niml"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dClustCountOutputs",
    "V_3D_CLUST_COUNT_METADATA",
    "v_3d_clust_count",
]
