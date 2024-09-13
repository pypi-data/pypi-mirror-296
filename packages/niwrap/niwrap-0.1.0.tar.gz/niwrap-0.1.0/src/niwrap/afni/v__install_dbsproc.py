# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__INSTALL_DBSPROC_METADATA = Metadata(
    id="7ea799e46dd0c117ef48ef903424d2da68c9470f.boutiques",
    name="@Install_DBSproc",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VInstallDbsprocOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__install_dbsproc(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def v__install_dbsproc(
    use_wget: bool = False,
    use_curl: bool = False,
    runner: Runner | None = None,
) -> VInstallDbsprocOutputs:
    """
    Installs the demo archive for DBS processing tools.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/@Install_DBSproc.html
    
    Args:
        use_wget: Use wget to download archive. Script chooses by default with\
            preference for curl.
        use_curl: Use curl to download archive. Script chooses by default with\
            preference for curl.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VInstallDbsprocOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__INSTALL_DBSPROC_METADATA)
    cargs = []
    cargs.append("Install_DBSproc")
    if use_wget:
        cargs.append("-wget")
    if use_curl:
        cargs.append("-curl")
    ret = VInstallDbsprocOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VInstallDbsprocOutputs",
    "V__INSTALL_DBSPROC_METADATA",
    "v__install_dbsproc",
]
