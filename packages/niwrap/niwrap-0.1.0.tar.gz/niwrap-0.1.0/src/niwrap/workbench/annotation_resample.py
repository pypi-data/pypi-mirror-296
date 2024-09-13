# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

ANNOTATION_RESAMPLE_METADATA = Metadata(
    id="97a1012c1e236672dd4a3e38c6d31fbee2a10f0f.boutiques",
    name="annotation-resample",
    package="workbench",
    container_image_tag="brainlife/connectome_workbench:1.5.0-freesurfer-update",
)


@dataclasses.dataclass
class AnnotationResampleSurfacePair:
    """
    pair of surfaces for resampling surface annotations for one structure.
    """
    source_surface: InputPathType
    """the midthickness surface of the current mesh the annotations use"""
    target_surface: InputPathType
    """the midthickness surface of the mesh the annotations should be
    transferred to"""
    
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
        cargs.append("-surface-pair")
        cargs.append(execution.input_file(self.source_surface))
        cargs.append(execution.input_file(self.target_surface))
        return cargs


class AnnotationResampleOutputs(typing.NamedTuple):
    """
    Output object returned when calling `annotation_resample(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def annotation_resample(
    annotation_in: InputPathType,
    annotation_out: str,
    surface_pair: list[AnnotationResampleSurfacePair] | None = None,
    runner: Runner | None = None,
) -> AnnotationResampleOutputs:
    """
    Resample an annotation file to different meshes.
    
    Resample an annotation file from the source mesh to the target mesh.
    
    Only annotations in surface space are modified, no changes are made to
    annotations in other spaces. The -surface-pair option may be repeated for
    additional structures used by surface space annotations.
    
    Author: Washington University School of Medicin
    
    Args:
        annotation_in: the annotation file to resample.
        annotation_out: name of resampled annotation file.
        surface_pair: pair of surfaces for resampling surface annotations for\
            one structure.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `AnnotationResampleOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(ANNOTATION_RESAMPLE_METADATA)
    cargs = []
    cargs.append("wb_command")
    cargs.append("-annotation-resample")
    cargs.append(execution.input_file(annotation_in))
    cargs.append(annotation_out)
    if surface_pair is not None:
        cargs.extend([a for c in [s.run(execution) for s in surface_pair] for a in c])
    ret = AnnotationResampleOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "ANNOTATION_RESAMPLE_METADATA",
    "AnnotationResampleOutputs",
    "AnnotationResampleSurfacePair",
    "annotation_resample",
]
