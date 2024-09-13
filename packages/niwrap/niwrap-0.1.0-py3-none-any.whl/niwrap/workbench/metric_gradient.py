# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

METRIC_GRADIENT_METADATA = Metadata(
    id="e6d7b3765c937638ae5184fba532a06fbd8adccd.boutiques",
    name="metric-gradient",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


@dataclasses.dataclass
class MetricGradientPresmooth:
    """
    smooth the metric before computing the gradient.
    """
    kernel: float
    """the size of the gaussian smoothing kernel in mm, as sigma by default"""
    opt_fwhm: bool = False
    """kernel size is FWHM, not sigma"""
    
    def run(
        self,
        execution: Execution,
    ) -> list[str]:
        """
        Build command line arguments. This method is called by the main command.
        
        Args:
            execution: The execution object.
        Returns:
            Command line arguments
        """
        cargs = []
        cargs.append("-presmooth")
        cargs.append(str(self.kernel))
        if self.opt_fwhm:
            cargs.append("-fwhm")
        return cargs


@dataclasses.dataclass
class MetricGradientRoi:
    """
    select a region of interest to take the gradient of.
    """
    roi_metric: InputPathType
    """the area to take the gradient within, as a metric"""
    opt_match_columns: bool = False
    """for each input column, use the corresponding column from the roi"""
    
    def run(
        self,
        execution: Execution,
    ) -> list[str]:
        """
        Build command line arguments. This method is called by the main command.
        
        Args:
            execution: The execution object.
        Returns:
            Command line arguments
        """
        cargs = []
        cargs.append("-roi")
        cargs.append(execution.input_file(self.roi_metric))
        if self.opt_match_columns:
            cargs.append("-match-columns")
        return cargs


class MetricGradientOutputs(typing.NamedTuple):
    """
    Output object returned when calling `metric_gradient(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    metric_out: OutputPathType
    """the magnitude of the gradient"""
    vector_metric_out: OutputPathType
    """the vectors as a metric file"""


def metric_gradient(
    surface: InputPathType,
    metric_in: InputPathType,
    metric_out: str,
    vector_metric_out: str,
    presmooth: MetricGradientPresmooth | None = None,
    roi: MetricGradientRoi | None = None,
    opt_vectors: bool = False,
    opt_column_column: str | None = None,
    opt_corrected_areas_area_metric: InputPathType | None = None,
    opt_average_normals: bool = False,
    runner: Runner | None = None,
) -> MetricGradientOutputs:
    """
    Surface gradient of a metric file.
    
    At each vertex, the immediate neighbors are unfolded onto a plane tangent to
    the surface at the vertex (specifically, perpendicular to the normal). The
    gradient is computed using a regression between the unfolded positions of
    the vertices and their values. The gradient is then given by the slopes of
    the regression, and reconstructed as a 3D gradient vector. By default, takes
    the gradient of all columns, with no presmoothing, across the whole surface,
    without averaging the normals of the surface among neighbors.
    
    When using -corrected-areas, note that it is an approximate correction.
    Doing smoothing on individual surfaces before averaging/gradient is
    preferred, when possible, in order to make use of the original surface
    structure.
    
    Specifying an ROI will restrict the gradient to only use data from where the
    ROI metric is positive, and output zeros anywhere the ROI metric is not
    positive.
    
    By default, the first column of the roi metric is used for all input
    columns. When -match-columns is specified to the -roi option, the input and
    roi metrics must have the same number of columns, and for each input
    column's index, the same column index is used in the roi metric. If the
    -match-columns option to -roi is used while the -column option is also used,
    the number of columns of the roi metric must match the input metric, and it
    will use the roi column with the index of the selected input column.
    
    The vector output metric is organized such that the X, Y, and Z components
    from a single input column are consecutive columns.
    
    Author: Washington University School of Medicin
    
    Args:
        surface: the surface to compute the gradient on.
        metric_in: the metric to compute the gradient of.
        metric_out: the magnitude of the gradient.
        vector_metric_out: the vectors as a metric file.
        presmooth: smooth the metric before computing the gradient.
        roi: select a region of interest to take the gradient of.
        opt_vectors: output gradient vectors.
        opt_column_column: select a single column to compute the gradient of:\
            the column number or name.
        opt_corrected_areas_area_metric: vertex areas to use instead of\
            computing them from the surface: the corrected vertex areas, as a\
            metric.
        opt_average_normals: average the normals of each vertex with its\
            neighbors before using them to compute the gradient.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `MetricGradientOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(METRIC_GRADIENT_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-metric-gradient")
    cargs.append(execution.input_file(surface))
    cargs.append(execution.input_file(metric_in))
    cargs.append(metric_out)
    if presmooth is not None:
        cargs.extend(presmooth.run(execution))
    if roi is not None:
        cargs.extend(roi.run(execution))
    if opt_vectors:
        cargs.append("-vectors")
    cargs.append(vector_metric_out)
    if opt_column_column is not None:
        cargs.extend([
            "-column",
            opt_column_column
        ])
    if opt_corrected_areas_area_metric is not None:
        cargs.extend([
            "-corrected-areas",
            execution.input_file(opt_corrected_areas_area_metric)
        ])
    if opt_average_normals:
        cargs.append("-average-normals")
    ret = MetricGradientOutputs(
        root=execution.output_file("."),
        metric_out=execution.output_file(metric_out),
        vector_metric_out=execution.output_file(vector_metric_out),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "METRIC_GRADIENT_METADATA",
    "MetricGradientOutputs",
    "MetricGradientPresmooth",
    "MetricGradientRoi",
    "metric_gradient",
]
