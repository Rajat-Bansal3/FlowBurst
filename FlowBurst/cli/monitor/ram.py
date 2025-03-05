import psutil

def check_memory(memory_thresh):
    """
    Check if memory usage exceeds a given percentage threshold.

    Args:
        memory_thresh (float): Maximum allowed memory usage percentage.

    Returns:
        dict: Contains total, available, used memory (GiB), current usage percentage, and breach status.
    """
    mem = psutil.virtual_memory()

    memory_breached = mem.percent > memory_thresh

    result = {
        "total_GiB": round(mem.total / 1024**3, 2),
        "available_GiB": round(mem.available / 1024**3, 2),
        "used_GiB": round(mem.used / 1024**3, 2),
        "free_GiB": round(mem.free / 1024**3, 2),
        "percent_used": round(mem.percent, 2),
        "memory_breached": memory_breached
    }

    return result
