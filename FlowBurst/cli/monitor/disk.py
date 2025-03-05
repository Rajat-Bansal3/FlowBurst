import psutil

def check_disk(disk_thresh: float) -> dict:
    """
    Check if disk usage exceeds the threshold.

    Args:
        disk_thresh (float): Percentage of max allowed disk usage.

    Returns:
        dict: Contains total, used, free disk space (GiB), current usage percentage, and breach status.
    """
    disk = psutil.disk_usage('/')
    current_disk_usage = round(disk.percent, 2)  
    is_Exhuasted = current_disk_usage > disk_thresh

    result = {
        "Total_GiB": round(disk.total / (1024 ** 3), 2),
        "Used_GiB": round(disk.used / (1024 ** 3), 2),
        "Free_GiB": round(disk.free / (1024 ** 3), 2),
        "Percent_Used": current_disk_usage,
        "Disk_Exhausted": is_Exhuasted
    }

    return result
