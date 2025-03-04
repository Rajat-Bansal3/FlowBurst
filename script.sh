#!/bin/bash

CPU_USAGE_THRESHOLD=80
RAM_USAGE_THRESHOLD=80
DISK_USAGE_THRESHOLD=80
AVG_LOAD_THRESHOLD=80
LOG_DIR=$(pwd)  
LOG_FILE="$LOG_DIR/resource_monitor.log"
NOTIFICATION_SENT=false
LOG_FREQ=3m

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -c, --cpu <value>      Set CPU usage threshold (default: 80%)"
    echo "  -r, --ram <value>      Set RAM usage threshold (default: 80%)"
    echo "  -d, --disk <value>     Set Disk usage threshold (default: 80%)"
    echo "  -l, --load <value>     Set Load average threshold (default: 80%)"
    echo "  -p, --path <dir>       Set path to log directory (default: current dir)"
    echo "  -f, --freq <value>     Set logging frequency (default: 3 minutes) { 1s, 2s, 3m, 4m, 5h, 6h }"
    echo "  -h, --help             Show this help message"
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--cpu)
            CPU_USAGE_THRESHOLD="$2"
            shift 2
            ;;
        -r|--ram)
            RAM_USAGE_THRESHOLD="$2"
            shift 2
            ;;
        -d|--disk)
            DISK_USAGE_THRESHOLD="$2"
            shift 2
            ;;
        -l|--load)
            AVG_LOAD_THRESHOLD="$2"
            shift 2
            ;;
        -p|--path)
            LOG_DIR="$2"
            LOG_FILE="$LOG_DIR/resource_monitor.log"
            shift 2
            ;;
        -f|--freq)
            LOG_FREQ="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo "Invalid option: $1"
            exit 1
            ;;
    esac
done

handle_threshold_exceed() {
    echo -e "\n ALERT: $1 usage exceeded the threshold of $2% (Current: $3%)"

}
mkdir -p "$LOG_DIR"
echo "Logging to: $LOG_FILE"

while true; do
    clear
    echo "================ System Resource Monitor ================"
    
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    echo -e "\n🔹 CPU Usage:"
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2+$4}')
    echo "Usage: $CPU_USAGE%"

    if (( $(echo "$CPU_USAGE > $CPU_USAGE_THRESHOLD" | bc -l) )); then
        handle_threshold_exceed "CPU" "$CPU_USAGE_THRESHOLD" "$CPU_USAGE"
    fi
    
    echo -e "\n🔹 Memory Usage:"
    RAM_USAGE=$(free | awk '/Mem:/ {printf "%.2f", $3/$2 * 100}')
    echo "Used: $RAM_USAGE%"

    if (( $(echo "$RAM_USAGE > $RAM_USAGE_THRESHOLD" | bc -l) )); then
        handle_threshold_exceed "RAM" "$RAM_USAGE_THRESHOLD" "$RAM_USAGE"
    fi
    
    echo -e "\n🔹 Disk Usage:"
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
    echo "Used: $DISK_USAGE%"

    if [[ $DISK_USAGE -gt $DISK_USAGE_THRESHOLD && $NOTIFICATION_SENT == false ]]; then
        NOTIFICATION_SENT=true
        if command -v notify-send >/dev/null; then
            notify-send "⚠️ Disk usage is high! It's recommended to keep usage below $DISK_USAGE_THRESHOLD%, but it's currently at $DISK_USAGE%."
        else
            echo "Notification is not supported on this system, but disk usage is high!"
        fi
    fi
    
    echo -e "\n🔹 Load Average:"
    LOAD_AVG=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | tr -d ',')
    echo "Load Avg: $LOAD_AVG"

    if (( $(echo "$LOAD_AVG > $AVG_LOAD_THRESHOLD" | bc -l) )); then
        handle_threshold_exceed "Load Average" "$AVG_LOAD_THRESHOLD" "$LOAD_AVG"
    fi

    echo "{
        \"timestamp\": \"$TIMESTAMP\",
        \"cpu_usage\": \"$CPU_USAGE\",
        \"ram_usage\": \"$RAM_USAGE\",
        \"disk_usage\": \"$DISK_USAGE\",
        \"load_avg\": \"$LOAD_AVG\"
    }" >> "$LOG_FILE"

    sleep $LOG_FREQ
done
