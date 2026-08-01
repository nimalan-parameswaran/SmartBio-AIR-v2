import time
from datetime import datetime

def format_timestamp(epoch: float) -> str:
    """Converts epoch float timestamp to standard ISO datetime string."""
    return datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamps a numerical value within bounds."""
    return max(min_val, min(max_val, value))
