import logging
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from hydra.core.config_store import ConfigStore
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.override_parser.types import (
    ChoiceSweep,
    Override,
    OverrideType,
    ValueType,
)
from hydra.core.plugins import Plugins
from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.plugins.sweeper import Sweeper
from hydra.types import HydraContext, TaskFunction
from omegaconf import DictConfig, OmegaConf

log = logging.getLogger(__name__)


@dataclass
class SweeperConfig:
    _target_: str = "hydra_plugins.ext_sweeper_plugin.ext_sweeper.ExtSweeper"


ConfigStore.instance().store(
    group="hydra/sweeper",
    name="ext",
    node=SweeperConfig,
    provider="hydra-ext-sweeper",
)


class ExtSweeper(Sweeper):
    """A hydra sweeper with extended syntax for efficient parameter sweeping."""

    def __init__(self):
        super().__init__()

        self.config: DictConfig | None = None
        self.launcher: Launcher | None = None
        self.hydra_context: HydraContext | None = None

    def __repr__(self):
        return "ExtSweeper()"

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        self.hydra_context = hydra_context
        self.config = config
        self.launcher = Plugins.instance().instantiate_launcher(
            hydra_context=hydra_context,
            task_function=task_function,
            config=config,
        )

    def sweep(self, arguments: list[str]) -> list[Sequence[JobReturn]]:
        log.info(f"{self!s} sweeping")
        log.info(f"Sweep output dir : {self.config.hydra.sweep.dir}")
        return []
