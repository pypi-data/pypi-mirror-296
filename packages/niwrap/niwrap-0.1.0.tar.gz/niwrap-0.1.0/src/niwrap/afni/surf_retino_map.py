# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

SURF_RETINO_MAP_METADATA = Metadata(
    id="6301d3d7b1303735f00712af4498f12f7c0c05f4.boutiques",
    name="SurfRetinoMap",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class SurfRetinoMapOutputs(typing.NamedTuple):
    """
    Output object returned when calling `surf_retino_map(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    vfr_output: OutputPathType
    """Output Visual Field Ratio (VFR) dataset."""
    threshold_max_output: OutputPathType
    """Maximum threshold at each node in the input datasets."""


def surf_retino_map(
    surface: str,
    polar: str,
    eccentricity: str,
    runner: Runner | None = None,
) -> SurfRetinoMapOutputs:
    """
    Tool for retinotopic mapping on cortical surfaces.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/SurfRetinoMap.html
    
    Args:
        surface: Surface on which distances are computed. See 'Specifying input\
            surfaces' section for syntax.
        polar: Retinotopic dataset: polar angle dataset.
        eccentricity: Retinotopic dataset: eccentricity angle dataset.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `SurfRetinoMapOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(SURF_RETINO_MAP_METADATA)
    cargs = []
    cargs.append("SurfRetinoMap")
    cargs.append(surface)
    cargs.append("-input")
    cargs.append(polar)
    cargs.append(eccentricity)
    cargs.append("[--prefix")
    cargs.append("PREFIX]")
    cargs.append("[--node_dbg")
    cargs.append("NODE]")
    ret = SurfRetinoMapOutputs(
        root=execution.output_file("."),
        vfr_output=execution.output_file("[PREFIX]_VFR.nii.gz"),
        threshold_max_output=execution.output_file("[PREFIX]_threshold_max.nii.gz"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "SURF_RETINO_MAP_METADATA",
    "SurfRetinoMapOutputs",
    "surf_retino_map",
]
