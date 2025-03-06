from monitor.monitoring_conf import start_monitoring , stop_monitoring
from devContainers.dev_containers_conf import get_environments , use_environments ,show_environments
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
    "environments" : {
        "show" : lambda : show_environments(),
        "use" : lambda : use_environments(),
        "get" : lambda : get_environments() 
    }
}