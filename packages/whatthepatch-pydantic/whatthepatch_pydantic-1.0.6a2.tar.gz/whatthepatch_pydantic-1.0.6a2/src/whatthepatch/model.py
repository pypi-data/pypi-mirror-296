from pydantic import BaseModel
from typing import Optional


class Change(BaseModel):
    old: Optional[int] = None
    new: Optional[int] = None
    line: str
    hunk: int


class Header(BaseModel):
    index_path: Optional[str] = None
    old_path: Optional[str] = None
    old_version: str
    new_path: Optional[str] = None
    new_version: str


class Diff(BaseModel):
    header: Header
    changes: list[Change]
    text: str
