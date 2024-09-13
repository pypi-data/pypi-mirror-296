# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

FSL_MOTION_OUTLIERS_METADATA = Metadata(
    id="eeaf3a58a08372c2bc62e13b7e1e8c46742557a1.boutiques",
    name="fsl_motion_outliers",
    package="fsl",
    container_image_tag="mcin/fsl:6.0.5",
)


class FslMotionOutliersOutputs(typing.NamedTuple):
    """
    Output object returned when calling `fsl_motion_outliers(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_confound_file: OutputPathType
    """Main output confound file"""
    metric_text_file: OutputPathType | None
    """Metric values saved as text file"""
    metric_plot_file: OutputPathType | None
    """Metric values saved as graphical plot (png format)"""


def fsl_motion_outliers(
    input_4d_image: InputPathType,
    output_confound_file: str,
    mask_image: InputPathType | None = None,
    save_metric_file: str | None = None,
    save_metric_plot: str | None = None,
    temp_path: str | None = None,
    refrms_flag: bool = False,
    dvars_flag: bool = False,
    refmse_flag: bool = False,
    fd_flag: bool = False,
    fdrms_flag: bool = False,
    abs_thresh: float | None = None,
    no_moco_flag: bool = False,
    dummy_scans: float | None = None,
    verbose_flag: bool = False,
    runner: Runner | None = None,
) -> FslMotionOutliersOutputs:
    """
    FSL tool used to calculate motion outliers in 4D image data.
    
    Author: FMRIB Analysis Group
    
    URL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLMotionOutliers
    
    Args:
        input_4d_image: Input 4D image (e.g. 4D.nii.gz).
        output_confound_file: Output confound file (e.g. confounds.txt).
        mask_image: Use supplied mask image for calculating metric.
        save_metric_file: Save metric values (e.g. DVARS) as text into\
            specified file.
        save_metric_plot: Save metric values (e.g. DVARS) as a graphical plot\
            (png format).
        temp_path: [Optional] Path to the location where temporary files should\
            be created. Defaults to /tmp.
        refrms_flag: Use RMS intensity difference to reference volume as metric.
        dvars_flag: Use DVARS as metric.
        refmse_flag: Mean Square Error version of --refrms (used in original\
            version of fsl_motion_outliers).
        fd_flag: Use FD (framewise displacement) as metric.
        fdrms_flag: Use FD with RMS matrix calculation as metric.
        abs_thresh: Specify absolute threshold value (otherwise use box-plot\
            cutoff = P75 + 1.5*IQR).
        no_moco_flag: Do not run motion correction (assumed already done).
        dummy_scans: Specify number of dummy scans to delete (before running\
            anything and creating EVs).
        verbose_flag: Verbose mode.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `FslMotionOutliersOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(FSL_MOTION_OUTLIERS_METADATA)
    cargs = []
    cargs.append("fsl_motion_outliers")
    cargs.append("-i")
    cargs.append(execution.input_file(input_4d_image))
    cargs.append("-o")
    cargs.append(output_confound_file)
    if mask_image is not None:
        cargs.extend([
            "-m",
            execution.input_file(mask_image)
        ])
    if save_metric_file is not None:
        cargs.extend([
            "-s",
            save_metric_file
        ])
    if save_metric_plot is not None:
        cargs.extend([
            "-p",
            save_metric_plot
        ])
    if temp_path is not None:
        cargs.extend([
            "-t",
            temp_path
        ])
    if refrms_flag:
        cargs.append("--refrms")
    if dvars_flag:
        cargs.append("--dvars")
    if refmse_flag:
        cargs.append("--refmse")
    if fd_flag:
        cargs.append("--fd")
    if fdrms_flag:
        cargs.append("--fdrms")
    if abs_thresh is not None:
        cargs.extend([
            "--thresh",
            str(abs_thresh)
        ])
    if no_moco_flag:
        cargs.append("--nomoco")
    if dummy_scans is not None:
        cargs.extend([
            "--dummy",
            str(dummy_scans)
        ])
    if verbose_flag:
        cargs.append("-v")
    ret = FslMotionOutliersOutputs(
        root=execution.output_file("."),
        output_confound_file=execution.output_file(output_confound_file),
        metric_text_file=execution.output_file(save_metric_file) if (save_metric_file is not None) else None,
        metric_plot_file=execution.output_file(save_metric_plot) if (save_metric_plot is not None) else None,
    )
    execution.run(cargs)
    return ret


__all__ = [
    "FSL_MOTION_OUTLIERS_METADATA",
    "FslMotionOutliersOutputs",
    "fsl_motion_outliers",
]
