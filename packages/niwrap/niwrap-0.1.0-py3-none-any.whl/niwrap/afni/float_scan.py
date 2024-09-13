# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

FLOAT_SCAN_METADATA = Metadata(
    id="ff43e34ccfb6d75bca9b732f0b330b522d1218c2.boutiques",
    name="float_scan",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class FloatScanOutputs(typing.NamedTuple):
    """
    Output object returned when calling `float_scan(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    stdout_file: OutputPathType
    """Output file with illegal values replaced by 0 when -fix flag is used"""


def float_scan(
    input_file: InputPathType,
    fix_illegal_values: bool = False,
    verbose_mode: bool = False,
    skip_count: int | None = None,
    runner: Runner | None = None,
) -> FloatScanOutputs:
    """
    Scans the input file of IEEE floating point numbers for illegal values:
    infinities and not-a-number (NaN) values.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/float_scan.html
    
    Args:
        input_file: Input file containing IEEE floating point numbers.
        fix_illegal_values: Writes a copy of the input file to stdout,\
            replacing illegal values with 0.
        verbose_mode: Verbose mode: print out index of each illegal value.
        skip_count: Skip the first n floating point locations (i.e., the first\
            4*n bytes) in the file.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `FloatScanOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(FLOAT_SCAN_METADATA)
    cargs = []
    cargs.append("float_scan")
    if fix_illegal_values:
        cargs.append("-fix")
    if verbose_mode:
        cargs.append("-v")
    if skip_count is not None:
        cargs.extend([
            "-skip",
            str(skip_count)
        ])
    cargs.append(execution.input_file(input_file))
    ret = FloatScanOutputs(
        root=execution.output_file("."),
        stdout_file=execution.output_file("stdout"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "FLOAT_SCAN_METADATA",
    "FloatScanOutputs",
    "float_scan",
]
