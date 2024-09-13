# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

TBSS_3_POSTREG_METADATA = Metadata(
    id="c19a16710795ec146e134573826a707599f9e887.boutiques",
    name="tbss_3_postreg",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class Tbss3PostregOutputs(typing.NamedTuple):
    """
    Output object returned when calling `tbss_3_postreg(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def tbss_3_postreg(
    runner: Runner | None = None,
) -> Tbss3PostregOutputs:
    """
    TBSS post-registration processing.
    
    Author: Oxford Centre for Functional MRI of the Brain (FMRIB)
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/TBSS/UserGuide#tbss_3_postreg
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `Tbss3PostregOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(TBSS_3_POSTREG_METADATA)
    cargs = []
    cargs.append("tbss_3_postreg")
    cargs.append("[OPTIONS]")
    ret = Tbss3PostregOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "TBSS_3_POSTREG_METADATA",
    "Tbss3PostregOutputs",
    "tbss_3_postreg",
]
