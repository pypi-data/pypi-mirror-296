#!/usr/bin/env python

import argparse
import os
import logging
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import json
from talp_pages.talp_common import (
    TALP_PAGES_VERSION,
    HighlightedRegions,
    TalpPageMetadata
)
from talp_pages.talp_badge import TalpBadge
from talp_pages.io.run_folders import RunFolder, get_run_folders 

from talp_pages.views.time_series_view import TimeSeriesView

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly import colors as pcolors

import plotly.express as px

from typing import List, Optional
from datetime import datetime


@dataclass
class ScalingView:
    pass


@dataclass
class MergeRequestView:
    pass


@dataclass
class TalpPageFolder:
    """Class for representing a Result page for a runfolder instance"""
    name: str
    run_folder: RunFolder
    output_path: Path
#    scaling_view: ScalingView
#    merge_request_view: MergeRequestView
    time_series_view: TimeSeriesView
    badge: Optional[TalpBadge] = None
    


def _verify_input(args):
    path = None

    # Check if the JSON file exists
    if os.path.exists(args.path):
        found_a_json = False
        for _, _, filenames in os.walk(args.path):
            for _ in [f for f in filenames if f.endswith(".json")]:
                found_a_json = True

        if not found_a_json:
            logging.error(
                f"The specified path '{args.path}' doesnt contain any .json files "
            )
            raise Exception("Path empty of .json files")
    else:
        logging.error(f"The specified path '{args.path}' does not exist.")
        raise Exception("Not existing path")

    # Check if output is empty

    if os.path.exists(args.output):
        if len(os.listdir(args.output)) != 0:
            logging.error(f"The specified output folder '{args.output}' is not empty")
            raise Exception("Non Empty output path")

    path = args.path
    output = args.output

    return path, output


def get_landing_page(pages):
    paths = []
    dfs = []
    for page in pages:
        dfs.extend(get_dfs(page.run_folder))
        paths.append(page.output_path)

    df = pd.concat(dfs)
    # filter df
    df= df[df['elapsedTime']>1]
    now = datetime.now().replace(tzinfo=None)
    df['timedelta_since_now'] = now-df['timestamp']
    df['days_since_now'] = df['timedelta_since_now'] / pd.to_timedelta(1, unit='D')
    
    opacities =1 -(df['days_since_now']/df["days_since_now"].max())
    fig = px.scatter(df,opacity=opacities, color="name",x="elapsedTime", y="parallelEfficiency",symbol="name",hover_data=["name", "metadata"])
    fig.update_coloraxes(showscale=False)
    fig.update_traces(marker={'size': 11})
    fig.to_html()
    #return render_template(TALP_PAGES_TEMPLATE_PATH, "landing_page.jinja", paths=paths,figure_overview=fig.to_html(full_html=False),)


def main(args):    

    path, output = _verify_input(args)
    now = datetime.now()
    # First detect the folder structure and append to the runs
    run_folders = get_run_folders(path)
    
    #highlighted_regions = HighlightedRegions(selected_regions=[TALP_PAGES_DEFAULT_REGION_NAME])
    #page_metadata = TalpPageMetadata(timestamp=now,timestamp_string=now.replace(microsecond=0).isoformat(),version=TALP_PAGES_VERSION)

    pages = []
    for run_folder in run_folders:
        logging.info(f"Processing folder: {run_folder.relative_path}")
        # pages
        dfs = get_dfs(run_folder)
        df = pd.concat(dfs)
     
        badge = None
        if args.badge:
            badge = TalpBadge(run_folder.latest_json)
        pages.append(
            TalpPageFolder(
                name=run_folder.relative_path,
                run_folder=run_folder, output_path=run_folder.relative_path, 
                time_series_view=TimeSeriesView(df,highlighted_regions,page_metadata),
                badge=badge
            )
        )
    for page in pages:
        output_path = os.path.join(output, page.output_path)
        os.makedirs(output_path)
        logging.info(f"Writing output in {output_path}")
        with open(os.path.join(output_path, "index.html"), "w") as json_file:
            json_file.write(page.time_series_view.get_html())
        if page.badge:
            rendered_svg = page.badge.get_badge_svg()
            with open(os.path.join(output_path, "talp.svg"), "wb") as f:
                f.write(rendered_svg)


    landing_page = get_landing_page(pages)
    with open(os.path.join(output, "index.html"), "w") as json_file:
        json_file.write(landing_page)


if __name__ == "__main__":
    main()
