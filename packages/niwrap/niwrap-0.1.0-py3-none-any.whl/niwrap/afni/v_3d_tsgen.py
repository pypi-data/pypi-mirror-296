# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_3D_TSGEN_METADATA = Metadata(
    id="410ba1425e90c9f623bd605b045f173958077c32.boutiques",
    name="3dTSgen",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V3dTsgenOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_3d_tsgen(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def v_3d_tsgen(
    input_file: InputPathType,
    signal_label: str,
    noise_label: str,
    sigma_value: float,
    output_file: str,
    in_tr_flag: bool = False,
    signal_constr: str | None = None,
    noise_constr: str | None = None,
    voxel_number: float | None = None,
    signal_coef: str | None = None,
    noise_coef: str | None = None,
    bucket_config: str | None = None,
    runner: Runner | None = None,
) -> V3dTsgenOutputs:
    """
    This program generates an AFNI 3d+time data set based on user-specified signal
    and noise models for each voxel.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTSgen.html
    
    Args:
        input_file: Filename of prototype 3d + time data file.
        signal_label: Name of the (non-linear) signal model.
        noise_label: Name of the (linear) noise model.
        sigma_value: Standard deviation of additive Gaussian noise.
        output_file: Filename of output 3d + time data file.
        in_tr_flag: Set the TR of the created timeseries to be the TR of the\
            prototype dataset. The default is TR = 1.
        signal_constr: Constraints for kth signal parameter. Format: k c d\
            where c <= gs[k] <= d.
        noise_constr: Constraints for kth noise parameter. Format: k c d where\
            c+b[k] <= gn[k] <= d+b[k].
        voxel_number: Screen output for voxel number.
        signal_coef: Write kth signal parameter gs[k]. Output 'fim' is written\
            to prefix filename.
        noise_coef: Write kth noise parameter gn[k]. Output 'fim' is written to\
            prefix filename.
        bucket_config: Create one AFNI 'bucket' dataset containing n\
            sub-bricks. n=0 creates the default output. Output 'bucket' is written\
            to prefixname.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V3dTsgenOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_3D_TSGEN_METADATA)
    cargs = []
    cargs.append("3dTSgen")
    cargs.append(execution.input_file(input_file))
    if in_tr_flag:
        cargs.append("-inTR")
    cargs.extend([
        "-signal",
        signal_label
    ])
    cargs.extend([
        "-noise",
        noise_label
    ])
    if signal_constr is not None:
        cargs.extend([
            "-sconstr",
            signal_constr
        ])
    if noise_constr is not None:
        cargs.extend([
            "-nconstr",
            noise_constr
        ])
    cargs.extend([
        "-sigma",
        str(sigma_value)
    ])
    if voxel_number is not None:
        cargs.extend([
            "-voxel",
            str(voxel_number)
        ])
    cargs.extend([
        "-output",
        output_file
    ])
    if signal_coef is not None:
        cargs.extend([
            "-scoef",
            signal_coef
        ])
    if noise_coef is not None:
        cargs.extend([
            "-ncoef",
            noise_coef
        ])
    if bucket_config is not None:
        cargs.extend([
            "-bucket",
            bucket_config
        ])
    ret = V3dTsgenOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V3dTsgenOutputs",
    "V_3D_TSGEN_METADATA",
    "v_3d_tsgen",
]
