# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

TCKDFC_METADATA = Metadata(
    id="51a5b1e93e640f64e9fa324dd21b00dc35eab082.boutiques",
    name="tckdfc",
    package="mrtrix",
    container_image_tag="mrtrix3/mrtrix3:3.0.4",
)


@dataclasses.dataclass
class TckdfcDynamic:
    """
    generate a "dynamic" (4D) output image; must additionally provide the shape
    and width (in volumes) of the sliding window.
    """
    shape: str
    """generate a "dynamic" (4D) output image; must additionally provide the
    shape and width (in volumes) of the sliding window."""
    width: int
    """generate a "dynamic" (4D) output image; must additionally provide the
    shape and width (in volumes) of the sliding window."""
    
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
        cargs.append("-dynamic")
        cargs.append(self.shape)
        cargs.append(str(self.width))
        return cargs


@dataclasses.dataclass
class TckdfcConfig:
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


class TckdfcOutputs(typing.NamedTuple):
    """
    Output object returned when calling `tckdfc(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output: OutputPathType
    """the output TW-dFC image"""


def tckdfc(
    tracks: InputPathType,
    fmri: InputPathType,
    output: str,
    static: bool = False,
    dynamic: TckdfcDynamic | None = None,
    template: InputPathType | None = None,
    vox: list[float] | None = None,
    stat_vox: str | None = None,
    backtrack: bool = False,
    upsample: int | None = None,
    info: bool = False,
    quiet: bool = False,
    debug: bool = False,
    force: bool = False,
    nthreads: int | None = None,
    config: list[TckdfcConfig] | None = None,
    help_: bool = False,
    version: bool = False,
    runner: Runner | None = None,
) -> TckdfcOutputs:
    """
    Perform the Track-Weighted Dynamic Functional Connectivity (TW-dFC) method.
    
    This command generates a Track-Weighted Image (TWI), where the contribution
    from each streamline to the image is the Pearson correlation between the
    fMRI time series at the streamline endpoints.
    
    The output image can be generated in one of two ways (note that one of these
    two command-line options MUST be provided):
    
    - "Static" functional connectivity (-static option): Each streamline
    contributes to a static 3D output image based on the correlation between the
    signals at the streamline endpoints using the entirety of the input time
    series.
    
    - "Dynamic" functional connectivity (-dynamic option): The output image is a
    4D image, with the same number of volumes as the input fMRI time series. For
    each volume, the contribution from each streamline is calculated based on a
    finite-width sliding time window, centred at the timepoint corresponding to
    that volume.
    
    Note that the -backtrack option in this command is similar, but not
    precisely equivalent, to back-tracking as can be used with
    Anatomically-Constrained Tractography (ACT) in the tckgen command. However,
    here the feature does not change the streamlines trajectories in any way; it
    simply enables detection of the fact that the input fMRI image may not
    contain a valid timeseries underneath the streamline endpoint, and where
    this occurs, searches from the streamline endpoint inwards along the
    streamline trajectory in search of a valid timeseries to sample from the
    input image.
    
    References:
    
    Calamante, F.; Smith, R.E.; Liang, X.; Zalesky, A.; Connelly, A
    Track-weighted dynamic functional connectivity (TW-dFC): a new method to
    study time-resolved functional connectivity. Brain Struct Funct, 2017, doi:
    10.1007/s00429-017-1431-1.
    
    Author: Robert E. Smith (robert.smith@florey.edu.au)
    
    URL: https://mrtrix.readthedocs.io/en/latest/reference/commands/tckdfc.html
    
    Args:
        tracks: the input track file.
        fmri: the pre-processed fMRI time series.
        output: the output TW-dFC image.
        static: generate a "static" (3D) output image.
        dynamic: generate a "dynamic" (4D) output image; must additionally\
            provide the shape and width (in volumes) of the sliding window.
        template: an image file to be used as a template for the output (the\
            output image will have the same transform and field of view).
        vox: provide either an isotropic voxel size (in mm), or comma-separated\
            list of 3 voxel dimensions.
        stat_vox: define the statistic for choosing the final voxel intensities\
            for a given contrast type given the individual values from the tracks\
            passing through each voxel\
            Options are: sum, min, mean, max (default: mean).
        backtrack: if no valid timeseries is found at the streamline endpoint,\
            back-track along the streamline trajectory until a valid timeseries is\
            found.
        upsample: upsample the tracks by some ratio using Hermite interpolation\
            before mapping (if omitted, an appropriate ratio will be determined\
            automatically).
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
        NamedTuple of outputs (described in `TckdfcOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(TCKDFC_METADATA)
    cargs = []
    cargs.append("tckdfc")
    if static:
        cargs.append("-static")
    if dynamic is not None:
        cargs.extend(dynamic.run(execution))
    if template is not None:
        cargs.extend([
            "-template",
            execution.input_file(template)
        ])
    if vox is not None:
        cargs.extend([
            "-vox",
            ",".join(map(str, vox))
        ])
    if stat_vox is not None:
        cargs.extend([
            "-stat_vox",
            stat_vox
        ])
    if backtrack:
        cargs.append("-backtrack")
    if upsample is not None:
        cargs.extend([
            "-upsample",
            str(upsample)
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
    cargs.append(execution.input_file(tracks))
    cargs.append(execution.input_file(fmri))
    cargs.append(output)
    ret = TckdfcOutputs(
        root=execution.output_file("."),
        output=execution.output_file(output),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "TCKDFC_METADATA",
    "TckdfcConfig",
    "TckdfcDynamic",
    "TckdfcOutputs",
    "tckdfc",
]
