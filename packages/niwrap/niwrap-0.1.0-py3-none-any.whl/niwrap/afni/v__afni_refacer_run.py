# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

V__AFNI_REFACER_RUN_METADATA = Metadata(
    id="199fdd53bee9a4f018fe31df30c5f175273c29d2.boutiques",
    name="@afni_refacer_run",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class VAfniRefacerRunOutputs(typing.NamedTuple):
    """
    Output object returned when calling `v__afni_refacer_run(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output_deface: OutputPathType
    """Defaced volume (face+ears replaced with zeros)"""
    output_reface: OutputPathType
    """Refaced volume (face+ears replaced with artificial values)"""
    output_reface_plus: OutputPathType
    """Reface_plused volume (face+ears+skull replaced with artificial values)"""
    output_face: OutputPathType
    """Face+ears used to replace or remove subject data"""
    output_face_plus: OutputPathType
    """Face+ears+skull used to replace subject data"""


def v__afni_refacer_run(
    input_file: InputPathType,
    prefix: str,
    mode_all: bool = False,
    anonymize_output: bool = False,
    cost_function: str | None = None,
    shell_option: str | None = None,
    no_clean: bool = False,
    no_images: bool = False,
    overwrite: bool = False,
    verbose: bool = False,
    runner: Runner | None = None,
) -> VAfniRefacerRunOutputs:
    """
    This script re-faces one input dataset, using a master shell dataset to write
    over the subject's 'face' region.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/@afni_refacer_run.html
    
    Args:
        input_file: Name of input dataset; can contain path information.
        prefix: Name of output dataset.
        mode_all: Output three volumes: one defaced, one refaced and one\
            reface_plused.
        anonymize_output: Use 3drefit and nifti_tool to anonymize the output\
            datasets.
        cost_function: Specify any cost function that is allowed by 3dAllineate\
            (default: lpa).
        shell_option: Specify which shell to use. Options:\
            afni_refacer_shell_sym_1.0.nii.gz (traditional),\
            afni_refacer_shell_sym_2.0.nii.gz (more face/neck removal). Default:\
            afni_refacer_shell_sym_1.0.nii.gz.
        no_clean: Don't delete temp working directory (default: remove working\
            directory).
        no_images: Don't make pretty images to automatically view the results\
            of re/defacing.
        overwrite: Final two file outputs will overwrite any existing files of\
            the same name (default: don't do this). NB: this option does not apply\
            to the working directory.
        verbose: Run the 3dAllineate part herein with '-verb' (for verbosity).
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `VAfniRefacerRunOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(V__AFNI_REFACER_RUN_METADATA)
    cargs = []
    cargs.append("@afni_refacer_run")
    cargs.append("-input")
    cargs.append(execution.input_file(input_file))
    if mode_all:
        cargs.append("-mode_all")
    cargs.append("-prefix")
    cargs.extend([
        "-prefix",
        prefix
    ])
    if anonymize_output:
        cargs.append("-anonymize_output")
    if cost_function is not None:
        cargs.extend([
            "-cost",
            cost_function
        ])
    if shell_option is not None:
        cargs.extend([
            "-shell",
            shell_option
        ])
    if no_clean:
        cargs.append("-no_clean")
    if no_images:
        cargs.append("-no_images")
    if overwrite:
        cargs.append("-overwrite")
    if verbose:
        cargs.append("-verb_allin")
    ret = VAfniRefacerRunOutputs(
        root=execution.output_file("."),
        output_deface=execution.output_file(prefix + ".deface.nii.gz"),
        output_reface=execution.output_file(prefix + ".reface.nii.gz"),
        output_reface_plus=execution.output_file(prefix + ".reface_plus.nii.gz"),
        output_face=execution.output_file(prefix + ".face.nii.gz"),
        output_face_plus=execution.output_file(prefix + ".face_plus.nii.gz"),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "VAfniRefacerRunOutputs",
    "V__AFNI_REFACER_RUN_METADATA",
    "v__afni_refacer_run",
]
