from __future__ import annotations
from typing import Type, Union, Optional, BinaryIO, Tuple
import os

version: str = ...
"""
Represents the version of this module as a string in the format "major.minor.micro".
"""

version_info: Tuple[int, int, int] = ...
"""
Represents the version of this module as a tuple of three integers: (major, minor, micro).
"""

LUNASVG_VERSION: int = ...
"""
Represents the version of the lunasvg library encoded as a single integer.
"""

LUNASVG_VERSION_MAJOR: int = ...
"""
Represents the major version number of the lunasvg library.
"""

LUNASVG_VERSION_MICRO: int = ...
"""
Represents the micro version number of the lunasvg library.
"""

LUNASVG_VERSION_MINOR: int = ...
"""
Represents the minor version number of the lunasvg library.
"""

LUNASVG_VERSION_STRING: str = ...
"""
Represents the version of the lunasvg library as a string in the format "major.minor.micro".
"""

class Bitmap:
    """
    The `Bitmap` class provides an interface for rendering to memory buffers.
    """
    def __init__(self, width: int, height: int) -> None:
        pass
    @classmethod
    def create_for_data(cls, data: memoryview, width: int, height: int, stride: int) -> Bitmap:
        pass
    def data(self) -> memoryview:
        pass
    def width(self) -> int:
        pass
    def height(self) -> int:
        pass
    def stride(self) -> int:
        pass
    def clear(self, color: int) -> None:
        pass
    def write_to_png(self, filename: Union[str, bytes, os.PathLike]) -> None:
        pass
    def write_to_png_stream(self, stream: BinaryIO) -> None:
        pass

class Matrix:
    """
    The `Matrix` class represents a 2D transformation matrix.
    """
    def __init__(self, a: float = 1.0, b: float = 0.0, c: float = 0.0, d: float = 1.0, e: float = 0.0, f: float = 0.0) -> None:
        pass
    def __repr__(self) -> str:
        pass
    def __len__(self) -> int:
        pass
    def __getitem__(self) -> float:
        pass
    def __mul__(self, other: Matrix) -> Matrix:
        pass
    def __imul__(self, other: Matrix) -> Matrix:
        pass
    def __invert__(self) -> Matrix:
        pass
    def multiply(self, other: Matrix) -> Matrix:
        pass
    def translate(self, tx: float, ty: float) -> Matrix:
        pass
    def scale(self, sx: float, sy: float) -> Matrix:
        pass
    def rotate(self, angle: float, tx: float = 0.0, ty: float = 0.0) -> Matrix:
        pass
    def shear(self, shx: float, shy: float) -> Matrix:
        pass
    @classmethod
    def translated(cls, tx: float, ty: float) -> Matrix:
        pass
    @classmethod
    def scaled(cls, sx: float, sy: float) -> Matrix:
        pass
    @classmethod
    def rotated(cls, angle: float, tx: float = 0.0, ty: float = 0.0) -> Matrix:
        pass
    def invert(self) -> Matrix:
        pass
    def inverse(self) -> Matrix:
        pass
    def reset(self) -> None:
        pass
    a: float = ...
    b: float = ...
    c: float = ...
    d: float = ...
    e: float = ...
    f: float = ...

class Box:
    """
    The `Box` class Represents a 2D axis-aligned bounding box.
    """
    def __init__(self, x: float = 0.0, y: float = 0.0, w: float = 0.0, h: float = 1.0) -> None:
        pass
    def __repr__(self) -> str:
        pass
    def __len__(self) -> int:
        pass
    def __getitem__(self) -> float:
        pass
    def transform(self, matrix: Matrix) -> Box:
        pass
    @classmethod
    def transformed(cls, matrix: Matrix) -> Box:
        pass
    x: float = ...
    y: float = ...
    w: float = ...
    h: float = ...

class Element:
    def __eq__(self) -> bool:
        pass
    def __ne__(self) -> bool:
        pass
    def has_attribute(self, name: str) -> bool:
        pass
    def get_attribute(self, name: str) -> str:
        pass
    def set_attribute(self, name: str, value: str) -> str:
        pass
    def render(self, bitmap: Bitmap, matrix: Matrix = ...) -> None:
        pass
    def render_to_bitmap(self, width: int = -1, height: int = -1, background_color: int = 0x00000000) -> Bitmap:
        pass
    def get_local_matrix(self) -> Matrix:
        pass
    def get_global_matrix(self) -> Matrix:
        pass
    def get_local_bounding_box(self) -> Box:
        pass
    def get_global_bounding_box(self) -> Box:
        pass
    def get_bounding_box(self) -> Box:
        pass
    def parent(self) -> Optional[Element]:
        pass
    def document(self) -> Document:
        pass

class Document:
    def __init__(self, filename: Union[str, bytes, os.PathLike]) -> None:
        pass
    @classmethod
    def load_from_data(cls, data: str) -> Document:
        pass
    def width(self) -> float:
        pass
    def height(self) -> float:
        pass
    def bounding_box(self) -> Box:
        pass
    def update_layout(self) -> None:
        pass
    def render(self) -> None:
        pass
    def render_to_bitmap(self, width: int = -1, height: int = -1, background_color: int = 0x00000000) -> None:
        pass
    def get_element_by_id(self, id: str) -> Optional[Element]:
        pass
    def document_element(self) -> Element:
        pass

def add_font_face_from_file(family: str, bold: bool, italic: bool, filename: Union[str, bytes, os.PathLike]) -> None:
    pass
def add_font_face_from_data(family: str, bold: bool, italic: bool, data: memoryview) -> None:
    pass
