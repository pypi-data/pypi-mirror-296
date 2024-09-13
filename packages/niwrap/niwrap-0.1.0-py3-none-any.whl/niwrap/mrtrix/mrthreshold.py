# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

MRTHRESHOLD_METADATA = Metadata(
    id="8568f1089ad54701e2d4499f7f58937f1bed960c.boutiques",
    name="mrthreshold",
    package="mrtrix",
    container_image_tag="mrtrix3/mrtrix3:3.0.4",
)


@dataclasses.dataclass
class MrthresholdConfig:
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


class MrthresholdOutputs(typing.NamedTuple):
    """
    Output object returned when calling `mrthreshold(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output: OutputPathType | None
    """the (optional) output binary image mask"""


def mrthreshold(
    input_: InputPathType,
    abs_: float | None = None,
    percentile: float | None = None,
    top: int | None = None,
    bottom: int | None = None,
    allvolumes: bool = False,
    ignorezero: bool = False,
    mask: InputPathType | None = None,
    comparison: str | None = None,
    invert: bool = False,
    out_masked: bool = False,
    nan: bool = False,
    info: bool = False,
    quiet: bool = False,
    debug: bool = False,
    force: bool = False,
    nthreads: int | None = None,
    config: list[MrthresholdConfig] | None = None,
    help_: bool = False,
    version: bool = False,
    output: str | None = None,
    runner: Runner | None = None,
) -> MrthresholdOutputs:
    """
    Create bitwise image by thresholding image intensity.
    
    The threshold value to be applied can be determined in one of a number of
    ways:
    
    - If no relevant command-line option is used, the command will automatically
    determine an optimal threshold;
    
    - The -abs option provides the threshold value explicitly;
    
    - The -percentile, -top and -bottom options enable more fine-grained control
    over how the threshold value is determined.
    
    The -mask option only influences those image values that contribute toward
    the determination of the threshold value; once the threshold is determined,
    it is applied to the entire image, irrespective of use of the -mask option.
    If you wish for the voxels outside of the specified mask to additionally be
    excluded from the output mask, this can be achieved by providing the
    -out_masked option.
    
    The four operators available through the "-comparison" option ("lt", "le",
    "ge" and "gt") correspond to "less-than" (<), "less-than-or-equal" (<=),
    "greater-than-or-equal" (>=) and "greater-than" (>). This offers
    fine-grained control over how the thresholding operation will behave in the
    presence of values equivalent to the threshold. By default, the command will
    select voxels with values greater than or equal to the determined threshold
    ("ge"); unless the -bottom option is used, in which case after a threshold
    is determined from the relevant lowest-valued image voxels, those voxels
    with values less than or equal to that threshold ("le") are selected. This
    provides more fine-grained control than the -invert option; the latter is
    provided for backwards compatibility, but is equivalent to selection of the
    opposite comparison within this selection.
    
    If no output image path is specified, the command will instead write to
    standard output the determined threshold value.
    
    References:
    
    * If not using any explicit thresholding mechanism:
    Ridgway, G. R.; Omar, R.; Ourselin, S.; Hill, D. L.; Warren, J. D. & Fox, N.
    C. Issues with threshold masking in voxel-based morphometry of atrophied
    brains. NeuroImage, 2009, 44, 99-111.
    
    Author: Robert E. Smith (robert.smith@florey.edu.au) and J-Donald Tournier
    (jdtournier@gmail.com)
    
    URL:
    https://mrtrix.readthedocs.io/en/latest/reference/commands/mrthreshold.html
    
    Args:
        input_: the input image to be thresholded.
        abs_: specify threshold value as absolute intensity.
        percentile: determine threshold based on some percentile of the image\
            intensity distribution.
        top: determine threshold that will result in selection of some number\
            of top-valued voxels.
        bottom: determine & apply threshold resulting in selection of some\
            number of bottom-valued voxels (note: implies threshold application\
            operator of "le" unless otherwise specified).
        allvolumes: compute a single threshold for all image volumes, rather\
            than an individual threshold per volume.
        ignorezero: ignore zero-valued input values during threshold\
            determination.
        mask: compute the threshold based only on values within an input mask\
            image.
        comparison: comparison operator to use when applying the threshold;\
            options are: lt,le,ge,gt (default = "le" for -bottom; "ge" otherwise).
        invert: invert the output binary mask (equivalent to flipping the\
            operator; provided for backwards compatibility).
        out_masked: mask the output image based on the provided input mask\
            image.
        nan: set voxels that fail the threshold to NaN rather than zero (output\
            image will be floating-point rather than binary).
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
        output: the (optional) output binary image mask.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `MrthresholdOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(MRTHRESHOLD_METADATA)
    cargs = []
    cargs.append("mrthreshold")
    if abs_ is not None:
        cargs.extend([
            "-abs",
            str(abs_)
        ])
    if percentile is not None:
        cargs.extend([
            "-percentile",
            str(percentile)
        ])
    if top is not None:
        cargs.extend([
            "-top",
            str(top)
        ])
    if bottom is not None:
        cargs.extend([
            "-bottom",
            str(bottom)
        ])
    if allvolumes:
        cargs.append("-allvolumes")
    if ignorezero:
        cargs.append("-ignorezero")
    if mask is not None:
        cargs.extend([
            "-mask",
            execution.input_file(mask)
        ])
    if comparison is not None:
        cargs.extend([
            "-comparison",
            comparison
        ])
    if invert:
        cargs.append("-invert")
    if out_masked:
        cargs.append("-out_masked")
    if nan:
        cargs.append("-nan")
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
    cargs.append(execution.input_file(input_))
    if output is not None:
        cargs.append(output)
    ret = MrthresholdOutputs(
        root=execution.output_file("."),
        output=execution.output_file(output) if (output is not None) else None,
    )
    execution.run(cargs)
    return ret


__all__ = [
    "MRTHRESHOLD_METADATA",
    "MrthresholdConfig",
    "MrthresholdOutputs",
    "mrthreshold",
]
