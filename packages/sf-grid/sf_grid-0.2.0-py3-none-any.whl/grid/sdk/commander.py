import paramiko
import subprocess
import shlex
import docker

class Commander:
    def __init__(self):
        self.node_data = None

    def set_node_data(self, data):
        self.node_data = data

    def check_grid_containers(self, node_name: str) -> bool:
        core_status = self.check_docker_container('grid_core', node_name)
        service_status = self.check_docker_container('grid_service', node_name)
        return core_status and service_status

    def check_docker_container(self, container_name: str, node_name: str) -> bool:
        command = "docker ps --format {{.Names}}"
        output = self.run_command(command, node_name, run_quiet=True)

        container_list = output.splitlines() if output else []
        return container_name in container_list

    def init_containers(self, node_name):
        images = ["sfgrid.azurecr.io/grid/core/sdk:latest", "sfgrid.azurecr.io/grid/serve/sdk:latest"]

        if node_name == "local":
            client = docker.from_env()

            try:
                for image in images:
                    client.images.get(image)

            except docker.errors.ImageNotFound:
                print("One or more Docker images do not exist. Attempting to download them...")
                self.update_containers(node_name)

        if self.node_data and node_name in self.node_data:
            node_info = self.node_data[node_name]
            if 'storage' in node_info:
                storage_volumes = node_info['storage']
                volume_mounts = " ".join([f"-v {host_path}:/mnt/{container_path}" for container_path, host_path in storage_volumes.items()])
            else:
                volume_mounts = ""
        else:
            volume_mounts = ""

        if volume_mounts:
            for mount in volume_mounts.split(" "):
                if mount.startswith("/"):
                    host_path, container_path = mount.split(":")
                    print(f"Mounting {host_path} to {container_path}")

        containers = {
            'grid_core': f"docker run -d --gpus all --network host {volume_mounts} --name grid_core sfgrid.azurecr.io/grid/core/sdk:latest",
            'grid_service': f"docker run -d --gpus all --network host {volume_mounts} --name grid_service sfgrid.azurecr.io/grid/serve/sdk:latest"
        }

        container_status = {container: self.check_docker_container(container, node_name) for container in containers}

        for container, command in containers.items():
            if not container_status[container]:
                print(f"Spinning up {container} on {node_name}...")
                self.run_command(command, node_name, run_quiet=True)

        container_status = {container: self.check_docker_container(container, node_name) for container in containers}

        for container, status in container_status.items():
            status_symbol = u"\u2713" if status else u"\u274C"
            print(f"{container}: {status_symbol}")

        if not container_status['grid_service'] or not container_status['grid_core']:
            print("Error: One or more GRID containers failed to start. Please check the logs.")
        else:
            print("Containers are active.")

    def login_registry(self, node_name, username, password):
        """Login to the GRID registry using username and password/access token"""
        print("Logging in to Scaled Foundations - GRID registry...")

        if node_name == 'local':
            login_command = f"docker login sfgrid.azurecr.io -u {username} --password-stdin"
            completed_process = subprocess.run(shlex.split(login_command), input=password.encode() + b'\n', capture_output=True)
            if completed_process.returncode == 0:
                print("Login successful!")
            else:
                print("Login failed with the following error:")
                print(completed_process.stderr.decode())

        else:
            # Prepare the Docker login command without embedding the password
            login_command = f"echo {password} | docker login sfgrid.azurecr.io -u {username} --password-stdin"

            # Use self.run_command to execute the login command
            self.run_command(login_command, node_name)

    def kill_containers(self, node_name):
        print(f"Stopping containers...")

        containers = ['grid_core', 'grid_service']

        for container in containers:
            commands = [f"docker stop {container}", f"docker rm {container}"]
            for command in commands:
                self.run_command(command, node_name, run_quiet=True)

        container_status = {container: self.check_docker_container(container, node_name) for container in containers}
        for container, status in container_status.items():
            status_symbol = u"\u2713" if status else u"\u274C"
            print(f"{container}: {status_symbol}")

        if not container_status['grid_service'] or not container_status['grid_core']:
            print("Containers stopped successfully.")
        else:
            print("Error: One or more containers are still active.")


    def update_containers(self, node_name):
        images = ["sfgrid.azurecr.io/grid/core/sdk:latest", "sfgrid.azurecr.io/grid/serve/sdk:latest"]

        if node_name == 'local':
            self._pull_docker_images(images)

        else:
            commands = [f"docker pull {image}" for image in images]

            for command in commands:
                self.run_command(command, node_name, run_quiet=False)

    def _pull_docker_images(self, images):
        for image in images:
            try:
                client = docker.from_env()
                for line in client.api.pull(image, stream=True, decode=True):
                    if 'progress' in line:
                        print(f"\r{line['status']} {line['progress']}", end='', flush=True)
                    elif 'status' in line:
                        print(f"\r{line['status']}", end='', flush=True)

                print(f"\n Image {image} pulled successfully.")

            except Exception as e:
                print(f"An error occurred: {e}")

    def run_command(self, command: str, node_name: str, run_quiet: str = False):
        if node_name == 'local':
            process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout:
                if not run_quiet:
                    print(stdout.strip())
                return stdout
            if stderr:
                print(stderr.strip())
        else:
            if self.node_data and node_name in self.node_data:
                output = self.run_remote_command(node_name, command)
                print(output)
                return output
            else:
                print(f"Error: Node data for '{node_name}' not found. Available nodes: {list(self.node_data.keys())}")

    def run_remote_command(self, resource_name: str, command: str) -> str:
        hostname = self.node_data[resource_name]["ip"]
        username = self.node_data[resource_name]["username"]
        password = self.node_data[resource_name]["password"]

        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the remote host
            ssh.connect(hostname, username=username, password=password)

            # Execute the command
            stdin, stdout, stderr = ssh.exec_command(command)

            # Read the output and error streams
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                return f"Error: {error}"
            return output
        except Exception as e:
            return f"Exception: {str(e)}"
        finally:
            # Close the SSH connection
            ssh.close()
