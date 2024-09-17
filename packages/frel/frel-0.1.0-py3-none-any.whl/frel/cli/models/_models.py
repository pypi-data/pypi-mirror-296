from typing import TypedDict


class ReleaseShort(TypedDict):
    name: str
    tag_name: str
    published_at: str
    n_assets: int


class ReleaseDetailed(TypedDict):
    name: str
    tag_name: str
    published_at: str
    draft: bool
    prerelease: bool
    assets: list["Asset"]
    n_assets: int
    body: str


class Asset(TypedDict):
    id: int
    name: str
    size: int
