# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__INSTALL_NIH_MARMOSET_METADATA = Metadata(
    id="bed80736e5fa98273f7fc03539dabc839ff0dee7.boutiques",
    name="@Install_NIH_Marmoset",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VInstallNihMarmosetOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__install_nih_marmoset(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def v__install_nih_marmoset(
    wget: bool = False,
    curl: bool = False,
    runner: Runner | None = None,
) -> VInstallNihMarmosetOutputs:
    """
    Installs the NIH marmoset template and atlases.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/@Install_NIH_Marmoset.html
    
    Args:
        wget: Use wget to download archive. Script chooses by default with\
            preference for curl.
        curl: Use curl to download archive. Script chooses by default with\
            preference for curl.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VInstallNihMarmosetOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__INSTALL_NIH_MARMOSET_METADATA)
    cargs = []
    cargs.append("@Install_NIH_Marmoset")
    if wget:
        cargs.append("-wget")
    if curl:
        cargs.append("-curl")
    ret = VInstallNihMarmosetOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VInstallNihMarmosetOutputs",
    "V__INSTALL_NIH_MARMOSET_METADATA",
    "v__install_nih_marmoset",
]
