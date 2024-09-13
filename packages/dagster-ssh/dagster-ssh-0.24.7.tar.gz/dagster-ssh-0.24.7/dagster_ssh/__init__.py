from dagster._core.libraries import DagsterLibraryRegistry

from dagster_ssh.resources import SSHResource, ssh_resource
from dagster_ssh.version import __version__

DagsterLibraryRegistry.register("dagster-ssh", __version__)

__all__ = ["ssh_resource", "SSHResource"]
