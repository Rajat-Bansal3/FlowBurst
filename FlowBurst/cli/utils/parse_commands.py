import argparse
from .services import Services

def manage_service(command, services, container_name=None): 
    for service in services:
        if service in Services:
            if container_name:
                Services[service][command](container_name)  # Pass container name if provided
            else:
                Services[service][command]()  
        else:
            print(f"Unknown service: {service}")

def parse_commands():
    parser = argparse.ArgumentParser(
        prog="FlowBurst",
        description="Want The local dev env switch to cloud env with same dependencies and seamlessly? We Got You"
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Commands")

    # Monitoring
    monitor_parser = subparsers.add_parser("monitor", help="Monitor system resources")
    monitor_parser.add_argument("action", choices=["start", "stop", "status"], help="Action to perform on monitoring")

    # Environments
    env_parser = subparsers.add_parser("environment", help="Manage environments")
    env_parser.add_argument("action", choices=["show", "use", "get"], help="Action to perform on environments")
    env_parser.add_argument("--pre-config", "-C", action="store_true", help="Use preconfigured Docker files written by the community")
    env_parser.add_argument("--existing-container", "-Ec", type=str, help="Use an existing container by name")

    args = parser.parse_args()
    print(args)  # Debugging output

    if args.command == "monitor":
        manage_service(args.action, ["monitoring"])
    
    elif args.command == "environment":
        if args.action == "use":
            if args.existing_container:
                manage_service("use --existing-container", ["environments"], args.existing_container)
            elif args.pre_config:
                manage_service("use --pre-config", ["environments"])
            else:
                manage_service("use", ["environments"])
        else:
            manage_service(args.action, ["environments"])

