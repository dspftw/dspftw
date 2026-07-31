#!/usr/bin/env python3
"""
Display information about the current DSPFTW Python environment.

Useful when reporting bugs, verifying installations, and
checking the software environment used for DSPFTW.

Examples
--------
    python3 scripts/show_environment.py
    python3 scripts/show_environment.py --numpy-config
"""

from __future__ import annotations

import argparse
import importlib
import os
import platform
import sys
from importlib.metadata import PackageNotFoundError, version


PACKAGES = [
    ("dspftw", "dspftw"),
    ("NumPy", "numpy"),
    ("SciPy", "scipy"),
    ("pip", "pip"),
    ("tox", "tox"),
]


def package_version(package_name: str) -> str:
    """Return the installed package version or 'NOT INSTALLED'."""
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "NOT INSTALLED"


def module_location(module_name: str) -> str:
    """Return the module filename or 'NOT IMPORTABLE'."""
    try:
        module = importlib.import_module(module_name)
        return getattr(module, "__file__", "(built-in)")
    except ImportError:
        return "NOT IMPORTABLE"


def print_section(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display information about the current DSPFTW environment."
    )
    parser.add_argument(
        "--numpy-config",
        action="store_true",
        help="Display detailed NumPy build configuration.",
    )

    args = parser.parse_args()

    print("DSPFTW Environment")
    print("==================")

    #
    # DSPFTW
    #
    print_section("DSPFTW")
    print(f"Version          : {package_version('dspftw')}")
    print(f"Location         : {module_location('dspftw')}")

    #
    # Python
    #
    print_section("Python")
    print(f"Executable       : {sys.executable}")
    print(f"Version          : {platform.python_version()}")
    print(f"Implementation   : {platform.python_implementation()}")
    print(f"Compiler         : {platform.python_compiler()}")

    #
    # Platform
    #
    print_section("Platform")
    print(f"Operating System : {platform.system()}")
    print(f"Release          : {platform.release()}")
    print(f"Machine          : {platform.machine()}")
    print(f"Processor        : {platform.processor()}")
    print(f"Architecture     : {platform.architecture()[0]}")

    #
    # Environment
    #
    print_section("Environment")
    print(f"Virtual Env      : {sys.prefix != sys.base_prefix}")
    print(f"sys.prefix       : {sys.prefix}")
    print(f"sys.base_prefix  : {sys.base_prefix}")
    print(f"TOX_ENV_NAME     : {os.environ.get('TOX_ENV_NAME', '(not running under tox)')}")

    #
    # Installed packages
    #
    print_section("Installed Packages")

    width = max(len(name) for name, _ in PACKAGES)

    for display_name, package_name in PACKAGES:
        print(f"{display_name:<{width}} : {package_version(package_name)}")

    #
    # Optional NumPy build information
    #
    if args.numpy_config:
        print_section("NumPy Configuration")

        try:
            numpy = importlib.import_module("numpy")
            numpy.show_config()
        except ImportError:
            print("NumPy is not installed.")


if __name__ == "__main__":
    main()
