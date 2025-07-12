# core_logic/calculations.py

# Add this import at the top of the file
from .materials import DRY_VOLUME_FACTOR, CEMENT_BAG_VOLUME_CUBIC_METERS


class BuildingProject:
    def __init__(self, mix_ratio: str):
        if not self._is_valid_ratio(mix_ratio): # A helper for validation
            raise ValueError("Invalid mix_ratio. Must be 'c:s:g' format.")
        self.mix_ratio = mix_ratio
        self.elements = [] # A list to store all concrete elements
        self.deductions = [] # A list for openings etc.

    def add_element(self, element_type: str, quantity: int, dimensions: dict):
        # dimensions will be a dict like {'length': l, 'width': w, 'height': h}
        volume = self._calculate_element_volume(dimensions)
        self.elements.append({
            "type": element_type,
            "quantity": quantity,
            "dimensions": dimensions,
            "total_volume": volume * quantity
        })

    def add_deduction(self, deduction_type: str, quantity: int, dimensions: dict):
        # For openings, etc.
        volume = self._calculate_element_volume(dimensions)
        self.deductions.append({
            "type": deduction_type,
            "quantity": quantity,
            "dimensions": dimensions,
            "total_volume": volume * quantity
        })
        
    def calculate_total_net_volume(self) -> float:
        gross_volume = sum(el['total_volume'] for el in self.elements)
        total_deductions = sum(d['total_volume'] for d in self.deductions)
        net_volume = gross_volume - total_deductions
        return max(0, net_volume) # Ensure volume isn't negative

    def calculate_total_materials(self) -> dict:
        net_volume = self.calculate_total_net_volume()
        # Here we reuse our previously written function!
        return calculate_material_quantities(net_volume, self.mix_ratio)

    def _calculate_element_volume(self, dims: dict) -> float:
        # A simple volume calculator, can be expanded later for L-beams, etc.
        return dims.get('length', 0) * dims.get('width', 0) * dims.get('height', 0)

    def _is_valid_ratio(self, ratio_str: str) -> bool:
        parts = ratio_str.split(':')
        return len(parts) == 3 and all(p.replace('.', '', 1).isdigit() for p in parts)



'''def calculate_volume(length: float, width: float, height: float) -> float:
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
'''


def calculate_material_quantities(wet_volume_m3: float, mix_ratio: str) -> dict:
    """
    Calculates the required quantities of cement, sand, and gravel.

    Args:
        wet_volume_m3 (float): The final volume of wet concrete needed in cubic meters.
        mix_ratio (str): The mix ratio of "cement:sand:gravel" as a string.

    Returns:
        dict: A dictionary containing the number of cement bags, and the volume
              of sand and gravel in cubic meters.
    """
    # 1. Parse the mix ratio string into numbers
    try:
        ratio_parts = [float(part) for part in mix_ratio.split(':')]
        if len(ratio_parts) != 3:
            raise ValueError
        cement_ratio, sand_ratio, gravel_ratio = ratio_parts
    except (ValueError, IndexError):
        raise ValueError("Invalid mix_ratio format. Expected 'cement:sand:gravel'.")

    # 2. Calculate the total dry volume required
    dry_volume = wet_volume_m3 * DRY_VOLUME_FACTOR

    # 3. Calculate the volume of each material
    sum_of_ratios = cement_ratio + sand_ratio + gravel_ratio
    
    cement_volume = (cement_ratio / sum_of_ratios) * dry_volume
    sand_volume = (sand_ratio / sum_of_ratios) * dry_volume
    gravel_volume = (gravel_ratio / sum_of_ratios) * dry_volume

    # 4. Convert cement volume to number of bags
    cement_bags = cement_volume / CEMENT_BAG_VOLUME_CUBIC_METERS

    # 5. Return the results in a structured dictionary
    return {
        "cement_bags": cement_bags,
        "sand_cubic_meters": sand_volume,
        "gravel_cubic_meters": gravel_volume,
    }