"""Adapters tests."""


from __future__ import annotations

import os
import sys

ROOT_PATH: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

from simpml.tabular.adapters_pool import ManipulateAdapter

def test_manipulate_adapter() -> None:
    """Test the `ManipulateAdapter` class."""
