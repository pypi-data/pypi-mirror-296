import logging
import pandas as pd

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly import colors as pcolors
from typing import List
from pathlib import Path
import numpy as np
from talp_pages.views.base_view import BaseView
from talp_pages.talp_common import (
    TALP_METRIC_TO_NAME_MAP,
    TALP_JSON_TIMESTAMP_KEY,
    TALP_JSON_METADATA_KEY,
    TalpPageMetadata,
    TALP_IMPLICIT_REGION_NAME
)

def sample_colorscale(colorscale, num_samples):
    """
    Samples a Plotly color scale and returns a list of discrete colors.

    Parameters:
    colorscale (list or str): The Plotly color scale to sample. It can be a predefined string or a custom color scale list.
    num_samples (int): The number of colors to sample from the color scale.

    Returns:
    list: A list of sampled colors in hexadecimal format.
    """
    if isinstance(colorscale, str):
        colorscale = pcolors.get_colorscale(colorscale)

    # Ensure the colorscale is normalized to [0, 1]
    colorscale = [
        (i / (len(colorscale) - 1), color) for i, color in enumerate(colorscale)
    ]

    # Generate the samples
    samples = [
        colorscale[int(i * (len(colorscale) - 1) / (num_samples - 1))][1]
        for i in range(num_samples)
    ]

    return samples

class TimeSeriesView(BaseView):

    def __init__(self,dataframe : pd.DataFrame, highlighted_regions_:List[str] ):
        self.df = dataframe
        self.highlighted_regions = highlighted_regions_
    
    def __get_scatter(self,region, metric, color, show_legend=False):
            
            if region in self.highlighted_regions:
                is_visible = True
            else:
                is_visible = "legendonly"
            
            return go.Scatter(
                x=self.df[self.df["regionName"] == region]["timestamp"],
                y=self.df[self.df["regionName"] == region][metric],
                text=self.df[self.df["regionName"] == region]["metadata"],
                mode="lines+markers",
                name=region,
                legendgroup=region,
                showlegend=show_legend,
                marker_color=color,
                line=dict(color=color),
                visible=is_visible,
                # hovertemplate='%{text}'),
            )

    def _get_figure(self): 
        regions = self.df["regionName"].unique().tolist()

        # for now use aggrnyl
        colorscale = "aggrnyl"

        region_to_colors = {}
        #sampled_colors = list(sample_colorscale(colorscale, len(regions)))
        for i, region in enumerate(regions):
            # compute average % of region
            mean_region = self.df.loc[self.df["regionName"] == region,'elapsedTime'].mean()
            mean_implicit =  self.df.loc[self.df["regionName"]==TALP_IMPLICIT_REGION_NAME,'elapsedTime'].mean()
            percentage =  mean_region / mean_implicit
            alpha = np.single(np.sqrt(percentage)+0.2)
            alpha = np.clip(alpha,0,1)
            region_to_colors[region] = f"rgba({np.random.randint(0,255)}, {np.random.randint(0,255)}, {np.random.randint(0,255)}, {alpha.round(2)})"
        
        # Create Big figure
        fig = make_subplots(
            rows=4,
            cols=6,
            specs=[
                [{"colspan": 6}, None, None, None, None, None],  # elapsed
                [
                    {"colspan": 2, "rowspan": 2},
                    None,
                    {"colspan": 4},
                    None,
                    None,
                    None,
                ],  # IPC pe
                [None, None, {"colspan": 2}, None, {"colspan": 2}, None],  # Comm LB
                [None, None, None, None, {}, {}],  # LB in / out
            ],
            horizontal_spacing=0.05,
            #subplot_titles=[TALP_METRIC_TO_NAME_MAP[metric] for metric in metrics],
            print_grid=False,
        )
        # Elapsed time
        metric = "elapsedTime"
        for region in regions:
            fig.add_trace(
                self.__get_scatter(region, metric, region_to_colors[region], True),
                col=1,
                row=1,
            )
        fig["layout"]["yaxis"]["title"] = "Time in [s]"

        # IPC
        metric = "IPC"
        for region in regions:
            fig.add_trace(
                self.__get_scatter(region, metric, region_to_colors[region]),
                col=1,
                row=2,
            )
        fig["layout"]["yaxis2"]["title"] = "IPC"

        # Parallel Effiency
        metric = "parallelEfficiency"
        for region in regions:
            fig.add_trace(
                self.__get_scatter(region, metric, region_to_colors[region]),
                col=3,
                row=2,
            )
        fig["layout"]["yaxis3"]["title"] = "Efficiency [0-1]"

        # communicationEfficiency
        metric = "mpiCommunicationEfficiency"
        for region in regions:
            fig.add_trace(
                self.__get_scatter(region, metric, region_to_colors[region]),
                col=3,
                row=3,
            )
        fig["layout"]["yaxis4"]["title"] = "Efficiency [0-1]"

        # LoadBalance
        metric = "mpiLoadBalance"
        for region in regions:
            fig.add_trace(
                self.__get_scatter(region, metric, region_to_colors[region]),
                col=5,
                row=3,
            )
        fig["layout"]["yaxis5"]["title"] = "Efficiency [0-1]"

        # Lb in
        metric = "mpiLoadBalanceIn"
        for region in regions:
            fig.add_trace(
                self.__get_scatter(region, metric, region_to_colors[region]),
                col=5,
                row=4,
            )
        fig["layout"]["yaxis6"]["title"] = "Efficiency [0-1]"

        # Lb out
        metric = "mpiLoadBalanceOut"
        for region in regions:
            fig.add_trace(
                self.__get_scatter(region, metric, region_to_colors[region]),
                col=6,
                row=4,
            )
        fig["layout"]["yaxis7"]["title"] = "Efficiency [0-1]"

        fig.update_traces(mode="markers+lines")
        return fig
        
    def get_html(self)->str:
        fig = self._get_figure()
        fig.update_layout(
            title="Performance Metrics Evolution",
            legend_title="Regions",
            autosize=True,
            height=1200,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
            font=dict(
                family="Roboto Condensed, monospace",
                # size=18,
            ),
        )
        return fig.to_html(full_html=False)
    
    def write_svg(self,path: Path) ->None:
        fig = self._get_figure()
        fig.update_layout(
            title="Performance Metrics Evolution",
            legend_title="Regions",
            autosize=True,
            height=1200,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
            font=dict(
                family="Roboto Condensed, monospace",
            ),
        )
        fig.write_image(path, engine="kaleido")
    
    def write_png(self,path: Path) ->None:
        fig = self._get_figure()
        fig.update_layout(
            title="Performance Metrics Evolution",
            legend_title="Regions",
            autosize=True,
            height=1200,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
            font=dict(
                family="Roboto Condensed, monospace",
            ),
        )
        fig.write_image(path, engine="kaleido")