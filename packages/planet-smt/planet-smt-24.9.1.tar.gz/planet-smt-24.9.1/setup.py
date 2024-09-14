"""Setup script for the Area Monitoring Orchestrator."""

import os
import re

from setuptools import find_packages, setup


def get_version() -> str:
    """Extracts data from the __init__ file."""
    with open(os.path.join(os.path.dirname(__file__), "..", "__init__.py"), encoding="utf-8") as f:
        return re.search(r'__version__\s*=\s*"(.*?)"', f.read()).group(1)  # type: ignore[union-attr]


def get_description() -> str:
    """Extracts readme from the root file."""
    with open(os.path.join(os.path.dirname(__file__), "..", "..", "README.md"), encoding="utf-8") as f:
        return f.read()


setup(
    name="planet-smt",
    python_requires=">=3.11",
    version=get_version(),
    long_description="The `planet-smt` package is a Python-based SDK for Planet's `Signals & Markers Toolkit` (SMT). You can find the full documentation, data specification, and a user guide at the [SMT Community GitLab repository](https://gitext.sinergise.com/area-monitoring/community). If you need to contact us, please refer to the [Contact Us](#contact-us) section.",
    description="SDK of Signals and Markers Toolkit",
    author="Planet Labs",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pydantic<2.0", "httpx", "backoff"],
)
