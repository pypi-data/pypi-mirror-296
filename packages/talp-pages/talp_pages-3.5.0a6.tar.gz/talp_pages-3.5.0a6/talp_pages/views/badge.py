import pandas as pd
import logging
from talp_pages.talp_common import TALP_IMPLICIT_REGION_NAME

from urllib.request import urlopen, Request
class Badge():
    def __init__(self,df:pd.DataFrame,ressource_label:str,region_for_badge:str) -> None:
        ressource_label_matching = df['ressourceLabel'] == ressource_label
        region_matching= df['regionName'] == region_for_badge
        if df.loc[ressource_label_matching & region_matching].empty:
            logging.warning(f"Unable to find region {region_for_badge} in {ressource_label} for {df['runFolder'].head(1)}. Continuing with region: {TALP_IMPLICIT_REGION_NAME}")
            region_for_badge = TALP_IMPLICIT_REGION_NAME
            region_matching= df['regionName'] == region_for_badge
            
        self.df = df.loc[ressource_label_matching & region_matching]
        

        
    def get_content(self):
        parallel_efficiency = self.df.sort_values(by=["timestamp"], ascending=False).loc[:,'parallelEfficiency'].head(1).values[0]

        if not parallel_efficiency:
            logging.error(f"Couldnt compute parallel_efficiency for badge. Expect wrong bagdes")
            parallel_efficiency = 0

        if parallel_efficiency < 0.6:
            bagde_url = f"https://img.shields.io/badge/Parallel_efficiency-{parallel_efficiency}-red"
        elif parallel_efficiency < 0.8:
            bagde_url = f"https://img.shields.io/badge/Parallel_efficiency-{parallel_efficiency}-orange"
        else:
            bagde_url = f"https://img.shields.io/badge/Parallel_efficiency-{parallel_efficiency}-green"

        return urlopen(Request(url=bagde_url, headers={"User-Agent": "Mozilla"})).read().decode('utf-8')