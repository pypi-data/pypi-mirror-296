from datetime import datetime
from typing import Sequence

from rich.console import Console
from rich.table import Table
import humanize

from ..models import ReleaseShort, ReleaseDetailed, Asset


class ReleasePresenter:
    def __init__(self):
        self._console = Console()

    def show_releases(self, owner_repo: str, releases: Sequence[ReleaseShort]):
        table = Table(title=f"Releases in {owner_repo}")
        table.add_column("Name")
        table.add_column("Tag")
        table.add_column("Published")
        table.add_column("Assets")

        now = datetime.now().astimezone()

        for rel in releases:
            published_at = datetime.fromisoformat(rel["published_at"])
            since_published = now - published_at

            table.add_row(
                rel["name"],
                rel["tag_name"],
                humanize.naturaltime(since_published),
                str(rel["n_assets"]),
            )

        self._console.print(table)

    def show_release(self, owner_repo: str, release: ReleaseDetailed):
        self._show_release_details(owner_repo=owner_repo, release=release)
        self._console.print()
        self._show_assets(assets=release["assets"])

    def _show_release_details(self, owner_repo: str, release: ReleaseDetailed):
        table = Table(
            show_edge=False,
            show_header=False,
        )
        table.add_column(justify="right")
        table.add_column()

        table.add_row("Repo", owner_repo)
        table.add_row("Tag", release["tag_name"])
        table.add_row("Release Name", release["name"])
        table.add_row("Published At", release["published_at"])
        table.add_row("Draft?", self._format_bool(release["draft"]))
        table.add_row("Prelease?", self._format_bool(release["prerelease"]))
        table.add_row("# of Assets", str(release["n_assets"]))
        table.add_row("Description", str(release["body"]))

        self._console.print(table)

    @staticmethod
    def _format_bool(value: bool) -> str:
        if value:
            return "yes"
        else:
            return "no"

    def _show_assets(self, assets: list[Asset]):
        table = Table(title="Assets")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Size")

        for asset in assets:
            table.add_row(
                str(asset["id"]),
                asset["name"],
                humanize.naturalsize(asset["size"]),
            )

        self._console.print(table)
