import re
from datetime import datetime
from typing import Optional, Sequence

import pdf_redactor  # type: ignore


class Redactor:
    def __init__(self, words: Optional[Sequence[str]] = None):
        self.words = words or []

    def redact(self, input_file: str, output_file: str) -> None:
        with open(input_file, "rb") as rf, open(output_file, "wb") as wf:
            options = pdf_redactor.RedactorOptions()
            options.input_stream = rf
            options.output_stream = wf
            options.metadata_filters = {
                "Producer": [lambda value: None],
                "CreationDate": [lambda value: datetime.utcnow()],
                "DEFAULT": [lambda value: None],
            }
            options.xmp_filters = [lambda xml: None]
            options.content_filters = [
                (
                    re.compile(r"([\w\.@]+" + word + r"[\w\.@]+)"),
                    lambda _: "(redacted)",
                )
                for word in self.words
            ]
            options.link_filters = [self._redact_link]
            pdf_redactor.redactor(options)

    def _redact_link(self, href: str, annotation: str) -> str:
        if href.startswith("mailto:"):
            for word in self.words:
                if word in href:
                    return "mailto:(redacted)"
        return href
