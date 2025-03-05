import psutil

def check_cpu(cpu_threshold, load_threshold):
    """
    Check if CPU usage or load average exceeds the threshold.
    Args:
        cpu_threshold (int): CPU usage threshold.
        load_threshold (int): Load average threshold.
    Returns:
        dict: Contains current CPU usage, load averages, and breach status.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    load_avg = psutil.getloadavg()
    cpu_cores = psutil.cpu_count()

    load_percent = [load / cpu_cores * 100 for load in load_avg]
    avg_load_percent = sum(load_percent) / len(load_percent)

    cpu_breached = cpu_usage > cpu_threshold
    load_breached = avg_load_percent > load_threshold

    result = {
        "cpu_usage": cpu_usage,
        "load_avg": load_avg,
        "load_percent": load_percent,
        "avg_load_percent": avg_load_percent,
        "cpu_breached": cpu_breached,
        "load_breached": load_breached,
        "breached": cpu_breached or load_breached
    }

    return result