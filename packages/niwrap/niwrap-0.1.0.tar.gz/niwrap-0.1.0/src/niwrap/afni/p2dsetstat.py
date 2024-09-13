# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

P2DSETSTAT_METADATA = Metadata(
    id="6ab79ed0457127d627c12768478d8bf910fecb25.boutiques",
    name="p2dsetstat",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class P2dsetstatOutputs(typing.NamedTuple):
    """
    Output object returned when calling `p2dsetstat(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    stat_value: OutputPathType
    """The converted statistic value."""


def p2dsetstat(
    dataset: str,
    pvalue: float,
    onesided: bool = False,
    quiet: bool = False,
    runner: Runner | None = None,
) -> P2dsetstatOutputs:
    """
    Convert a p-value to a statistic of choice with reference to a specific dataset.
    
    Author: AFNI Team
    
    URL: https://afni.nimh.nih.gov/pub/dist/doc/program_help/p2dsetstat.html
    
    Args:
        dataset: Specify a dataset DDD and, if it has multiple sub-bricks, the\
            [i]th subbrick with the statistic of interest MUST be selected\
            explicitly; note the use of quotation marks around the brick selector\
            (because of the square-brackets). 'i' can be either a number or a\
            string label selector.
        pvalue: Input p-value P, which MUST be in the interval [0,1].
        onesided: One-sided test.
        quiet: Output only the final statistic value.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `P2dsetstatOutputs`).
    """
    if not (0 <= pvalue <= 1): 
        raise ValueError(f"'pvalue' must be between 0 <= x <= 1 but was {pvalue}")
    runner = runner or get_global_runner()
    execution = runner.start_execution(P2DSETSTAT_METADATA)
    cargs = []
    cargs.append("p2dsetstat")
    cargs.append("-inset")
    cargs.extend([
        "-inset",
        dataset
    ])
    cargs.append("-pval")
    cargs.extend([
        "-pval",
        str(pvalue)
    ])
    if onesided:
        cargs.append("-1sided")
    if quiet:
        cargs.append("-quiet")
    ret = P2dsetstatOutputs(
        root=execution.output_file("."),
        stat_value=execution.output_file("stdout"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "P2DSETSTAT_METADATA",
    "P2dsetstatOutputs",
    "p2dsetstat",
]
