from talp_pages.talp_common import TALP_PAGES_VERSION
import pathlib
from jinja2 import Environment, FileSystemLoader
TALP_PAGES_TEMPLATE_PATH = pathlib.Path(__file__).parent.joinpath("templates").resolve()
from typing import List,Dict
from talp_pages.views.scaling_view import ScalingView
from talp_pages.views.time_series_view import TimeSeriesView
import logging
from datetime import datetime
import pandas as pd
from talp_pages.io.output import RenderedSite, RenderedSiteType,RenderedBadge
class Navbar:
    def __init__(self,links: Dict[str,str]) -> None:
        self.links = links




class HTMLSite:
    def __init__(self,template_name: str) -> None:
        self.page_metadata={'page_metadata':
            {
            'timestamp_string': datetime.now().isoformat(timespec="seconds"),
            'version': TALP_PAGES_VERSION,
            'home': "index.html",
            }
        }
        self.jinja_env = Environment(loader=FileSystemLoader(TALP_PAGES_TEMPLATE_PATH))
        self.template_name = template_name
        self.template =self.jinja_env.get_template(self.template_name)
    

    def render_template(self,**context)->str:
        # Render the template with the provided context
        return self.template.render({**context,**self.page_metadata})



    

    
class ScalingSite(HTMLSite):
    def __init__(self) -> None:
        super().__init__('scaling.jinja')

    def get_content(self,df,regions):
        regions_to_render = []
        configurations = {}
        scaling_mode = "Unkown Scaling Mode"
        latest_change = None
        for region_name in regions:
            configurations[region_name] =[]
            view = ScalingView(df)
            figure = None
            try:
                figure = view.get_html(region_name)
                clean_df,df_return,df_datapoints= view.get_dfs(region_name)
            except ValueError as e: 
                logging.warn(f"Trying to get region with name  {region_name} for scaling analysis but failed. Skipping that region... {e}")
            
            for datapoint in df_datapoints:
                date = pd.to_datetime(datapoint['timestamp'].to_numpy().squeeze())
                try: 
                    if date > latest_change:
                        latest_change = date
                except TypeError:
                    latest_change = date

                configurations[region_name].append(
                    {'label': datapoint['ressourceLabel'].to_numpy().squeeze(),
                     'json_file': datapoint['jsonFile'].to_numpy().squeeze(),
                     'timestamp': date.isoformat(),
                     'metadata': datapoint['metadata'].to_numpy().squeeze()
                    }
                )
                scaling_mode = datapoint['scalingMode'].to_numpy().squeeze()

            
            #except Exception as e:
            #    logging.error(f"Cannot find specified Region {region_name}: {e}")
            #    figure=None
            if figure:
                regions_to_render.append({'name': region_name,'figure': figure})
        
        html = self.render_template(regions=regions_to_render,configurations=configurations,scaling_mode=scaling_mode)
        return latest_change,scaling_mode,html
    


class LandingSite(HTMLSite):
    def __init__(self) -> None:
        super().__init__('landing_page.jinja')

    def get_content(self,other_sites: List[RenderedSite], badges: List[RenderedBadge]):

        sites_dict={}
        sites_metadata={}
        bagdes_dict={}
        badge_region=""
        for badge in badges:
            badge_region=badge.region_for_badge
            bagdes_dict[str(badge.relative_output_path)]=[]

        for badge in badges:
            bagdes_dict[str(badge.relative_output_path)].append({
                'link':f"{badge.relative_output_path}/{badge.filename}",
                'label':f"{badge.ressource_label}",
            })
        for site in other_sites:
            if site.type == RenderedSiteType.SCALING:
                icon = "bi-table"
            elif site.type == RenderedSiteType.TIMESERIES:
                icon = "bi-graph-up"
            else:
                icon = "bi-bar-chart"
        
            try:
                sites_dict[str(site.relative_output_path)].append(
                    {'label':site.label,
                     'icon': icon,
                     'type': site.type.value,
                     'link':f"{site.relative_output_path}/{site.filename}",
                    'newest_data': site.latest_change
                    }
                )
            except KeyError:
               sites_dict[str(site.relative_output_path)] = []
               sites_dict[str(site.relative_output_path)].append(
                    {'label':site.label,
                     'icon': icon,
                     'type': site.type.value,
                     'link':f"{site.relative_output_path}/{site.filename}",
                     'newest_data': site.latest_change
                    }
                )
        for path,pages in sites_dict.items():
            newest_date = max([page['newest_data'] for page in pages])
            sites_metadata[path] = {
                'last_update': newest_date.isoformat(timespec="seconds")
            }
        html = self.render_template(sites_dict=sites_dict,
                                    sites_metadata=sites_metadata,
                                    badges_dict=bagdes_dict,
                                    badge_region=badge_region)
        return html
    

    
class TimeSeriesSite(HTMLSite):
    def __init__(self) -> None:
        super().__init__('time_series.jinja')
    
    def get_content(self,ressource_label,df,regions):
        # clean df
        clean_df = df[df['ressourceLabel'] == ressource_label]
        view = TimeSeriesView(clean_df, regions)
        date = pd.to_datetime(clean_df['timestamp'].max())
        html = self.render_template(figure=view.get_html())
        return date,html