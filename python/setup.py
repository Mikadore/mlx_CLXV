"""Build the Linux/XCB Python package and its native MiniLibX library."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.dist import Distribution


PYTHON_DIR = Path(__file__).resolve().parent
REPO_ROOT = PYTHON_DIR.parent
PACKAGE_DIR = PYTHON_DIR / "src" / "mlx"

# setuptools reads this dynamic version while loading pyproject.toml, before
# any build command runs. The repository keeps the canonical version at root.
shutil.copyfile(REPO_ROOT / "version", PYTHON_DIR / "version")


def pkg_config(*args: str) -> str:
    """Return pkg-config output, with an actionable missing-dependency error."""
    try:
        result = subprocess.run(
            ["pkg-config", *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("pkg-config is required to build mlx") from exc
    except subprocess.CalledProcessError as exc:
        packages = "xcb vulkan"
        raise RuntimeError(
            f"pkg-config could not find required modules ({packages}); "
            "install their development packages first"
        ) from exc
    return result.stdout.strip()


class BuildPy(build_py):
    """Compile libmlx and stage its files before setuptools packages them."""

    def run(self) -> None:
        cflags = pkg_config("--cflags", "xcb", "vulkan")
        ldflags = pkg_config("--libs", "xcb", "vulkan")

        env = os.environ.copy()
        env["CFLAGS"] = " ".join(filter(None, [env.get("CFLAGS", ""), cflags]))
        env["LDFLAGS"] = " ".join(filter(None, [env.get("LDFLAGS", ""), ldflags]))
        subprocess.run(
            ["make", "BACKEND=xcb", "config", "libmlx.so"],
            cwd=REPO_ROOT,
            env=env,
            check=True,
        )

        shutil.copyfile(REPO_ROOT / "libmlx.so", PACKAGE_DIR / "libmlx.so")
        docs_dir = PACKAGE_DIR / "docs"
        docs_dir.mkdir(exist_ok=True)
        shutil.copyfile(REPO_ROOT / "src" / "mlx.h", docs_dir / "mlx.h")
        for manual in (REPO_ROOT / "man" / "man3").glob("*"):
            shutil.copyfile(manual, docs_dir / manual.name)

        super().run()


class BinaryDistribution(Distribution):
    """Tell wheel builders this package contains a platform-specific library."""

    def has_ext_modules(self) -> bool:
        return True


setup(
    cmdclass={"build_py": BuildPy},
    distclass=BinaryDistribution,
)
