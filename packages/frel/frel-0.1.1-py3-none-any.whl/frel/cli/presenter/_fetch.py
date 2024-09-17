from pathlib import Path

import humanize
from rich.progress import Progress, TaskID


class FetchPresenter:
    def __init__(self, progress: Progress, task_id: TaskID):
        self._progress = progress
        self._task_id = task_id

    @classmethod
    def for_asset(cls, asset_name: str, bytes_total: int) -> "FetchPresenter":
        progress = Progress()
        size = humanize.naturalsize(bytes_total)
        task_id = progress.add_task(f"{asset_name} ({size})", total=bytes_total)
        return cls(progress=progress, task_id=task_id)

    def __enter__(self):
        self._progress.__enter__()

    def __exit__(self, *args, **kwargs):
        self._progress.__exit__(*args, **kwargs)

    def callback(self, bytes_done: int):
        self._progress.update(self._task_id, completed=bytes_done)

    @staticmethod
    def show_output_asset_file(path: Path):
        print(f"Asset saved at {path}")
