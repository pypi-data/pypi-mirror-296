# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__ATLASIZE_METADATA = Metadata(
    id="92a5f64f5c4f1d01138a6ae2a38488993fd99734.boutiques",
    name="@Atlasize",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VAtlasizeOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__atlasize(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    niml_file: OutputPathType
    """Generated NIML file for the atlas"""


def v__atlasize(
    runner: Runner | None = None,
) -> VAtlasizeOutputs:
    """
    Script to turn a volumetric dataset into an AFNI atlas.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/@Atlasize.html
    
    Args:
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VAtlasizeOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__ATLASIZE_METADATA)
    cargs = []
    cargs.append("@Atlasize")
    cargs.append("[-dset")
    cargs.append("DSET]")
    cargs.append("[-space")
    cargs.append("SPACE]")
    cargs.append("[-lab_file")
    cargs.append("FILE")
    cargs.append("cLAB")
    cargs.append("cVAL]")
    cargs.append("[-lab_file_delim")
    cargs.append("COL_DELIM]")
    cargs.append("[-longnames")
    cargs.append("cLONGNAME]")
    cargs.append("[-last_longname_col")
    cargs.append("cLASTLONGNAME]")
    cargs.append("[-atlas_type")
    cargs.append("TP]")
    cargs.append("[-atlas_description")
    cargs.append("DESCRP]")
    cargs.append("[-atlas_name")
    cargs.append("NAME]")
    cargs.append("[-auto_backup]")
    cargs.append("[-centers]")
    cargs.append("[-centertype")
    cargs.append("TYPE]")
    cargs.append("[-centermask")
    cargs.append("DSET]")
    cargs.append("[-skip_novoxels]")
    cargs.append("[-h_web]")
    cargs.append("[-hweb]")
    cargs.append("[-h_view]")
    cargs.append("[-hview]")
    cargs.append("[-all_opts]")
    cargs.append("[-h_find")
    cargs.append("WORD]")
    ret = VAtlasizeOutputs(
        root=execution.output_file("."),
        niml_file=execution.output_file("[DSET].niml"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VAtlasizeOutputs",
    "V__ATLASIZE_METADATA",
    "v__atlasize",
]
