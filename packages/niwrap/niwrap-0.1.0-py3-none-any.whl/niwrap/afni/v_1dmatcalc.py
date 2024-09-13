# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V_1DMATCALC_METADATA = Metadata(
    id="e6d002dffc94c6e5ac26f600399471ff7e3b57fb.boutiques",
    name="1dmatcalc",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class V1dmatcalcOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v_1dmatcalc(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_file: OutputPathType
    """Output file resulting from the evaluated expression"""


def v_1dmatcalc(
    expression: str | None = None,
    runner: Runner | None = None,
) -> V1dmatcalcOutputs:
    """
    A tool to evaluate space-delimited RPN (Reverse Polish Notation) matrix-valued
    expressions.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/1dmatcalc.html
    
    Args:
        expression: Expression to evaluate the RPN matrix-valued operations.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `V1dmatcalcOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V_1DMATCALC_METADATA)
    cargs = []
    cargs.append("1dmatcalc")
    if expression is not None:
        cargs.append(expression)
    ret = V1dmatcalcOutputs(
        root=execution.output_file("."),
        output_file=execution.output_file("[OUTPUT_FILE]"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "V1dmatcalcOutputs",
    "V_1DMATCALC_METADATA",
    "v_1dmatcalc",
]
