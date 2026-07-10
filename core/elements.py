from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------
# Base Element
# ---------------------------------------------------------

@dataclass
class Element:
    type: str
    bbox: List[float]


# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

@dataclass
class Title(Element):
    text: str
    level: int


# ---------------------------------------------------------
# Paragraph
# ---------------------------------------------------------

@dataclass
class Paragraph(Element):
    text: str


# ---------------------------------------------------------
# Table
# ---------------------------------------------------------

@dataclass
class Table(Element):
    html: str


# ---------------------------------------------------------
# Image
# ---------------------------------------------------------

@dataclass
class Image(Element):
    path: str