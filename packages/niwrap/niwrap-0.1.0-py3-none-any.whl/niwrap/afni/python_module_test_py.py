# This file was auto generated by Styx.
# Do not edit this file directly.

import typing
import pathlib
from styxdefs import *
import dataclasses

PYTHON_MODULE_TEST_PY_METADATA = Metadata(
    id="614d501177ac8886b18aafb60fea6cd60289ed17.boutiques",
    name="python_module_test.py",
    package="afni",
    container_image_tag="afni/afni_make_build:AFNI_24.2.06",
)


class PythonModuleTestPyOutputs(typing.NamedTuple):
    """
    Output object returned when calling `python_module_test_py(...)`.
    """
    root: OutputPathType
    """Output root folder. This is the root folder for all outputs."""


def python_module_test_py(
    full_test: bool = False,
    platform_info: bool = False,
    python_ver: bool = False,
    test_defaults: bool = False,
    test_modules: list[str] | None = None,
    verbose: float | None = None,
    help_: bool = False,
    hist: bool = False,
    show_valid_opts: bool = False,
    ver: bool = False,
    runner: Runner | None = None,
) -> PythonModuleTestPyOutputs:
    """
    Test the loading of Python modules, specifically designed to ensure
    compatibility with AFNI software.
    
    Author: AFNI Team
    
    URL:
    https://afni.nimh.nih.gov/pub/dist/doc/program_help/python_module_test.py.html
    
    Args:
        full_test: Perform all of the standard tests.
        platform_info: Display system information, including OS and version\
            along with the CPU type.
        python_ver: Display the version of Python in use.
        test_defaults: Test the default module list used by AFNI programs.
        test_modules: Test the specified list of modules.
        verbose: Specify a verbose level.
        help_: Display the help message.
        hist: Display the modification history.
        show_valid_opts: Display all valid options in a short format.
        ver: Display the version number.
        runner: Command runner.
    Returns:
        NamedTuple of outputs (described in `PythonModuleTestPyOutputs`).
    """
    runner = runner or get_global_runner()
    execution = runner.start_execution(PYTHON_MODULE_TEST_PY_METADATA)
    cargs = []
    cargs.append("python_module_test.py")
    if full_test:
        cargs.append("-full_test")
    if platform_info:
        cargs.append("-platform_info")
    if python_ver:
        cargs.append("-python_ver")
    if test_defaults:
        cargs.append("-test_defaults")
    if test_modules is not None:
        cargs.extend([
            "-test_modules",
            *test_modules
        ])
    if verbose is not None:
        cargs.extend([
            "-verb",
            str(verbose)
        ])
    if help_:
        cargs.append("-help")
    if hist:
        cargs.append("-hist")
    if show_valid_opts:
        cargs.append("-show_valid_opts")
    if ver:
        cargs.append("-ver")
    ret = PythonModuleTestPyOutputs(
        root=execution.output_file("."),
    )
    execution.run(cargs)
    return ret


__all__ = [
    "PYTHON_MODULE_TEST_PY_METADATA",
    "PythonModuleTestPyOutputs",
    "python_module_test_py",
]
