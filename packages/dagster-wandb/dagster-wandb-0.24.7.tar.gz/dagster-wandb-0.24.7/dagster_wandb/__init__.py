from dagster._core.libraries import DagsterLibraryRegistry

from dagster_wandb.io_manager import WandbArtifactsIOManagerError, wandb_artifacts_io_manager
from dagster_wandb.launch.ops import run_launch_agent, run_launch_job
from dagster_wandb.resources import wandb_resource
from dagster_wandb.types import SerializationModule, WandbArtifactConfiguration
from dagster_wandb.version import __version__

DagsterLibraryRegistry.register("dagster-wandb", __version__)

__all__ = [
    "WandbArtifactsIOManagerError",
    "SerializationModule",
    "wandb_resource",
    "wandb_artifacts_io_manager",
    "WandbArtifactConfiguration",
    "run_launch_agent",
    "run_launch_job",
]
