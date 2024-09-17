import os
import requests

from ._models import Release


class GHConnector:
    def __init__(self, token: str):
        self._token = token

    @classmethod
    def from_env(cls):
        return cls(token=os.environ["FREL_GH_TOKEN"])

    @property
    def headers(self):
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "User-Agent": "python",
        }

    @property
    def base_uri(self):
        return "https://api.github.com"

    def list_releases(
        self, owner_repo: str, n_per_page: int, page: int
    ) -> list[Release]:
        url = f"{self.base_uri}/repos/{owner_repo}/releases"
        resp = requests.get(
            url, headers=self.headers, params={"per_page": n_per_page, "page": page}
        )
        resp.raise_for_status()
        return resp.json()

    def get_release(self, owner_repo: str, tag: str) -> Release:
        url = f"{self.base_uri}/repos/{owner_repo}/releases/tags/{tag}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()
