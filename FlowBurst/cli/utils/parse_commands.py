import argparse
from .services import Services

def manage_service(command, services): 
    for service in services:
        if service in Services:
            Services[service][command]()  
        else:
            print(f"⚠️ Unknown service: {service}")

def parse_commands():
    parser = argparse.ArgumentParser(prog="FlowBurst", description="Want The local dev env switch to cloud env with same dependencies and seamlessly? We Got You")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Commands")

    # monitoring
    monitor_parser = subparsers.add_parser("monitor", help="Monitor system resources")
    monitor_parser.add_argument("action", choices=["start", "stop", "status"], help="Action to perform on monitoring")

    # enviroments
    monitor_parser = subparsers.add_parser("environment", help="Monitor system resources")
    monitor_parser.add_argument("action", choices=["show", "use", "get"], help="Action to perform on environments")

    args = parser.parse_args()

    if args.command == "monitor":
        manage_service(args.action, ["monitoring"])
    elif args.command == "environment":
        manage_service(args.action, ["environments"])