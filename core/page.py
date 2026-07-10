from dataclasses import dataclass, field

from core.elements import Element


@dataclass
class Page:

    page_number: int

    elements: list[Element] = field(default_factory=list)

    def add(self, element: Element):

        self.elements.append(element)