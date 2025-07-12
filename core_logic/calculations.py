# core_logic/calculations.py

def calculate_volume(length: float, width: float, height: float) -> float:
    """
    Calculates the volume of a rectangular prism.

    Args:
        length (float): The length of the element.
        width (float): The width of the element.
        height (float): The height or depth of the element.

    Returns:
        float: The calculated volume.
    """
    # Basic validation to prevent non-physical dimensions
    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError("Dimensions must be positive non-zero values.")

    return length * width * height