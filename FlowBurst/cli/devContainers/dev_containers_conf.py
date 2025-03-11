import questionary
import subprocess
import os
import pyperclip
import pathlib
from devContainers.container import DEV_CONTAINER, docker_file

DOCKER_FILES_PATH = f"{pathlib.Path(__file__).parent.resolve()}/dock-files"

def copy_to_clipboard(file_name):
    """ Copies the content of a file to clipboard """
    with open(file_name, 'r') as f:
        text = f.read()
        pyperclip.copy(text)
    print(f"Copied contents of {file_name} to clipboard!")

def show_environments():
    """ Prints a list of available environments for the user to select from """
    print("Available development environments:\n")
    print("\n".join(DEV_CONTAINER.keys()))

def use_environments(config=False, existing_container=None):
    """
    Asks the user to select an environment and either:
    - Use a pre-configured Dockerfile (copy path to clipboard)
    - Run a Docker container and attach it to VS Code
    - Attach to an already running container (if specified)
    """
    if existing_container:
        attach_to_vscode(existing_container)
        return

    selected = questionary.select(
        "Select a container to use:",
        choices=list(DEV_CONTAINER.keys())
    ).ask()

    if not selected:
        print("No container selected. Exiting.")
        return

    image_name = DEV_CONTAINER[selected]
    print(f"Selected container: {selected} ({image_name})")

    if config:
        dockfile = docker_file[selected]
        copy_to_clipboard(f"{DOCKER_FILES_PATH}/{dockfile}")
        print(f"Pre-configured Dockerfile for {selected} copied!")
        print("\nBuild and run using:")
        print(f"make a docker image\neg. docker build -t {selected.lower()} -f {DOCKER_FILES_PATH}/{dockfile} .")
        print(f"run it using docker run command \n eg:docker run -d --name {selected.lower()} -v $(pwd):/workspace {selected.lower()}")
        print(f"connect to vscode using code --remote command \n eg:code --remote containers/{selected.lower()}")
    else:
        pull_image(image_name)
        run_container(image_name, selected.lower())
        attach_to_vscode(selected.lower())

def get_environments():
    """ Retrieves Dockerfile and dev-container configuration files """
    print("Fetching Dockerfile and dev-container configuration...")

def pull_image(image_name):
    """ Pulls the Docker image """
    try:
        subprocess.run(["docker", "pull", image_name], check=True)
        print(f"✅ Successfully pulled {image_name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to pull {image_name}. Ensure Docker is running.")

def run_container(image_name, container_name):
    """ Runs a new container with the required permissions for VS Code """
    try:
        print(f"🚀 Starting container: {container_name} with image: {image_name}...")
        subprocess.run([
            "docker", "run", "-dit", "--name", container_name,
            "-v", f"{os.getcwd()}:/workspace",
            "--privileged",
            "--cap-add=ALL",
            "--security-opt", "seccomp=unconfined",
            "--security-opt", "apparmor=unconfined",
            "--network=host",
            image_name , "/bin/bash"
        ], check=True)
        print(f"✅ Container {container_name} is now running!")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to start container {container_name}. Check Docker logs.")

def attach_to_vscode(container_name):
    """ Attaches a running container to VS Code """
    print(f"🔗 Attaching {container_name} to VS Code...")
    try:
        subprocess.run(["code", "--remote", f"containers/{container_name}"], check=True)
        print(f"✅ Successfully attached to {container_name} in VS Code.")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to attach {container_name} to VS Code. Ensure it is running.")

def list_active_containers():
    """ Lists all active Docker containers """
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, check=True)
        containers = result.stdout.strip().split("\n")
        if containers:
            print("Active Containers:")
            for container in containers:
                print(f"- {container}")
        else:
            print("No active containers found.")
    except subprocess.CalledProcessError:
        print("❌ Failed to list active containers.")

def connect_to_container(name):
    """ Connects the user to an existing container in VS Code """
    print(f"🔗 Connecting to existing container: {name}...")
    attach_to_vscode(name)
