import mappings
import re

def add_stage(data_values):
    val = mappings.single_val(data_values)
    if val:
        return f"Stage {val}"
    else:
        return "Not available"


def fix_systemic(data_values):
    return ["Systemic therapy"]

