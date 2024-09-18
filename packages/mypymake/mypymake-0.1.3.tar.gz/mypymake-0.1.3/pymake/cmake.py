import subprocess
from pathlib import Path
import os
from typing import Optional, List, Dict, Union


class _Config:
    def __init__(self):
        self.cmake_lists_path: Optional[Path] = None
        self.verbose: bool = False
        self.build_dir: str = "build"
        self.build_type: str = "Release"

    def clear(self):
        self.__init__()


_config = _Config()


def set_verbose(verbose: bool = True) -> None:
    _config.verbose = verbose


def set_build_options(build_dir: str = "build", build_type: str = "Release") -> None:
    _config.build_dir = build_dir
    _config.build_type = build_type


def _search_for_cmake_lists(path: Union[str, Path]) -> Optional[Path]:
    try:
        path = Path(path).resolve()
        if path.is_file() and path.name.lower() == "cmakelists.txt":
            return path
        elif path.is_dir():
            for child in path.iterdir():
                result = _search_for_cmake_lists(child)
                if result is not None:
                    return result
    except (PermissionError, OSError) as e:
        print(f"Error accessing {path}: {e}")
    return None


def search_for_cmake_lists(path: Union[str, Path]) -> Optional[Path]:
    try:
        path = Path(path).resolve()
        result = _search_for_cmake_lists(path)
        _config.cmake_lists_path = result
        return result
    except Exception as e:
        print(f"Error in search_for_cmake_lists: {e}")
        return None


def build() -> None:
    if _config.cmake_lists_path is None:
        raise ValueError("CMakeLists.txt not found")

    cmake_source_dir = _config.cmake_lists_path.parent
    build_path = Path(_config.build_dir)

    cmake_configure_cmd = [
        "cmake",
        "-S",
        str(cmake_source_dir),
        "-B",
        str(build_path),
        f"-DCMAKE_BUILD_TYPE={_config.build_type}",
    ]

    print(f"Configuring CMake project in {cmake_source_dir}")
    try:
        result = subprocess.run(
            cmake_configure_cmd, check=True, capture_output=True, text=True
        )
        if _config.verbose:
            print(f"CMake configuration output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"CMake configuration failed: {e.stderr}")
        raise

    cmake_build_cmd = [
        "cmake",
        "--build",
        str(build_path),
        "--config",
        _config.build_type,
    ]
    if _config.verbose:
        cmake_build_cmd.extend(["--verbose"])

    print(f"Building CMake project in {build_path}")
    try:
        result = subprocess.run(
            cmake_build_cmd, check=True, capture_output=True, text=True
        )
        if _config.verbose:
            print(f"CMake build output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"CMake build failed: {e.stderr}")
        raise

    print("CMake build completed successfully")


def run_target(target: str) -> None:
    if _config.cmake_lists_path is None:
        raise ValueError("CMakeLists.txt not found")

    build_path = Path(_config.build_dir)

    cmake_run_cmd = [
        "cmake",
        "--build",
        str(build_path),
        "--target",
        target,
        "--config",
        _config.build_type,
    ]
    if _config.verbose:
        cmake_run_cmd.extend(["--verbose"])

    print(f"Running CMake target '{target}' in {build_path}")
    try:
        result = subprocess.run(
            cmake_run_cmd, check=True, capture_output=True, text=True
        )
        print(f"CMake target '{target}' completed successfully")
        if result.stdout:
            print(f"Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running CMake target '{target}':\n{e.stderr}")
        raise


def run(
    executable: str,
    args: Optional[List[str]] = None,
    env: Optional[Dict[str, str]] = None,
) -> Optional[subprocess.CompletedProcess]:
    build_path = Path(_config.build_dir)
    executable_path = build_path / executable

    if os.name == "nt" and not executable_path.suffix:
        executable_path = executable_path.with_suffix(".exe")

    if not executable_path.exists():
        raise FileNotFoundError(f"Executable not found: {executable_path}")

    command = [str(executable_path)]
    if args:
        command.extend(args)

    print(f"Running '{executable_path}'...")
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
        print(f"Permission denied: Unable to execute '{executable_path}'")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

    print("--- End of output ---")
    print(f"Return code: {result.returncode}")

    return result
