# tests/test_calculations.py

# We need to import the function we want to test.
# It doesn't exist yet, but we'll create it soon.
from core_logic.calculations import calculate_volume

def test_calculate_volume_positive_dimensions():
    """
    Tests the volume calculation for a standard rectangular prism
    with positive, non-zero dimensions.
    """
    # Test Case 1: Simple integers
    assert calculate_volume(length=2, width=3, height=4) == 24

    # Test Case 2: Using floating-point numbers
    assert calculate_volume(length=2.5, width=1.5, height=2.0) == 7.5

    # Test Case 3: A "long" beam
    assert calculate_volume(length=10, width=0.5, height=0.5) == 2.5