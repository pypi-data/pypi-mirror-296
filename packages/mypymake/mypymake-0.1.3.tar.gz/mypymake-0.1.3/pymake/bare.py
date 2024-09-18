import os
import subprocess
from pathlib import Path

from ._types import List, Optional


class _Config:
    def __init__(self):
        self.source_files: List[Path] = []
        self.include_files: List[Path] = []

        self.source_directories: List[Path] = []
        self.include_directories: List[Path] = []

        self.defines: List[str] = []
        self.library_paths: List[Path] = []
        self.libraries: List[str] = []
        self.extra_args: List[str] = []

        self.output_directory: Path
        self.output_file: str

        self.verbose: bool = False
        self.compile_error: bool = False

    def clear(self):
        for attr, value in self.__dict__.items():
            if isinstance(value, list):
                value.clear()
            elif isinstance(value, Path):
                setattr(self, attr, Path("."))
            elif isinstance(value, bool):
                setattr(self, attr, False)


_compiler_config = _Config()


def add_source_file(*file_names: str):
    """
    Adds one or more source files for compilation.

    Args:
        file_names (str): Names of the source files.
    """
    _compiler_config.source_files.extend(Path(file_name) for file_name in file_names)


def add_source_directory(*directories: str):
    """
    Adds one or more source directories for compilation.

    Args:
        directories (str): Paths to the source directories.
    """
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                _compiler_config.source_files.append(Path(root, file))


def add_include_directory(*directories: str):
    """
    Adds one or more include directories for compilation.

    Args:
        directories (str): Paths to the include directories.
    """
    _compiler_config.include_directories.extend(
        Path(directory) for directory in directories
    )


def define(*macros: str):
    """
    Defines one or more macros for compilation.

    Args:
        macros (str): Names of the macros.
    """
    _compiler_config.defines.extend(macro for macro in macros)


def add_library_path(*paths: str):
    """
    Adds one or more library search paths.

    Args:
        paths (str): Paths to the libraries.
    """
    _compiler_config.library_paths.extend(Path(path) for path in paths)


def link_library(*library_names: str):
    """
    Links one or more libraries by name.

    Args:
        library_names (str): Names of the libraries.
    """
    _compiler_config.libraries.extend(library_name for library_name in library_names)


def add_args(*args: str):
    """
    Adds one or more extra arguments to the compiler command.

    Args:
        args (str): Extra arguments.
    """
    _compiler_config.extra_args.extend(arg for arg in args)


def set_verbose(verbose: bool = True):
    """
    Enables or disables verbose output.

    Args:
        verbose (bool): If True, enables verbose output.
    """
    _compiler_config.verbose = verbose


def build(
    output_file: str = "output",
    output_directory: str = "build",
    compiler: str = "default",
    flags: Optional[List[str]] = None,
    compile_only: bool = False,
    assembly_only: bool = False,
    preprocess_only: bool = False,
):
    """
    Compiles the program.

    Args:
        output_file (str): Name of the output file.
        compiler (str): Compiler to use.
        flags (list): List of additional compiler flags.
        compile_only (bool): If True, compile and assemble but do not link.
        assembly_only (bool): If True, compile only but do not assemble or link.
        preprocess_only (bool): If True, preprocess only, do not compile, assemble or link.
    """

    flags = flags or []

    output_dir = Path(output_directory)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    _compiler_config.output_directory = output_dir

    output_path = _compiler_config.output_directory / output_file
    cmd = [
        compiler,
        "-o",
        str(output_path),
    ]

    if preprocess_only:
        cmd.append("-E")
    elif assembly_only:
        cmd.append("-S")
    elif compile_only:
        cmd.append("-c")

    cmd.extend(str(file) for file in _compiler_config.source_files)
    cmd.extend(f"-I{directory}" for directory in _compiler_config.include_directories)
    cmd.extend(f"-D{macro}" for macro in _compiler_config.defines)
    cmd.extend(f"-L{path}" for path in _compiler_config.library_paths)
    cmd.extend(f"-l{lib}" for lib in _compiler_config.libraries)
    cmd.extend(flags)
    cmd.extend(_compiler_config.extra_args)

    if _compiler_config.verbose:
        print(f"Compile command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Compilation succeeded.")
        if _compiler_config.verbose:
            print(result.stdout, end="")
    except subprocess.CalledProcessError as e:
        print("Compilation failed:")
        print(e.stderr, end="")
        _compiler_config.compile_error = True


def run(
    output_file: str = "output",
    args: Optional[List[str]] = None,
    env: Optional[dict] = None,
) -> subprocess.CompletedProcess:
    """
    Runs the compiled program.

    Args:
        output_file (str): Name of the output file.
        args (list, optional): List of arguments to pass to the program.
        env (dict, optional): Dictionary of environment variables to set for the program.

    Returns:
        subprocess.CompletedProcess: The result of the subprocess run.

    Raises:
        FileNotFoundError: If the compiled program doesn't exist.
        PermissionError: If the user doesn't have permission to execute the program.
    """
    if _compiler_config.compile_error:
        print("Compilation failed. Cannot run the program.")
        return None

    output_path = _compiler_config.output_directory / output_file
    if os.name == "nt" and not output_path.suffix:
        output_path = output_path.with_suffix(".exe")

    if not output_path.exists():
        raise FileNotFoundError(f"Compiled program not found: {output_path}")

    command = [str(output_path)]
    if args:
        command.extend(args)

    print(f"Running '{output_path}'...")
    print("--- Output ---")

    try:
        result = subprocess.run(
            command, capture_output=True, text=True, env=env, check=True
        )
        print(result.stdout)
        if result.stderr:
            print("--- Error Output ---")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Program exited with non-zero status: {e.returncode}")
        print(e.stdout)
        if e.stderr:
            print("--- Error Output ---")
            print(e.stderr)
        result = e
    except PermissionError:
        print(f"Permission denied: Unable to execute '{output_path}'")
        return None

    print("--- End of output ---")
    print(f"Return code: {result.returncode}")

    return result
