# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

CONVERT_AFFINE_METADATA = Metadata(
    id="7a81c98e6ffb9e99458da7102f3f7f507d10fe49.boutiques",
    name="convert-affine",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


@dataclasses.dataclass
class ConvertAffineFromWorld:
    """
    input is a NIFTI 'world' affine.
    """
    input_: str
    """the input affine"""
    opt_inverse: bool = False
    """for files that use 'target to source' convention"""
    
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
        cargs.append("-from-world")
        cargs.append(self.input_)
        if self.opt_inverse:
            cargs.append("-inverse")
        return cargs


@dataclasses.dataclass
class ConvertAffineFromFlirt:
    """
    input is a flirt matrix.
    """
    input_: str
    """the input affine"""
    source_volume: str
    """the source volume used when generating the input affine"""
    target_volume: str
    """the target volume used when generating the input affine"""
    
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
        cargs.append("-from-flirt")
        cargs.append(self.input_)
        cargs.append(self.source_volume)
        cargs.append(self.target_volume)
        return cargs


@dataclasses.dataclass
class ConvertAffineToWorld:
    """
    write output as a NIFTI 'world' affine.
    """
    output: str
    """output - the output affine"""
    opt_inverse: bool = False
    """write file using 'target to source' convention"""
    
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
        cargs.append("-to-world")
        cargs.append(self.output)
        if self.opt_inverse:
            cargs.append("-inverse")
        return cargs


@dataclasses.dataclass
class ConvertAffineToFlirt:
    """
    write output as a flirt matrix.
    """
    output: str
    """output - the output affine"""
    source_volume: str
    """the volume you want to apply the transform to"""
    target_volume: str
    """the target space you want the transformed volume to match"""
    
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
        cargs.append("-to-flirt")
        cargs.append(self.output)
        cargs.append(self.source_volume)
        cargs.append(self.target_volume)
        return cargs


class ConvertAffineOutputs(typing.NamedTuple):
    """
    Output object returned when calling `convert_affine(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def convert_affine(
    from_world: ConvertAffineFromWorld | None = None,
    opt_from_itk_input: str | None = None,
    from_flirt: ConvertAffineFromFlirt | None = None,
    to_world: ConvertAffineToWorld | None = None,
    opt_to_itk_output: str | None = None,
    to_flirt: list[ConvertAffineToFlirt] | None = None,
    runner: Runner | None = None,
) -> ConvertAffineOutputs:
    """
    Convert an affine file between conventions.
    
    NIFTI world matrices can be used directly on mm coordinates via matrix
    multiplication, they use the NIFTI coordinate system, that is, positive X is
    right, positive Y is anterior, and positive Z is superior. Note that
    wb_command assumes that world matrices transform source coordinates to
    target coordinates, while other tools may use affines that transform target
    coordinates to source coordinates.
    
    The ITK format is used by ANTS.
    
    You must specify exactly one -from option, but you may specify multiple -to
    options, and -to-flirt may be specified more than once.
    
    Author: Washington University School of Medicin
    
    Args:
        from_world: input is a NIFTI 'world' affine.
        opt_from_itk_input: input is an ITK matrix: the input affine.
        from_flirt: input is a flirt matrix.
        to_world: write output as a NIFTI 'world' affine.
        opt_to_itk_output: write output as an ITK affine: output - the output\
            affine.
        to_flirt: write output as a flirt matrix.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `ConvertAffineOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(CONVERT_AFFINE_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-convert-affine")
    if from_world is not None:
        cargs.extend(from_world.run(execution))
    if opt_from_itk_input is not None:
        cargs.extend([
            "-from-itk",
            opt_from_itk_input
        ])
    if from_flirt is not None:
        cargs.extend(from_flirt.run(execution))
    if to_world is not None:
        cargs.extend(to_world.run(execution))
    if opt_to_itk_output is not None:
        cargs.extend([
            "-to-itk",
            opt_to_itk_output
        ])
    if to_flirt is not None:
        cargs.extend([a for c in [s.run(execution) for s in to_flirt] for a in c])
    ret = ConvertAffineOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "CONVERT_AFFINE_METADATA",
    "ConvertAffineFromFlirt",
    "ConvertAffineFromWorld",
    "ConvertAffineOutputs",
    "ConvertAffineToFlirt",
    "ConvertAffineToWorld",
    "convert_affine",
]
