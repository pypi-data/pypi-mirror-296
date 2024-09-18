from abc import ABC

from pydantic import BaseModel


class BoundingBox(BaseModel):
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    page: int


class Attributes(BaseModel, ABC):
    pass


class DocumentAttributes(Attributes):
    pass


class PageAttributes(Attributes):
    page: int


class TextAttributes(Attributes):
    bounding_box: list[BoundingBox] = []
