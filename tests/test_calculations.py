# tests/test_calculations.py

import pytest
# We need to import the function we want to test.
# It doesn't exist yet, but we'll create it soon.
from core_logic.calculations import calculate_volume
from core_logic.calculations import calculate_material_quantities

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


def test_calculate_material_quantities():
    """
    Tests the calculation of cement, sand, and gravel for a given volume
    and mix ratio.
    
    Using a wet volume of 1 m^3 and a mix ratio of 1:2:4.
    """
    # Arrange: Define the inputs
    wet_volume_m3 = 1.0
    mix_ratio = "1:2:4" # Cement:Sand:Gravel

    # Act: Call the function to get the results
    materials = calculate_material_quantities(wet_volume_m3, mix_ratio)

    # Assert: Check if the results are what we expect
    # Expected calculations:
    # Dry Volume = 1.0 * 1.54 = 1.54 m^3
    # Sum of ratios = 1 + 2 + 4 = 7
    # Cement Volume = (1/7) * 1.54 = 0.22 m^3
    # Sand Volume = (2/7) * 1.54 = 0.44 m^3
    # Gravel Volume = (4/7) * 1.54 = 0.88 m^3
    # Cement Bags = 0.22 / 0.0347 = 6.34 bags
    
    assert materials["cement_bags"] == pytest.approx(6.34, abs=0.01)
    assert materials["sand_cubic_meters"] == pytest.approx(0.44)
    assert materials["gravel_cubic_meters"] == pytest.approx(0.88)