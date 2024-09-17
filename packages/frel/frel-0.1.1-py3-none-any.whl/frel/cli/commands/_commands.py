import click
from ...gh import GHConnector
from ...fetch import Fetcher
from ..presenter import ReleasePresenter, FetchPresenter
from ..models import (
    ReleaseShort as ReleaseShortView,
    ReleaseDetailed as ReleaseDetailedView,
)


@click.group()
def entrypoint():
    pass


@click.argument("owner_repo")
@entrypoint.command(name="list")
def list_full(owner_repo: str):
    conn = GHConnector.from_env()
    releases = conn.list_releases(
        owner_repo=owner_repo,
        n_per_page=10,
        page=1,
    )

    presenter = ReleasePresenter()
    release_views: list[ReleaseShortView] = [
        {
            "name": r["name"],
            "tag_name": r["tag_name"],
            "n_assets": len(r["assets"]),
            "published_at": r["published_at"],
        }
        for r in releases
    ]
    presenter.show_releases(owner_repo=owner_repo, releases=release_views)


@entrypoint.command(name="l")
def list_alias(*args, **kwargs):
    return list_full(*args, **kwargs)


@click.argument("tag")
@click.argument("owner_repo")
@entrypoint.command(name="show")
def show_release_full(owner_repo: str, tag: str):
    conn = GHConnector.from_env()
    release = conn.get_release(owner_repo=owner_repo, tag=tag)

    presenter = ReleasePresenter()
    release_view: ReleaseDetailedView = {
        "name": release["name"],
        "tag_name": release["tag_name"],
        "published_at": release["published_at"],
        "draft": release["draft"],
        "prerelease": release["prerelease"],
        "assets": [
            {
                "id": a["id"],
                "name": a["name"],
                "size": a["size"],
            }
            for a in release["assets"]
        ],
        "n_assets": len(release["assets"]),
        "body": release["body"],
    }
    presenter.show_release(owner_repo=owner_repo, release=release_view)


@entrypoint.command(name="s")
def show_alias(*args, **kwargs):
    return show_release_full(*args, **kwargs)


@click.argument("asset")
@click.argument("tag")
@click.argument("owner_repo")
@entrypoint.command()
def fetch(owner_repo: str, tag: str, asset: str):
    conn = GHConnector.from_env()
    fetcher = Fetcher(
        gh_connector=conn, owner_repo=owner_repo, tag=tag, asset_name=asset
    )

    presenter = FetchPresenter.for_asset(
        asset_name=asset, bytes_total=fetcher.bytes_total
    )

    with presenter:
        path = fetcher.fetch(progress=presenter.callback)

    presenter.show_output_asset_file(path)
