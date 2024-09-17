from functools import cached_property
from pathlib import Path

import requests

from ..gh import GHConnector, Asset
from ._models import ProgressCallback


class Fetcher:
    def __init__(
        self, gh_connector: GHConnector, owner_repo: str, tag: str, asset_name: str
    ):
        self._conn = gh_connector
        self._owner_repo = owner_repo
        self._tag = tag
        self._asset_name = asset_name

    def fetch(self, progress: ProgressCallback):
        url = self._asset["browser_download_url"]

        with self._file_path.open("wb") as f:
            resp = requests.get(url, stream=True)
            bytes_done = 0
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk is None:
                    continue

                f.write(chunk)
                f.flush()

                bytes_done += len(chunk)
                progress(bytes_done=bytes_done)

        return self._file_path

    @staticmethod
    def _find_asset_by_name(assets: list[Asset], name: str) -> Asset:
        for asset in assets:
            if asset["name"] == name:
                return asset

        raise ValueError(f"Asset {name} not found")

    @property
    def _file_path(self) -> Path:
        return Path(self._asset_name)

    @property
    def bytes_total(self) -> int:
        return self._asset["size"]

    @cached_property
    def _asset(self) -> Asset:
        release = self._conn.get_release(owner_repo=self._owner_repo, tag=self._tag)
        asset = self._find_asset_by_name(release["assets"], self._asset_name)
        return asset
