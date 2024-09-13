def convert_units(value, from_unit, to_unit):
    """Convert value from one unit to another."""
    conversion_factors = {
        ("meters", "feet"): 3.28084,
        ("feet", "meters"): 1 / 3.28084,
    }
    factor = conversion_factors.get((from_unit.lower(), to_unit.lower()))
    if factor:
        return value * factor
    else:
        raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported.")


def validate_config(config, required_keys):
    """Validate that all required keys are present in the config."""
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ValueError(
            f"Missing required configuration keys: {', '.join(missing_keys)}"
        )
