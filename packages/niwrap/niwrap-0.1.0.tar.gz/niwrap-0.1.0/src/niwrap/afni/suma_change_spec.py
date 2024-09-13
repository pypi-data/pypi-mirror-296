# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

SUMA_CHANGE_SPEC_METADATA = Metadata(
    id="2f1f46eccd2cdbc80832dbdd7c28c2bc7b4896ca.boutiques",
    name="suma_change_spec",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class SumaChangeSpecOutputs(typing.NamedTuple):
    """
    Output object returned when calling `suma_change_spec(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_spec: OutputPathType | None
    """New Spec file"""
    backup_spec: OutputPathType
    """Backup of the original Spec file"""


def suma_change_spec(
    input_: InputPathType,
    state: str,
    domainparent: str | None = None,
    output: str | None = None,
    remove: bool = False,
    anatomical: bool = False,
    runner: Runner | None = None,
) -> SumaChangeSpecOutputs:
    """
    This program changes SUMA's surface specification (Spec) files.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/suma_change_spec.html
    
    Args:
        input_: SUMA Spec file to change.
        state: State within the Spec file to change.
        domainparent: New Domain Parent for the state within the Spec file.
        output: Name to which the new Spec file will be temporarily written.
        remove: Remove the automatically created backup.
        anatomical: Add 'Anatomical = Y' to the selected SurfaceState.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `SumaChangeSpecOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(SUMA_CHANGE_SPEC_METADATA)
    cargs = []
    cargs.append("suma_change_spec")
    cargs.append("-input")
    cargs.append(execution.input_file(input_))
    cargs.append("-state")
    cargs.append(state)
    cargs.append("-domainparent")
    if domainparent is not None:
        cargs.append(domainparent)
    cargs.append("-output")
    if output is not None:
        cargs.append(output)
    if remove:
        cargs.append("-remove")
    if anatomical:
        cargs.append("-anatomical")
    ret = SumaChangeSpecOutputs(
        root=execution.output_file("."),
        output_spec=execution.output_file(output) if (output is not None) else None,
        backup_spec=execution.output_file(pathlib.Path(input_).name + ".bkp"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "SUMA_CHANGE_SPEC_METADATA",
    "SumaChangeSpecOutputs",
    "suma_change_spec",
]
