"""
Project: W03 Water Pressure
Author: Oscar FOnseca
Description: Calculates water pressure through a distribution system including towers, tanks, and various pipe diameters.
Enhancements:
1. Defined constants for gravity, water density, and dynamic viscosity.
2. Added a function to convert kPa to PSI.
3. Updated main to display results in both units.
"""

# Global Constants (Exceeding Requirements)
EARTH_ACCELERATION_OF_GRAVITY = 9.80665
WATER_DENSITY = 998.2
WATER_DYNAMIC_VISCOSITY = 0.0010016

def water_column_height(tower_height, tank_height):
    """Calculate the height of the water column."""
    return tower_height + (3 * tank_height / 4)

def pressure_gain_from_water_height(height):
    """Calculate pressure gain from the height of the water column."""
    return (WATER_DENSITY * EARTH_ACCELERATION_OF_GRAVITY * height) / 1000

def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    """Calculate pressure loss due to friction in a pipe."""
    return (-friction_factor * pipe_length * WATER_DENSITY * (fluid_velocity**2)) / (2000 * pipe_diameter)

def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """Calculate pressure loss from pipe fittings."""
    return (-0.04 * WATER_DENSITY * (fluid_velocity**2) * quantity_fittings) / 2000

def reynolds_number(hydraulic_diameter, fluid_velocity):
    """Calculate the Reynolds number of the flow."""
    return (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / WATER_DYNAMIC_VISCOSITY

def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    """Calculate pressure loss caused by pipe diameter reduction."""
    # Grouping (0.1 + 50/R) is critical for the correct result
    k = (0.1 + 50 / reynolds_number) * (((larger_diameter / smaller_diameter)**4) - 1)
    return (-k * WATER_DENSITY * (fluid_velocity**2)) / 2000

def convert_kpa_to_psi(kpa):
    """Convert pressure from kilopascals to pounds per square inch."""
    return kpa * 0.1450377377

def main():
    """Get user input and calculate the total pressure at the house."""
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_fittings = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))

    velocity = 1.65
    friction = 0.013
    diameter1 = 0.28687
    diameter2 = 0.048692

    # Step-by-step calculations
    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)

    # Supply pipe loss
    loss = pressure_loss_from_pipe(diameter1, length1, friction, velocity)
    pressure += loss

    # Fittings loss
    loss = pressure_loss_from_fittings(velocity, quantity_fittings)
    pressure += loss

    # Reduction loss
    reynolds = reynolds_number(diameter1, velocity)
    loss = pressure_loss_from_pipe_reduction(diameter1, velocity, reynolds, diameter2)
    pressure += loss

    # House pipe loss
    loss = pressure_loss_from_pipe(diameter2, length2, friction, velocity)
    pressure += loss

    # Final Output
    print(f"Pressure at house: {pressure:.1f} kilopascals")
    print(f"Pressure at house: {convert_kpa_to_psi(pressure):.1f} pounds per square inch")

if __name__ == "__main__":
    main()