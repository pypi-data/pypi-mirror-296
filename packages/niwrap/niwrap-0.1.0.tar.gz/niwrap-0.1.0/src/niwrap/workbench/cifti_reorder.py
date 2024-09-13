# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

CIFTI_REORDER_METADATA = Metadata(
    id="99290b5497c22077215e5388634353b6a67904bc.boutiques",
    name="cifti-reorder",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


class CiftiReorderOutputs(typing.NamedTuple):
    """
    Output object returned when calling `cifti_reorder(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    cifti_out: OutputPathType
    """the reordered cifti file"""


def cifti_reorder(
    cifti_in: InputPathType,
    direction: str,
    reorder_list: str,
    cifti_out: str,
    runner: Runner | None = None,
) -> CiftiReorderOutputs:
    """
    Reorder the parcels or scalar/label maps in a cifti file.
    
    The mapping along the specified direction must be parcels, scalars, or
    labels. For pscalar or ptseries, use COLUMN to reorder the parcels. For
    dlabel, use ROW. The <reorder-list> file must contain 1-based indices
    separated by whitespace (spaces, newlines, tabs, etc), with as many indices
    as <cifti-in> has along the specified dimension. These indices specify which
    current index should end up in that position, for instance, if the current
    order is 'A B C D', and the desired order is 'D A B C', the text file should
    contain '4 1 2 3'.
    
    Author: Washington University School of Medicin
    
    Args:
        cifti_in: input cifti file.
        direction: which dimension to reorder along, ROW or COLUMN.
        reorder_list: a text file containing the desired order transformation.
        cifti_out: the reordered cifti file.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `CiftiReorderOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(CIFTI_REORDER_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-cifti-reorder")
    cargs.append(execution.input_file(cifti_in))
    cargs.append(direction)
    cargs.append(reorder_list)
    cargs.append(cifti_out)
    ret = CiftiReorderOutputs(
        root=execution.output_file("."),
        cifti_out=execution.output_file(cifti_out),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "CIFTI_REORDER_METADATA",
    "CiftiReorderOutputs",
    "cifti_reorder",
]
