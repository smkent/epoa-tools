from typing import Iterable, Optional, Tuple

def slugify(
    text: str,
    entities: bool = True,
    decimal: bool = True,
    hexadecimal: bool = True,
    max_length: int = 0,
    word_boundary: bool = False,
    separator: str = "-",
    save_order: bool = False,
    stopwords: Iterable[str] = (),
    regex_pattern: Optional[str] = None,
    lowercase: bool = True,
    replacements: Iterable[Tuple[str, str]] = (),
    allow_unicode: bool = False,
) -> str:
    pass
