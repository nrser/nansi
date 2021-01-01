from __future__ import annotations
from typing import *
from abc import ABCMeta, abstractmethod

class Node(metaclass=ABCMeta):
    head: Line

    @abstractmethod
    def each(self) -> Generator[Union[Node, Line], None, None]:
        pass

# https://nginx.org/en/docs/beginners_guide.html#conf_structure

class Comment(Node):
    pass

class Directive:
    pass

class SimpleDirective(Node, Directive):
    pass

class BlockDirectiveStart(Line):
    pass

class BlockDirectiveEnd(Line):
    pass

class BlockDirective(Node, Directive):
    pass
