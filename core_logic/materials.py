# core_logic/materials.py

# Standard factor to convert wet volume of concrete to dry volume of materials
DRY_VOLUME_FACTOR = 1.54

# Standard density of cement is ~1440 kg/m^3
# A standard bag of cement is 50kg.
# Volume of one 50kg bag of cement = 50 / 1440 = 0.0347 m^3
CEMENT_BAG_VOLUME_CUBIC_METERS = 0.0347