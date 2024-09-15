from pathlib import Path

from xdg_base_dirs import xdg_config_home, xdg_data_home


def _elia_directory(root: Path) -> Path:
    directory = root / "elia"
    directory.mkdir(exist_ok=True, parents=True)
    return directory


def data_directory() -> Path:
    """Return (possibly creating) the application data directory."""
    return _elia_directory(xdg_data_home())


def config_directory() -> Path:
    """Return (possibly creating) the application config directory."""
    return _elia_directory(xdg_config_home())


def config_file() -> Path:
    return config_directory() / "config.toml"


def theme_directory() -> Path:
    """Return (possibly creating) the themes directory."""
    theme_dir = data_directory() / "themes"
    theme_dir.mkdir(exist_ok=True, parents=True)
    return theme_dir
