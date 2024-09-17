from dataclasses import dataclass
from pathlib import Path
import os
from enum import Enum
import logging

from datetime import datetime
class RenderedSiteType(Enum):
    TIMESERIES = "Time Series"
    SCALING = "Scaling"
    LANDINGPAGE = "Landing Page"


@dataclass
class RenderedSite:
    relative_output_path: str
    filename: str
    content: str
    type: RenderedSiteType
    label: str
    latest_change: datetime
    

@dataclass
class RenderedBadge:
    relative_output_path: str
    filename: str
    region_for_badge: str
    ressource_label: str
    content: str



def write_badge(output_path: Path, badge: RenderedBadge):
    folder = os.path.join(output_path,badge.relative_output_path)
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder,badge.filename)
    logging.debug(f"Writing Badge {file_path}")
    with open(file_path, "w") as file:
        file.write(badge.content)


def write_site(output_path: Path, site: RenderedSite):
    folder = os.path.join(output_path,site.relative_output_path)
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder,site.filename)
    logging.debug(f"Writing Site {file_path}")
    with open(file_path, "w") as file:
        file.write(site.content)