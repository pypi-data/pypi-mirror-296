import logging
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from hydra._internal.core_plugins.basic_sweeper import BasicSweeper, BasicSweeperConf
from hydra.core.config_store import ConfigStore
from hydra.core.hydra_config import HydraConfig
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
class ExtSweeperConf(BasicSweeperConf):
    _target_: str = "hydra_plugins.hydra_ext_sweeper.ext_sweeper.ExtSweeper"


ConfigStore.instance().store(
    group="hydra/sweeper",
    name="ext",
    node=ExtSweeperConf,
    provider="hydra-ext-sweeper",
)

log = logging.getLogger(__name__)


class ExtSweeper(BasicSweeper):
    """A hydra sweeper with extended syntax for efficient parameter sweeping."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def sweep(self, arguments: list[str]) -> list[Sequence[JobReturn]]:
        # log.info("RangeSweeper sweeping")
        # log.info(f"Sweep output dir : {self.config.hydra.sweep.dir}")
        return super().sweep(arguments)

    #     src_lists = []
    #     for s in arguments:
    #         key, value = s.split("=")
    #         gl = re.match(r"glob\((.+)\)", value)
    #         if "," in value:
    #             possible_values = value.split(",")
    #         elif ":" in value:
    #             possible_values = range(*[int(v) for v in value.split(":")])
    #         elif gl:
    #             possible_values = list(glob.glob(gl[1], recursive=True))
    #         else:
    #             possible_values = [value]
    #         src_lists.append([f"{key}={val}"
    #                          for val in possible_values])

    #     batch = list(itertools.product(*src_lists))

    #     returns = [self.launcher.launch(batch)]
    #     return returns
