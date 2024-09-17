from typing import TypedDict


class Release(TypedDict):
    id: int
    name: str
    tag_name: str
    body: str
    published_at: str
    draft: bool
    prerelease: bool
    assets: list["Asset"]


class Asset(TypedDict):
    id: int
    name: str
    label: str
    size: int
    browser_download_url: str
