# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

TTOLOGP_METADATA = Metadata(
    id="ec7bd326f37ef20eb7460f2d41957799c29390d3.boutiques",
    name="ttologp",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class TtologpOutputs(typing.NamedTuple):
    """
    Output object returned when calling `ttologp(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_logpvol: OutputPathType
    """Output volume for logp value"""


def ttologp(
    varsfile: InputPathType,
    cbsfile: InputPathType,
    dof: str,
    runner: Runner | None = None,
) -> TtologpOutputs:
    """
    Tool for computing logp.
    
    Author: Unknown
    
    Args:
        varsfile: Path to the vars file.
        cbsfile: Path to the cbs file.
        dof: Degree of freedom.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `TtologpOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(TTOLOGP_METADATA)
    cargs = []
    cargs.append("ttologp")
    cargs.append("[OPTIONS]")
    cargs.append(execution.input_file(varsfile))
    cargs.append(execution.input_file(cbsfile))
    cargs.append(dof)
    ret = TtologpOutputs(
        root=execution.output_file("."),
        output_logpvol=execution.output_file("[OUTPUTVOL].nii.gz"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "TTOLOGP_METADATA",
    "TtologpOutputs",
    "ttologp",
]
