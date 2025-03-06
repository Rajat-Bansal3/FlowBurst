import time
import json
from pathlib import Path
from threading import Thread, Event
from monitor.cpu import check_cpu
from monitor.ram import check_memory
from monitor.disk import check_disk

monitoring_active = Event()
monitoring_active.set()


def monitor_system(cpu_threshold, load_threshold, ram_threshold, disk_threshold, log_path, freq=5):
    """
    Continuously monitor CPU, RAM, and disk usage.
    """
    Path(log_path).touch(exist_ok=True)

    while True:
        cpu_status = check_cpu(cpu_threshold, load_threshold)
        ram_status = check_memory(ram_threshold)
        disk_status = check_disk(disk_threshold)

        log_entry = {
            "cpu_status": cpu_status,
            "ram_status": ram_status,
            "disk_status": disk_status,
            "timestamp": time.time()  
        }

        # Log the status to the specified log file in JSON format
        with open(log_path, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")

        time.sleep(freq)

def start_monitoring(config_path, log_file):
    """
    Start the monitoring loop in a separate thread.
    """
    try:
        with open(f"{config_path}", "r", encoding="utf-8") as file:
            config = json.load(file)

        # DEFAULTS: change if u want 
        cpu_threshold = config.get("cpu_thresh", 80)
        cpu_load_threshold = config.get("cpu_load_thresh", 80)
        ram_threshold = config.get("ram_thresh", 75)
        disk_threshold = config.get("disk_thresh", 90)

        monitor_thread = Thread(
            target=monitor_system,
            args=(cpu_threshold, cpu_load_threshold, ram_threshold, disk_threshold, log_file, 5),
            # daemon=True
        )
        monitor_thread.start()
        print("Monitoring started. Logs are being written to:", log_file)

    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {config_path}")

def stop_monitoring():
    """
    Stop the monitoring loop.
    """
    monitoring_active.clear()  
    print("Monitoring stopped.")

