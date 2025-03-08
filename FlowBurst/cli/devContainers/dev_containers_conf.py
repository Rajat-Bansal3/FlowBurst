import questionary
from devContainers.container import DEV_CONTAINER , docker_file
import subprocess
import os
import shutil
import pathlib


DOCKER_FILES_PATH=f"{pathlib.Path(__file__).parent.resolve()}/dock-files"

def show_environments ():
    """

    prints a list of available environments to select from for the user 

    """
    print("Select a container to pull:\n")
    print(" \n".join(DEV_CONTAINER.keys())) 
        

def use_environments (config=False):
    """
        asks the user to select a environment to use
    """
    selected = questionary.select(
        "Select a container to pull:",
        choices=list(DEV_CONTAINER.keys())
    ).ask()
    if not selected:
        print("No container selected. Exiting.")
        return
    image_name = DEV_CONTAINER[selected]
    print(f"Selected container: {selected} ({image_name})")
    if(config):
        dockfile = docker_file[selected]
        shutil.copy(f"{DOCKER_FILES_PATH}/{dockfile}.flowburst")
        shutil.copy(preconfig_file, "Dockerfile")
        print(f"Pre-configured Dockerfile for {selected} copied!")
        print(f"\nBuild and run using:\n")
        # WIP: write command to attack container to vscode
    else:
        pull_image(image_name)


def get_environments ():
    print("get docker file and dev-container file for dev container")
def pull_image(image_name):
    try:
        subprocess.run(["docker", "pull", image_name], check=True)
        print(f"Successfully pulled {image_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to pull {image_name}. Ensure Docker is running.")