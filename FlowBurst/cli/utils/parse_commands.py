import argparse
from .services import Services

def manage_service(command, services): 
    for service in services:
        if service in Services:
            Services[service][command]()  
        else:
            print(f"Unknown service: {service}")

def parse_commands():
    parser = argparse.ArgumentParser(prog="FlowBurst", description="Want The local dev env switch to cloud env with same dependencies and seamlessly? We Got You")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Commands")

    # monitoring
    monitor_parser = subparsers.add_parser("monitor", help="Monitor system resources")
    monitor_parser.add_argument("action", choices=["start", "stop", "status"], help="Action to perform on monitoring")

    # environments
    env_parser = subparsers.add_parser("environment", help="Manage environments")
    env_parser.add_argument("action", choices=["show", "use", "get"], help="Action to perform on environments")

    if env_parser.get_default('action') == 'use':
        env_parser.add_argument("--pre-config", action="store_true", help="use preconfigured docker files written by community")

    args = parser.parse_args()

    if args.command == "monitor":
        manage_service(args.action, ["monitoring"])
    elif args.command == "environment":
        print(args)
        if args.action == "use" and args.pre_config:
            manage_service("use --pre-config", ["environments"])
        else:
            manage_service(args.action, ["environments"])

