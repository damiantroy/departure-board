from dataclasses import dataclass
from datetime import datetime

import tomli


@dataclass
class Config:
    route_type: int
    stop_id: int
    direction_id: int
    base_url: str
    dev_id: str
    api_key: str
    timezone: str


def read_config() -> Config:
    with open("config/config.toml", "rb") as f:
        config_data = tomli.load(f)

    config = Config(
        route_type=config_data.get("route_type"),
        stop_id=config_data.get("stop_id"),
        direction_id=config_data.get("direction_id"),
        base_url=config_data.get("base_url"),
        dev_id=config_data.get("dev_id"),
        api_key=config_data.get("api_key"),
        timezone=config_data.get("timezone"),
    )

    # If the config timezone is not set, use the machine's timezone
    if not config.timezone:
        config.timezone = datetime.now().astimezone().tzinfo

    return config
