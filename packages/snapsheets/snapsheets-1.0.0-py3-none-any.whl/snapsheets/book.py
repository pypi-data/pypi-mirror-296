"""

```python
from snapsheets.book import Book

book = Book("config.toml")
book.snapshots()

# 📣 Sample spreadsheet for snapsheets. (%Y%m%d)
# 🤖 Downloaded sample1.csv
# 🚀 Rnamed sample1.csv to 20220602_sample1.csv
# 📣 Sample spreadsheet for snapsheets. (%Y%m)
# 🤖 Downloaded sample2.csv
# 🚀 Rnamed sample2.csv to 202206_sample2.csv
```
"""

import sys
from dataclasses import dataclass
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import yaml
from loguru import logger

from snapsheets.sheet import Sheet


@dataclass
class Book:
    """
    A class for collection of spreadsheets
    """

    fname: str = "config.toml"
    """config filename or directory"""

    def __post_init__(self) -> None:
        p = Path(self.fname)
        if not p.exists():
            error = "Unable to locate config file/directory."
            error += f"Perhaps you need to create a new config file/directory. : {p}"
            logger.error(error)
            sys.exit()

        self.fnames = self.get_fnames()
        self.config = self.load_config()
        self.sheets = self.get_sheets()

    def get_fnames(self) -> list[Path]:
        """Get list of configuration files.

        Returns
        -------
        list[Path]
            list of configuration files
        """
        p = Path(self.fname)
        logger.info(f"Load config : {p}")

        if p.is_file():
            return [p]

        fnames = sorted(p.glob("*.toml"))
        return fnames

    def load_config(self) -> dict:
        """Load configuration from files.

        - Supported format: ``toml``, ``.yml``, and ``.yaml``

        Returns
        -------
        dict
            configuration in dict-object
        """
        config = {}
        for fname in self.fnames:
            suffix = fname.suffix
            if suffix in [".toml"]:
                _config = self.load_config_toml(fname)
            elif suffix in [".yml", ".yaml"]:
                _config = self.load_config_yaml(fname)
            else:
                error = f"Wrong config format. '{suffix}' not supported."
                logger.error(error)
                sys.exit()
            config.update(_config)
        return config

    def load_config_toml(self, fname: Path) -> dict:
        """Load configurations from TOML format.

        Parameters
        ----------
        fname : Path
            config filename

        Returns
        -------
        dict
            config as dict-object
        """
        with fname.open("rb") as f:
            config = tomllib.load(f)
        return config

    def load_config_yaml(self, fname: Path) -> dict:
        """
        Load configurations from YAML format.

        Parameters
        ----------
        fname : Path
            config filename

        Returns
        -------
        dict
            config as dict-object
        """
        with fname.open("r") as f:
            config = yaml.safe_load(f)
        return config

    def get_sheets(self) -> list[Sheet]:
        """
        Get list of sheets in configuration.

        Returns
        -------
        list[Sheet]
            list of Sheet objects
        """
        sheets = self.config.get("sheets")
        if sheets is None:
            return []

        sheets = []
        for sheet in self.config["sheets"]:
            url = sheet.get("url")
            filename = sheet.get("filename")
            desc = sheet.get("desc")
            datefmt = sheet.get("datefmt")
            skip = sheet.get("skip")
            _sheet = Sheet(
                url=url,
                filename=filename,
                description=desc,
                datefmt=datefmt,
                skip=skip,
            )
            sheets.append(_sheet)
        return sheets

    def snapshots(self) -> None:
        """
        Take a snapshot of sheets.
        """

        for sheet in self.sheets:
            sheet.snapshot()
