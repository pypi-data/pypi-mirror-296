"""
Utility functions.

This module contains utility functions to read the configuration, download the CLI and determine
the various paths.
"""

import os
import platform
from pathlib import Path
from typing import Tuple, Union

from django.conf import settings


class Config:
    """Configuration for the Tailwind CSS CLI."""

    default_src_repo = "tailwindlabs/tailwindcss"

    @property
    def tailwind_version(self) -> str:
        return getattr(settings, "TAILWIND_CLI_VERSION", "3.4.11")

    @property
    def cli_path(self) -> Union[Path, None]:
        p = getattr(settings, "TAILWIND_CLI_PATH", "~/.local/bin/")
        if p is None:
            return p
        return Path(p).expanduser()

    @property
    def automatic_download(self) -> bool:
        return bool(getattr(settings, "TAILWIND_CLI_AUTOMATIC_DOWNLOAD", True))

    @property
    def src_css(self) -> Union[str, None]:
        return getattr(settings, "TAILWIND_CLI_SRC_CSS", None)

    @property
    def dist_css(self) -> str:
        return getattr(settings, "TAILWIND_CLI_DIST_CSS", "css/tailwind.css")

    @property
    def config_file(self) -> str:
        return getattr(settings, "TAILWIND_CLI_CONFIG_FILE", "tailwind.config.js")

    @property
    def src_repo(self) -> str:
        return getattr(settings, "TAILWIND_CLI_SRC_REPO", self.default_src_repo)

    @property
    def asset_name(self) -> str:
        return getattr(settings, "TAILWIND_CLI_ASSET_NAME", "tailwindcss")

    @staticmethod
    def validate_settings() -> None:
        """Validate the settings."""
        if settings.STATICFILES_DIRS is None or len(settings.STATICFILES_DIRS) == 0:
            msg = "STATICFILES_DIRS is empty. Please add a path to your static files."
            raise ValueError(msg)

    @staticmethod
    def get_system_and_machine() -> Tuple[str, str]:
        """Get the system and machine name."""
        system = platform.system().lower()
        if system == "darwin":
            system = "macos"

        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            machine = "x64"
        elif machine == "aarch64":
            machine = "arm64"

        return system, machine

    def get_download_url(self) -> str:
        """Get the download url for the Tailwind CSS CLI."""
        system, machine = self.get_system_and_machine()
        extension = ".exe" if system == "windows" else ""
        return (
            f"https://github.com/{self.src_repo}/releases/download/"
            f"v{self.tailwind_version}/{self.asset_name}-{system}-{machine}{extension}"
        )

    def get_full_cli_path(self) -> Path:
        """Get path to the Tailwind CSS CLI."""

        # If Tailwind CSS CLI path points to an existing executable use is.
        if self.cli_path and self.cli_path.exists() and self.cli_path.is_file() and os.access(self.cli_path, os.X_OK):
            return self.cli_path

        # Otherwise try to calculate the full cli path as usual.
        system, machine = self.get_system_and_machine()
        extension = ".exe" if system == "windows" else ""
        executable_name = f"tailwindcss-{system}-{machine}-{self.tailwind_version}{extension}"
        if self.cli_path is None:
            return Path(settings.BASE_DIR) / executable_name
        else:
            return self.cli_path / executable_name

    def get_full_src_css_path(self) -> Path:
        """Get path to the source css."""
        if self.src_css is None:
            msg = "No source CSS file specified. Please set TAILWIND_SRC_CSS in your settings."
            raise ValueError(msg)
        return Path(settings.BASE_DIR) / self.src_css

    def get_full_dist_css_path(self) -> Path:
        """Get path to the compiled css."""
        if settings.STATICFILES_DIRS is None or len(settings.STATICFILES_DIRS) == 0:
            msg = "STATICFILES_DIRS is empty. Please add a path to your static files."
            raise ValueError(msg)

        return Path(settings.STATICFILES_DIRS[0]) / self.dist_css

    def get_full_config_file_path(self) -> Path:
        """Get path to the tailwind.config.js file."""
        return Path(settings.BASE_DIR) / self.config_file
