# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

METRIC_MERGE_METADATA = Metadata(
    id="b20e665ab170420a89d49fa4becc85244a5eb213.boutiques",
    name="metric-merge",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


@dataclasses.dataclass
class MetricMergeUpTo:
    """
    use an inclusive range of columns.
    """
    last_column: str
    """the number or name of the last column to include"""
    opt_reverse: bool = False
    """use the range in reverse order"""
    
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
        cargs.append("-up-to")
        cargs.append(self.last_column)
        if self.opt_reverse:
            cargs.append("-reverse")
        return cargs


@dataclasses.dataclass
class MetricMergeColumn:
    """
    select a single column to use.
    """
    column: str
    """the column number or name"""
    up_to: MetricMergeUpTo | None = None
    """use an inclusive range of columns"""
    
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
        cargs.append("-column")
        cargs.append(self.column)
        if self.up_to is not None:
            cargs.extend(self.up_to.run(execution))
        return cargs


@dataclasses.dataclass
class MetricMergeMetric:
    """
    specify an input metric.
    """
    metric_in: InputPathType
    """a metric file to use columns from"""
    column: list[MetricMergeColumn] | None = None
    """select a single column to use"""
    
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
        cargs.append("-metric")
        cargs.append(execution.input_file(self.metric_in))
        if self.column is not None:
            cargs.extend([a for c in [s.run(execution) for s in self.column] for a in c])
        return cargs


class MetricMergeOutputs(typing.NamedTuple):
    """
    Output object returned when calling `metric_merge(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    metric_out: OutputPathType
    """the output metric"""


def metric_merge(
    metric_out: str,
    metric: list[MetricMergeMetric] | None = None,
    runner: Runner | None = None,
) -> MetricMergeOutputs:
    """
    Merge metric files into a new file.
    
    Takes one or more metric files and constructs a new metric file by
    concatenating columns from them. The input metric files must have the same
    number of vertices and same structure.
    
    Example: wb_command -metric-merge out.func.gii -metric first.func.gii
    -column 1 -metric second.func.gii
    
    This example would take the first column from first.func.gii, followed by
    all columns from second.func.gii, and write these columns to out.func.gii.
    
    Author: Washington University School of Medicin
    
    Args:
        metric_out: the output metric.
        metric: specify an input metric.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `MetricMergeOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(METRIC_MERGE_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-metric-merge")
    cargs.append(metric_out)
    if metric is not None:
        cargs.extend([a for c in [s.run(execution) for s in metric] for a in c])
    ret = MetricMergeOutputs(
        root=execution.output_file("."),
        metric_out=execution.output_file(metric_out),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "METRIC_MERGE_METADATA",
    "MetricMergeColumn",
    "MetricMergeMetric",
    "MetricMergeOutputs",
    "MetricMergeUpTo",
    "metric_merge",
]
