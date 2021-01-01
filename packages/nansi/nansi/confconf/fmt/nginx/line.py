from __future__ import annotations
from typing import *
from abc import ABCMeta, abstractmethod
import re
from dataclasses import dataclass

class Line(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def match(cls, src: str) -> Optional[Mapping[str, Any]]:
        pass

    @classmethod
    def from_string(cls, src: str) -> Optional[Line]:
        if props := cls.match(src):
            return cls(**props)
        return None

    prev: Optional[Line] = None
    next: Optional[Line] = None

# https://nginx.org/en/docs/beginners_guide.html#conf_structure

# @dataclass
class Comment(Line):
    RE = re.compile(
        r'(?P<predent>\s+)'
        r'#(?P<indent>\s+)'
        r'(?P<text>.*\S)?'
        r'(\s+)' # or r'(?P<trailing_ws>\s+)' if want to preserve?
    )

    @classmethod
    def match(cls, src: str):
        if match := cls.RE.fullmatch(src):
            return match.groupdict()
        return None

    predent: Optional[str]
    indent: Optional[str]
    text: Optional[str]
    # trailing_ws: Optional[str]

    def __init__(self, predent, indent, text):
        self.predent = predent
        self.indent = indent
        self.text = text

