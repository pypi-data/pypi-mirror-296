# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

MRAVERAGEHEADER_METADATA = Metadata(
    id="b801a707f3ed2c058aecf4b7046515d22da3c81e.boutiques",
    name="mraverageheader",
    package="mrtrix",
    container_image_tag="mrtrix3/mrtrix3:3.0.4",
)


@dataclasses.dataclass
class MraverageheaderConfig:
    """
    temporarily set the value of an MRtrix config file entry.
    """
    key: str
    """temporarily set the value of an MRtrix config file entry."""
    value: str
    """temporarily set the value of an MRtrix config file entry."""
    
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
        cargs.append("-config")
        cargs.append(self.key)
        cargs.append(self.value)
        return cargs


class MraverageheaderOutputs(typing.NamedTuple):
    """
    Output object returned when calling `mraverageheader(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output: OutputPathType
    """the output image"""


def mraverageheader(
    input_: list[InputPathType],
    output: str,
    padding: float | None = None,
    resolution: str | None = None,
    fill: bool = False,
    datatype: str | None = None,
    info: bool = False,
    quiet: bool = False,
    debug: bool = False,
    force: bool = False,
    nthreads: int | None = None,
    config: list[MraverageheaderConfig] | None = None,
    help_: bool = False,
    version: bool = False,
    runner: Runner | None = None,
) -> MraverageheaderOutputs:
    """
    Calculate the average (unbiased) coordinate space of all input images.
    
    
    
    References:
    
    .
    
    Author: Maximilian Pietsch (maximilian.pietsch@kcl.ac.uk)
    
    URL:
    https://mrtrix.readthedocs.io/en/latest/reference/commands/mraverageheader.html
    
    Args:
        input_: the input image(s).
        output: the output image.
        padding: boundary box padding in voxels. Default: 0.
        resolution: subsampling of template compared to smallest voxel size in\
            any input image. Valid options are 'mean': unbiased but loss of\
            resolution for individual images possible, and 'max': smallest voxel\
            size of any input image defines the resolution. Default: mean.
        fill: set the intensity in the first volume of the average space to 1.
        datatype: specify output image data type. Valid choices are: float32,\
            float32le, float32be, float64, float64le, float64be, int64, uint64,\
            int64le, uint64le, int64be, uint64be, int32, uint32, int32le, uint32le,\
            int32be, uint32be, int16, uint16, int16le, uint16le, int16be, uint16be,\
            cfloat32, cfloat32le, cfloat32be, cfloat64, cfloat64le, cfloat64be,\
            int8, uint8, bit.
        info: display information messages.
        quiet: do not display information messages or progress status;\
            alternatively, this can be achieved by setting the MRTRIX_QUIET\
            environment variable to a non-empty string.
        debug: display debugging messages.
        force: force overwrite of output files (caution: using the same file as\
            input and output might cause unexpected behaviour).
        nthreads: use this number of threads in multi-threaded applications\
            (set to 0 to disable multi-threading).
        config: temporarily set the value of an MRtrix config file entry.
        help_: display this information page and exit.
        version: display version information and exit.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `MraverageheaderOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(MRAVERAGEHEADER_METADATA)
    cargs = []
    cargs.append("mraverageheader")
    if padding is not None:
        cargs.extend([
            "-padding",
            str(padding)
        ])
    if resolution is not None:
        cargs.extend([
            "-resolution",
            resolution
        ])
    if fill:
        cargs.append("-fill")
    if datatype is not None:
        cargs.extend([
            "-datatype",
            datatype
        ])
    if info:
        cargs.append("-info")
    if quiet:
        cargs.append("-quiet")
    if debug:
        cargs.append("-debug")
    if force:
        cargs.append("-force")
    if nthreads is not None:
        cargs.extend([
            "-nthreads",
            str(nthreads)
        ])
    if config is not None:
        cargs.extend([a for c in [s.run(execution) for s in config] for a in c])
    if help_:
        cargs.append("-help")
    if version:
        cargs.append("-version")
    cargs.extend([execution.input_file(f) for f in input_])
    cargs.append(output)
    ret = MraverageheaderOutputs(
        root=execution.output_file("."),
        output=execution.output_file(output),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "MRAVERAGEHEADER_METADATA",
    "MraverageheaderConfig",
    "MraverageheaderOutputs",
    "mraverageheader",
]
