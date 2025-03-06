from monitor.monitoring_conf import start_monitoring , stop_monitoring
import pathlib

curr_dir = pathlib.Path(__file__).parent

default_config_file = f"{curr_dir.resolve()}/config.json"
defualt_log_dir = f"{curr_dir.parent.parent.resolve()}/logs/sysmon/flow_burst_sysmon.log"

Services = {
    "monitoring": {
        "start": lambda : start_monitoring(default_config_file , defualt_log_dir),
        "stop": lambda : stop_monitoring(),
        "status": lambda: print("📊 Monitoring is running"),
    },
    "logging": {
        "start": lambda: print("✅ Logging service started"),
        "stop": lambda: print("🛑 Logging service stopped"),
        "status": lambda: print("📜 Logging is active"),
    },
    "network": {
        "start": lambda: print("✅ Network service initialized"),
        "stop": lambda: print("🛑 Network service shut down"),
        "status": lambda: print("🌐 Network is operational"),
    },
}