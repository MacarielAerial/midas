"""
Test the entire flow end to end
"""

import logging
from pathlib import Path
from typing import Any, Dict

from kedro.config import ConfigLoader
from kedro.io import DataCatalog
from kedro.runner import SequentialRunner
from pipelinex import FlexiblePipeline, HatchDict

from midas.nodes.kedro_utils import get_feed_dict

log = logging.getLogger(__name__)


def test_e2e() -> None:
    conf_loader: ConfigLoader = ConfigLoader(conf_paths=["conf/base", "conf/local"])

    conf_logging: Dict[str, Any] = conf_loader.get("logging*", "logging*/**")
    logging.config.dictConfig(conf_logging)

    conf_catalog: Dict[str, Any] = conf_loader.get("catalog*", "catalog*/**")
    data_catalog: DataCatalog = DataCatalog.from_config(conf_catalog)

    conf_params: Dict[str, Any] = conf_loader.get("parameters*", "parameters*/**")
    data_catalog.add_feed_dict(feed_dict=get_feed_dict(params=conf_params))

    conf_pipeline: Dict[str, Any] = conf_loader.get("pipelines*", "pipelines*/**")
    ac_pipeline: FlexiblePipeline = HatchDict(conf_pipeline).get("acquisition_pipeline")

    runner: SequentialRunner = SequentialRunner()
    runner.run(pipeline=ac_pipeline, catalog=data_catalog)

    assert Path("data/01_raw/snp_names.json").is_file()
