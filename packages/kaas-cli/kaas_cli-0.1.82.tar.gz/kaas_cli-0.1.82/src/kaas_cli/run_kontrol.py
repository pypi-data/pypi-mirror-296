from __future__ import annotations

import logging
import os
import random
import re
import shutil
import subprocess
import sys

import click
import docker
import requests

from .constants import CONFIG_LOG_PATH
from .types import KontrolVersion  # noqa: TC003


class RunKontrol:
    def __init__(self, kontrol_version: KontrolVersion, mode: str):
        self.kontrol_version = kontrol_version
        self.mode = mode
        self._configure_logging()

    def _configure_logging(self) -> None:
        """Configure logging for the application."""
        if not CONFIG_LOG_PATH.exists():
            CONFIG_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONFIG_LOG_PATH.touch()
        logging.basicConfig(
            filename=CONFIG_LOG_PATH,
            filemode='a',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG,
        )

    def run(self) -> bool:
        """
        Run Kontrol with the given version and current source code within the current directory structure.
        KaaS will do the best it can to provide default values for kontrol.toml and foundry.toml, but it may not be possible to provide defaults for all configurations.
        Execution will start and results dumped to log/console.
        True if Kontrol ran at all PERIOD. If there are errors in the proofs these will be output but that is still a success to RUN kontrol.
        Returns:
            bool: True if Kontrol ran successfully, False otherwise
        """
        if self.mode == 'container':
            return self.run_in_container()
        elif self.mode == 'local':
            return self.run_locally()
        elif self.mode == 'remote':
            return self.run_remotely()
        else:
            click.echo(f"Invalid mode: {self.mode}")
            return False

    def run_in_container(self) -> bool:
        if not self.is_docker_installed():
            click.echo("Docker is not installed. Please install Docker to run in a container.")
            return False

        self.kontrol_version = self.get_or_set_kontrol_version()
        if self.kontrol_version == "v0.0.0":
            click.echo("Error getting latest Kontrol release and No Version Specified. Exiting...")
            sys.exit(1)

        try:
            self.setup_docker_container()
            self.run_kontrol_in_container()
            return True
        except Exception as e:
            click.echo(f"Critical Container Error: {e}")
            sys.exit(1)

    def get_or_set_kontrol_version(self) -> KontrolVersion:
        if self.kontrol_version == "v0.0.0":
            click.echo("No Version Specified... Using LATEST Kontrol Version")
            return self.get_latest_kontrol_release()
        return self.kontrol_version

    def setup_docker_container(self) -> None:
        kv = self.kontrol_version.lstrip('v')
        click.echo(f"Using Kontrol Image: runtimeverificationinc/kontrol:ubuntu-jammy-{kv}")

        kontrol_toml, foundry_toml = self.find_kontrol_configs()
        self.output_folder = self.scrape_foundry_toml(foundry_toml)
        docker_client = docker.from_env()
        click.echo("Pulling Kontrol Image...")
        image_tag = "ubuntu-jammy-" + kv
        docker_client.images.pull("runtimeverificationinc/kontrol", tag=image_tag)

        container_id = random.randint(1000, 2000)
        click.echo(f"Generated container ID: {container_id}")
        self.container = docker_client.containers.run(
            f"runtimeverificationinc/kontrol:ubuntu-jammy-{kv}",
            name=f"kaas-proof-container-{container_id}",
            command="tail -f /dev/null",  # Keeps the container running
            # volumes={os.getcwd(): {'bind': '/opt/kaas', 'mode': 'rw'}},
            stdout=True,
            stderr=True,
            remove=True,
            user="user",
            detach=True,
            working_dir="/opt/kaas",
        )
        click.echo("Setting Permissions on Container Files...")
        self.container.exec_run("chown -R user:user /opt/kaas", stream=True, user='root')
        self.copy_files_to_container(self.container.name, '/opt/kaas', os.path.dirname(kontrol_toml))
        # self.configure_container_user()

    def scrape_foundry_toml(self, foundry_toml: str) -> str:
        foundry_toml_path = os.path.abspath(foundry_toml)
        try:
            with open(foundry_toml_path, 'r') as file:
                for line in file:
                    if line.startswith('out'):
                        out_value = line.split('=')[1].strip().strip('"')  # Strip the quotes and spaces
                        return out_value
            raise RuntimeError("No 'out' value found in foundry.toml")
        except Exception as e:
            click.echo(f"Read Error on foundry.toml: {e}")
            sys.exit(1)

    def copy_files_to_container(self, container_id: str | None, container_path: str, host_path: str) -> None:
        if container_id is None:
            click.echo("Lost Context to Container... Exiting...")
            raise RuntimeError("Lost context to container")
        user_id = 'user'
        group_id = 'user'
        command = f"tar -cf - ./ | docker exec -i {container_id} bash -cl 'tar -xf - -C {container_path} --owner={user_id} --group={group_id}'"
        try:
            click.echo("Copying files to container")
            os.chdir(host_path)
            subprocess.run(command, shell=True, check=True)
        except Exception as e:
            click.echo(f"Error copying files to container: {e}")
            sys.exit(1)

    def copy_files_from_container(self, container_id: str | None, container_path: str, host_path: str) -> None:
        if container_id is None:
            click.echo("Lost Context to Container... Exiting...")
            raise RuntimeError("Lost context to container")
        # Create a tarball inside the container and stream it to the host
        # user_id = os.getuid()
        # group_id = os.getgid()
        command = (
            f"docker exec -i {container_id} bash -cl 'tar -cf - -C {container_path} {self.output_folder}/' | tar -xf -"
        )
        try:
            click.echo("Copying files from container")
            subprocess.run(command, shell=True, check=True)
        except Exception as e:
            click.echo(f"Error copying files from container: {e}")
            sys.exit(1)

    def run_kontrol_in_container(self) -> None:
        click.echo(f"Container Status: {self.container.status}")
        click.echo(f"Container Name: {self.container.name}")
        click.echo(f"Container ID: {self.container.id}")
        click.echo("Starting Kontrol Build...")
        return_code = self.container.exec_run("kontrol build", stdout=True, stderr=True, workdir="/opt/kaas")
        click.echo(f"Build Return Code: {return_code}")
        self.container.logs()

        click.echo("Starting Kontrol Prove...")
        return_code = self.container.exec_run("kontrol prove", stdout=True, stderr=True, workdir="/opt/kaas")
        click.echo(f"Prove Return Code: {return_code}")
        self.container.logs()

        self.copy_files_from_container(self.container.name, "/opt/kaas", "./")
        click.echo("Stop Container...")
        self.container.stop()

    def run_locally(self) -> bool:
        if not self.is_kontrol_installed():
            click.echo("Kontrol is not installed. Please install Kontrol to run locally. Using kup.")
            click.echo(
                "  For installation instructions, visit: https://github.com/runtimeverification/kontrol#fast-installation"
            )
            return False

        self.check_local_kontrol_version()
        kontrol_toml, foundry_toml = self.find_kontrol_configs()
        click.echo(f"  Change directory to: {os.path.dirname(kontrol_toml)}")
        dirname = os.path.dirname(kontrol_toml)
        os.chdir(dirname)
        if not self.run_kontrol_build():
            return False

        if not self.run_kontrol_prove():
            return False

        return True

    def check_local_kontrol_version(self) -> None:
        os.system("kontrol version")
        click.echo("  is installed. Checking Kontrol Version...")
        if self.kontrol_version == "v0.0.0":
            click.echo('No Version Specified... Using currently installed version')
        else:
            self.verify_specific_kontrol_version()

    def verify_specific_kontrol_version(self) -> None:
        click.echo(f"Requested Kontrol Version: {self.kontrol_version}")
        try:
            result = subprocess.run(["kontrol", "version"], check=True, capture_output=True, text=True)
            version = self.kontrol_version.lstrip('v')
            version_pattern = re.compile(rf"Kontrol version: {re.escape(version)}\b")
            if version_pattern.search(result.stdout):
                click.echo("Exact Version Installed. Proceeding...")
            else:
                click.echo(f"Requested Version: {version}, NOT FOUND")
                click.echo(
                    "  Visit https://github.com/runtimeverification/kontrol#fast-installation for installation instructions"
                )
                sys.exit(1)
        except Exception as e:
            click.echo(f"Error checking Kontrol Version: {e}")
            sys.exit(1)

    def run_kontrol_build(self) -> bool:
        try:
            click.echo("Starting Kontrol Build...")
            result = subprocess.run(["kontrol", "build"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            click.echo(result.stdout)  # Print the entire output to stdout
            if result.returncode != 0:
                click.echo("Error detected during Kontrol build. Skipping prove step.")
                return False
            return True
        except Exception as e:
            click.echo(f"Error running Kontrol build: {e}")
            return False

    def run_kontrol_prove(self) -> bool:
        try:
            click.echo("Starting Kontrol Prove...")
            result = subprocess.run(["kontrol", "prove"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            click.echo(result.stdout)  # Print the entire output to stdout
            if result.returncode != 0:
                click.echo("Error detected during Kontrol prove. Skipping prove step.")
                return False
            return True
        except Exception as e:
            click.echo(f"Error running Kontrol prove: {e}")
            return False

    def run_remotely(self) -> bool:
        click.echo("Running on https://KaaS.runtimeverification.com")
        click.echo("  Visit your Compute Dashboard to check the status of your jobs.")
        # TODO: Check context for logged in status
        # TODO: Check context for vault_spec
        # TODO: Check context for token
        # TODO: Check foundry.toml / kontrol.toml
        # TODO: Opens Local Browser to kaas.runtimeverification.com to track the build

        click.echo("Running Kontrol Build")
        click.echo("Running Kontrol Prove")
        return True

    def get_latest_kontrol_release(self) -> KontrolVersion:
        url = "https://api.github.com/repos/runtimeverification/kontrol/releases/latest"
        try:
            reponse = requests.get(url)
            if reponse.status_code == 200:
                return reponse.json()['tag_name']
            else:
                raise RuntimeError("Fetching Latest Release Failed..")
        except Exception as e:
            click.echo(f"Error: {e}")
            click.echo("  Specify a version already locally installed or check your internet connection")
            sys.exit(1)

    def is_docker_installed(self) -> bool:
        # Check User environment for 'docker' command
        try:
            shutil.which('docker')
        except Exception as e:
            logging.error(f"Error checking for docker installation: {e}")
            return False
        return True

    def is_kontrol_installed(self) -> bool:
        # Check User environment for 'kontrol' command
        click.echo("Checking local Kontrol installation...")
        try:
            shutil.which('kontrol')
        except Exception as e:
            click.echo(f"Error checking for kontrol: {e}")
            return False
        return True

    def find_kontrol_configs(self) -> tuple[str, str]:
        """
        Check if kontrol.toml and foundry.toml or just 'foundry.toml' exist below the current directory.
        Use chdir to change to the directory containing the kontrol.toml and foundry.toml files
        then if they do exist, return the path, otherwise return None

        Returns:
            str: Path to the directory containing the kontrol.toml and foundry.toml files
        """
        # Check if kontrol.toml and foundry.toml or just 'foundry.toml' exist below the current directory
        kontrol_toml = self.find_file('kontrol.toml') + '/kontrol.toml'
        foundry_toml = self.find_file('foundry.toml') + '/foundry.toml'
        if kontrol_toml == "" and foundry_toml != "":
            click.echo("No kontrol.toml file found...")
            click.echo("  Foundry Files Found! .... Kontrol attempting to generate a default kontrol.toml file")
            # TODO Hold off on helping further until we have a better understanding of what the user wants and how kontrol should be used to provide a better default init configuration
            sys.exit(1)
        elif foundry_toml == "":
            click.echo(
                "No foundry.toml file found. Please create a foundry.toml file or run 'kaas-cli run --help' for more information."
            )
            sys.exit(1)
        else:
            click.echo("Found kontrol.toml and foundry.toml files.")
        return kontrol_toml, foundry_toml

    def find_file(self, file_name: str) -> str:
        """
        Check if the file exists below the current directory
        if it does, return the path to the file, otherwise return None

        Returns:
            str: Path to the file
        """
        for root, _dirs, files in os.walk("."):
            if file_name in files:
                return os.path.relpath(root)
        return ""
