import pytest
from src.utils import capture_image

def test_capture_image():
    result = capture_image()
    assert result is None  # Since no camera is available in testing
