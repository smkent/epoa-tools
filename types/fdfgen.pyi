from typing import Iterable, Optional, Tuple

def forge_fdf(
    pdf_form_url: Optional[str] = None,
    fdf_data_strings: Iterable[Tuple[str, str]] = [],
    fdf_data_names: Iterable[Tuple[str, str]] = [],
    fields_hidden: Iterable[str] = [],
    fields_readonly: Iterable[str] = [],
    checkbox_checked_name: bytes = b"Yes",
) -> bytes:
    pass
