"""Sheet class

:Example:

```python
from snapsheets.sheet import Sheet

url = "https://docs.google.com/spreadsheets/d/16Sc_UgShNuxMfRnBiFsjmfThE1VfVhJf3jgmxNvFeEI/edit#gid=2015536778"
filename = "sample.csv"
description = "Sample spreadsheet for snapsheets"
datefmt = "%Y"
skip = False

s = Sheet(url=url, filename=filename, description=description, datefmt=datefmt, skip=skip)
s.snapshot()

# (printed to stdout)
# 📣 Sample spreadsheet for snapsheets
# 🤖 Downloaded as sample.csv
# 🚀 Renamed to 2022_sample.csv
```
"""

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

import requests
from loguru import logger


@dataclass
class Sheet:
    """
    A class for single spreadsheet
    """

    url: str
    """URL of Google spreadsheet."""

    description: str
    """Description of the sheet."""

    filename: str
    """Output filename."""

    datefmt: str = "%Y%m%d"
    """Format of datetime prefix for backup filename. (default: "%Y%m%d")"""

    skip: bool = False
    """Set to True if you want to skip. (default: False)"""

    def __post_init__(self) -> None:
        """
        1. Check if the URL is of Google spreadsheet
        1. Check if the URL is shared
        1. Parse export format from the given output filename
        1. Parse key and gid from the given URL
        """
        self.parsed_url = urlparse(self.url)
        self.validate_url()

        if not self.skip:
            p = Path(self.filename)
            self.suffix = p.suffix
            self.fmt = self.get_fmt()

            self.key = self.get_key()
            self.gid = self.get_gid()
            self.export_url = self.get_export_url()

    def validate_url(self) -> None:
        """Validate the provided Google Sheets URL.

        Ensure the URL is a Google Sheets URL.
        - Use urlparse to break down the URL into its components.
        - Check if the netloc (domain) is "docs.google.com".

        Check if the URL is accessible and shared.
        - Use requests.get() to attempt to access the URL.
        - Check if the URL is valid and whether the document is shared.
        - If the URL is invalid or unshared (response.ok is False), log an error and sets self.skip to True.


        """
        parsed_url = self.parsed_url

        # check if the URL domain is Google Sheets
        if parsed_url.netloc not in ["docs.google.com"]:
            msg = f"URL should start with 'https://docs.google.com/' : {self.url}"
            logger.error(msg)
            self.skip = True
            # exit the method since validation failed
            return

        # show warning if the URL is not HTTPS
        if parsed_url.scheme != "https":
            msg = "URL is not using HTTPS. Proceed with caution."
            logger.warning(msg)

        # Try to access the URL to see if it is shared
        try:
            response = requests.get(self.url, timeout=10)
            # if the response is no successful, log and skip
            if not response.ok:
                msg = f"URL might be unshared or inaccessible. Status: {response.status_code} - {response.reason}"
                logger.error(msg)
                self.skip = True
        except requests.exceptions.RequestException as e:
            # Catch network-related errors:
            # ConnectionError
            # Timeout
            # HTTPError
            # TooManyRedirects
            msg = f"Failed to connect to URL: {e}"
            logger.error(msg)
            self.skip = True

    def get_fmt(self) -> str:
        """Parse suffix for export format from given output filename.

        - Available suffix is ``xlsx``, ``ods``, ``csv``, and ``tsv``.
        - ``sys.exit`` when the given suffix does not match above.

        Returns
        -------
        str
            suffix of output filename
        """
        ok = ["xlsx", "ods", "csv", "tsv"]
        fmt = Path(self.filename).suffix.strip(".")
        if fmt not in ok:
            error = f"{fmt} is a wrong format. Select from {ok}."
            logger.error(error)
            sys.exit()
        return fmt

    def get_key(self) -> str:
        """Parse ``key`` (=spreadsheet ID) from given URL.

        Returns
        -------
        str
            spreadsheet ID
        """
        parsed_url = self.parsed_url
        key = parsed_url.path.split("/")[3]
        return key

    def get_gid(self) -> str:
        """Parse ``gid`` (=sheet ID) from given URL

        - Set ``gid=0`` (=Sheet1) if not found.

        Returns
        -------
        str
            sheet ID
        """
        parsed_url = self.parsed_url
        fragments = parsed_url.fragment.split("=")
        if len(fragments) > 1:
            gid = fragments[1]
            return gid
        else:
            return "0"

    def get_export_url(self) -> str:
        """
        Generate export URL from given arguments.

        Returns
        -------
        str
            export URL
        """
        path = f"https://docs.google.com/spreadsheets/d/{self.key}/export"
        query = f"format={self.fmt}"
        if self.gid:
            query += f"&gid={self.gid}"
        url = f"{path}?{query}"
        return url

    def download(self) -> None:
        """Download spreadsheet.

        - Download using ``wget`` command
        - Output filename can be configured with CLI option and config file.
        """
        if self.skip:
            info = f"Skipped downloading {self.filename}."
            logger.info(info)
            return

        cmd = ["wget", "--quiet", "-O", self.filename, self.export_url]
        cmd = [str(c) for c in cmd if c]
        try:
            # check=True to raise an exception automatically.
            # if failed, set self.skip to True
            subprocess.run(cmd, check=True)
            msg = f"🤖 Downloaded as {self.filename}"
            logger.success(msg)
        except subprocess.CalledProcessError as e:
            msg = f"Failed to download the file: {e}"
            logger.error(msg)
            self.skip = True

    def backup(self) -> None:
        """Rename downloaded file

        - Prefix is added to the filename using current datetime.
        - A datetime format of prefix can be configured with CLI option and config file.
        """
        if self.skip:
            info = f"Skipped renaming {self.filename}"
            logger.info(info)
            return

        now = datetime.now().strftime(self.datefmt)
        savef = self.filename
        p = Path(self.filename)
        fname = f"{now}_{p.name}"
        movef = Path(p.parent, fname)
        shutil.move(savef, movef)
        info = f"🚀 Renamed to {movef}"
        logger.success(info)

    def snapshot(self) -> None:
        """Run ``download()`` & ``backup()``"""
        logger.info(f"📣 {self.description}")
        self.download()
        self.backup()
