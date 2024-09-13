# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

BIANCA_CLUSTER_STATS_METADATA = Metadata(
    id="423d2c0db4c16353a60f313d20a887bcdbff6e8b.boutiques",
    name="bianca_cluster_stats",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class BiancaClusterStatsOutputs(typing.NamedTuple):
    """
    Output object returned when calling `bianca_cluster_stats(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def bianca_cluster_stats(
    bianca_output_map: InputPathType,
    threshold: float,
    min_cluster_size: float,
    mask: InputPathType | None = None,
    runner: Runner | None = None,
) -> BiancaClusterStatsOutputs:
    """
    Calculate number of clusters and WMH volume in a BIANCA output map.
    
    Args:
        bianca_output_map: BIANCA output map file.
        threshold: Threshold value to apply.
        min_cluster_size: Minimum cluster size in voxels.
        mask: Optional mask file (in the same space as the BIANCA output map).
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `BiancaClusterStatsOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(BIANCA_CLUSTER_STATS_METADATA)
    cargs = []
    cargs.append("bianca_cluster_stats")
    cargs.append(execution.input_file(bianca_output_map))
    cargs.append(str(threshold))
    cargs.append(str(min_cluster_size))
    if mask is not None:
        cargs.append(execution.input_file(mask))
    ret = BiancaClusterStatsOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "BIANCA_CLUSTER_STATS_METADATA",
    "BiancaClusterStatsOutputs",
    "bianca_cluster_stats",
]
