from functools import cached_property
from importlib import resources
from pathlib import Path
from typing import Generator

FORM_FILE = "F700-200-000.pdf"


class Builder:
    @cached_property
    def form_path(self) -> Path:
        print("GET PATH")
        return next(self._get_form_path())

    def _get_form_path(self) -> Generator[Path, None, None]:
        package = "epoa_tools.data"
        try:
            with resources.as_file(  # type: ignore
                resources.files(package).joinpath(FORM_FILE)  # type: ignore
            ) as path:
                yield path
        except AttributeError:
            with resources.path(package, FORM_FILE) as path:
                yield path


def main() -> None:
    b = Builder()
    print(b.form_path)
