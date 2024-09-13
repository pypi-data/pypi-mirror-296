# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

DWIEXTRACT_METADATA = Metadata(
    id="0671192cc8b8c9f31703ecba4585dd82f28ae520.boutiques",
    name="dwiextract",
    package="mrtrix",
    container_image_tag="mrtrix3/mrtrix3:3.0.4",
)


@dataclasses.dataclass
class DwiextractFslgrad:
    """
    Provide the diffusion-weighted gradient scheme used in the acquisition in
    FSL bvecs/bvals format files. If a diffusion gradient scheme is present in
    the input image header, the data provided with this option will be instead
    used.
    """
    bvecs: InputPathType
    """Provide the diffusion-weighted gradient scheme used in the acquisition in
    FSL bvecs/bvals format files. If a diffusion gradient scheme is present in
    the input image header, the data provided with this option will be instead
    used."""
    bvals: InputPathType
    """Provide the diffusion-weighted gradient scheme used in the acquisition in
    FSL bvecs/bvals format files. If a diffusion gradient scheme is present in
    the input image header, the data provided with this option will be instead
    used."""
    
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
        cargs.append("-fslgrad")
        cargs.append(execution.input_file(self.bvecs))
        cargs.append(execution.input_file(self.bvals))
        return cargs


class DwiextractExportGradFslOutputs(typing.NamedTuple):
    """
    Output object returned when calling `DwiextractExportGradFsl | None(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    bvecs_path: OutputPathType
    """export the diffusion-weighted gradient table to files in FSL (bvecs /
    bvals) format"""
    bvals_path: OutputPathType
    """export the diffusion-weighted gradient table to files in FSL (bvecs /
    bvals) format"""


@dataclasses.dataclass
class DwiextractExportGradFsl:
    """
    export the diffusion-weighted gradient table to files in FSL (bvecs / bvals)
    format.
    """
    bvecs_path: str
    """export the diffusion-weighted gradient table to files in FSL (bvecs /
    bvals) format"""
    bvals_path: str
    """export the diffusion-weighted gradient table to files in FSL (bvecs /
    bvals) format"""
    
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
        cargs.append("-export_grad_fsl")
        cargs.append(self.bvecs_path)
        cargs.append(self.bvals_path)
        return cargs
    
    def outputs(
        self,
        execution: Execution,
    ) -> DwiextractExportGradFslOutputs:
        """
        Collect output file paths.
        
        Args:
            execution: The execution object.
        Returns:
            NamedTuple of outputs (described in `DwiextractExportGradFslOutputs`).
        """
        ret = DwiextractExportGradFslOutputs(
            root=execution.output_file("."),
            bvecs_path=execution.output_file(self.bvecs_path),
            bvals_path=execution.output_file(self.bvals_path),
        )
        return ret


@dataclasses.dataclass
class DwiextractImportPeEddy:
    """
    import phase-encoding information from an EDDY-style config / index file
    pair.
    """
    config: InputPathType
    """import phase-encoding information from an EDDY-style config / index file
    pair"""
    indices: InputPathType
    """import phase-encoding information from an EDDY-style config / index file
    pair"""
    
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
        cargs.append("-import_pe_eddy")
        cargs.append(execution.input_file(self.config))
        cargs.append(execution.input_file(self.indices))
        return cargs


@dataclasses.dataclass
class DwiextractConfig:
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


class DwiextractOutputs(typing.NamedTuple):
    """
    Output object returned when calling `dwiextract(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""
    output: OutputPathType
    """the output image (diffusion-weighted volumes by default)."""
    export_grad_mrtrix: OutputPathType | None
    """export the diffusion-weighted gradient table to file in MRtrix format """
    export_grad_fsl: DwiextractExportGradFslOutputs | None
    """Outputs from `DwiextractExportGradFsl`."""


def dwiextract(
    input_: InputPathType,
    output: str,
    bzero: bool = False,
    no_bzero: bool = False,
    singleshell: bool = False,
    grad: InputPathType | None = None,
    fslgrad: DwiextractFslgrad | None = None,
    shells: list[float] | None = None,
    export_grad_mrtrix: str | None = None,
    export_grad_fsl: DwiextractExportGradFsl | None = None,
    import_pe_table: InputPathType | None = None,
    import_pe_eddy: DwiextractImportPeEddy | None = None,
    pe: list[float] | None = None,
    strides: str | None = None,
    info: bool = False,
    quiet: bool = False,
    debug: bool = False,
    force: bool = False,
    nthreads: int | None = None,
    config: list[DwiextractConfig] | None = None,
    help_: bool = False,
    version: bool = False,
    runner: Runner | None = None,
) -> DwiextractOutputs:
    """
    Extract diffusion-weighted volumes, b=0 volumes, or certain shells from a DWI
    dataset.
    
    
    
    References:
    
    .
    
    Author: David Raffelt (david.raffelt@florey.edu.au) and Thijs Dhollander
    (thijs.dhollander@gmail.com) and Robert E. Smith
    (robert.smith@florey.edu.au)
    
    URL:
    https://mrtrix.readthedocs.io/en/latest/reference/commands/dwiextract.html
    
    Args:
        input_: the input DW image.
        output: the output image (diffusion-weighted volumes by default).
        bzero: Output b=0 volumes (instead of the diffusion weighted volumes,\
            if -singleshell is not specified).
        no_bzero: Output only non b=0 volumes (default, if -singleshell is not\
            specified).
        singleshell: Force a single-shell (single non b=0 shell) output. This\
            will include b=0 volumes, if present. Use with -bzero to enforce\
            presence of b=0 volumes (error if not present) or with -no_bzero to\
            exclude them.
        grad: Provide the diffusion-weighted gradient scheme used in the\
            acquisition in a text file. This should be supplied as a 4xN text file\
            with each line is in the format [ X Y Z b ], where [ X Y Z ] describe\
            the direction of the applied gradient, and b gives the b-value in units\
            of s/mm^2. If a diffusion gradient scheme is present in the input image\
            header, the data provided with this option will be instead used.
        fslgrad: Provide the diffusion-weighted gradient scheme used in the\
            acquisition in FSL bvecs/bvals format files. If a diffusion gradient\
            scheme is present in the input image header, the data provided with\
            this option will be instead used.
        shells: specify one or more b-values to use during processing, as a\
            comma-separated list of the desired approximate b-values (b-values are\
            clustered to allow for small deviations). Note that some commands are\
            incompatible with multiple b-values, and will report an error if more\
            than one b-value is provided.\
            WARNING: note that, even though the b=0 volumes are never referred\
            to as shells in the literature, they still have to be explicitly\
            included in the list of b-values as provided to the -shell option!\
            Several algorithms which include the b=0 volumes in their\
            computations may otherwise return an undesired result.
        export_grad_mrtrix: export the diffusion-weighted gradient table to\
            file in MRtrix format.
        export_grad_fsl: export the diffusion-weighted gradient table to files\
            in FSL (bvecs / bvals) format.
        import_pe_table: import a phase-encoding table from file.
        import_pe_eddy: import phase-encoding information from an EDDY-style\
            config / index file pair.
        pe: select volumes with a particular phase encoding; this can be three\
            comma-separated values (for i,j,k components of vector direction) or\
            four (direction & total readout time).
        strides: specify the strides of the output data in memory; either as a\
            comma-separated list of (signed) integers, or as a template image from\
            which the strides shall be extracted and used. The actual strides\
            produced will depend on whether the output image format can support it.
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
        NamedTuple of outputs (described in `DwiextractOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(DWIEXTRACT_METADATA)
    cargs = []
    cargs.append("dwiextract")
    if bzero:
        cargs.append("-bzero")
    if no_bzero:
        cargs.append("-no_bzero")
    if singleshell:
        cargs.append("-singleshell")
    if grad is not None:
        cargs.extend([
            "-grad",
            execution.input_file(grad)
        ])
    if fslgrad is not None:
        cargs.extend(fslgrad.run(execution))
    if shells is not None:
        cargs.extend([
            "-shells",
            ",".join(map(str, shells))
        ])
    if export_grad_mrtrix is not None:
        cargs.extend([
            "-export_grad_mrtrix",
            export_grad_mrtrix
        ])
    if export_grad_fsl is not None:
        cargs.extend(export_grad_fsl.run(execution))
    if import_pe_table is not None:
        cargs.extend([
            "-import_pe_table",
            execution.input_file(import_pe_table)
        ])
    if import_pe_eddy is not None:
        cargs.extend(import_pe_eddy.run(execution))
    if pe is not None:
        cargs.extend([
            "-pe",
            ",".join(map(str, pe))
        ])
    if strides is not None:
        cargs.extend([
            "-strides",
            strides
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
    cargs.append(execution.input_file(input_))
    cargs.append(output)
    ret = DwiextractOutputs(
        root=execution.output_file("."),
        output=execution.output_file(output),
        export_grad_mrtrix=execution.output_file(export_grad_mrtrix) if (export_grad_mrtrix is not None) else None,
        export_grad_fsl=export_grad_fsl.outputs(execution) if export_grad_fsl else None,
    )
    execution.run(cargs)
    return ret


__all__ = [
    "DWIEXTRACT_METADATA",
    "DwiextractConfig",
    "DwiextractExportGradFsl",
    "DwiextractExportGradFslOutputs",
    "DwiextractFslgrad",
    "DwiextractImportPeEddy",
    "DwiextractOutputs",
    "dwiextract",
]
