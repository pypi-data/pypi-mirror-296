# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_ICC_METADATA = Metadata(
    id="2f04f1351aa6871ec205758e1754b90e4b3d32ce.boutiques",
    name="3dICC",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dIccOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_icc(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_file: OutputPathType
    """Name of the output file"""


def v_3d_icc(
    model: str,
    prefix: str,
    data_table: str,
    mask: InputPathType | None = None,
    runner: Runner | None = None,
) -> V3dIccOutputs:
    """
    AFNI Program for IntraClass Correlatin (ICC) Analysis.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dICC.html
    
    Args:
        model: Model structure for all the variables. The expression FORMULA\
            with more than one variable has to be surrounded within quotes.\
            Variable names should be consistent with the ones used in the header of\
            -dataTable.
        prefix: Name of output file. For AFNI format, provide prefix only, with\
            no view+suffix needed. Filename for NIfTI format should have .nii\
            attached, while file name for surface data is expected to end with\
            .niml.dset.
        data_table: List the data structure with a header as the first line.\
            The first column is reserved with label 'Subj', and the last is\
            reserved for 'InputFile'.
        mask: Path to mask file. Only process voxels inside this mask.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dIccOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_ICC_METADATA)
    cargs = []
    cargs.append("3dICC")
    cargs.append(model)
    cargs.append("-prefix")
    cargs.append(prefix)
    cargs.append("-mask")
    if mask is not None:
        cargs.append(execution.input_file(mask))
    cargs.append("-dataTable")
    cargs.append(data_table)
    cargs.append("[OPTIONS]")
    ret = V3dIccOutputs(
        root=execution.output_file("."),
        output_file=execution.output_file(prefix),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dIccOutputs",
    "V_3D_ICC_METADATA",
    "v_3d_icc",
]
