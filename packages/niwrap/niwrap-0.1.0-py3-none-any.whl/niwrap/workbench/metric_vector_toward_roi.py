# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

METRIC_VECTOR_TOWARD_ROI_METADATA = Metadata(
    id="685141a970a934c93282eada97a659baeaf4e5ac.boutiques",
    name="metric-vector-toward-roi",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


class MetricVectorTowardRoiOutputs(typing.NamedTuple):
    """
    Output object returned when calling `metric_vector_toward_roi(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    metric_out: OutputPathType
    """the output metric"""


def metric_vector_toward_roi(
    surface: InputPathType,
    target_roi: InputPathType,
    metric_out: str,
    opt_roi_roi_metric: InputPathType | None = None,
    runner: Runner | None = None,
) -> MetricVectorTowardRoiOutputs:
    """
    Find if vectors point toward an roi.
    
    At each vertex, compute the vector along the start of the shortest path to
    the ROI.
    
    Author: Washington University School of Medicin
    
    Args:
        surface: the surface to compute on.
        target_roi: the roi to find the shortest path to.
        metric_out: the output metric.
        opt_roi_roi_metric: don't compute for vertices outside an roi: the\
            region to compute inside, as a metric.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `MetricVectorTowardRoiOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(METRIC_VECTOR_TOWARD_ROI_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-metric-vector-toward-roi")
    cargs.append(execution.input_file(surface))
    cargs.append(execution.input_file(target_roi))
    cargs.append(metric_out)
    if opt_roi_roi_metric is not None:
        cargs.extend([
            "-roi",
            execution.input_file(opt_roi_roi_metric)
        ])
    ret = MetricVectorTowardRoiOutputs(
        root=execution.output_file("."),
        metric_out=execution.output_file(metric_out),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "METRIC_VECTOR_TOWARD_ROI_METADATA",
    "MetricVectorTowardRoiOutputs",
    "metric_vector_toward_roi",
]
