import pandas as pd
from pathlib import Path

class BaseView():
    def __init__(self,dataframe: pd.DataFrame) -> None:
        self.df = dataframe
    
    def get_html(self) -> str:
        raise NotImplementedError

    def write_svg(self,path: Path) ->None:
        raise NotImplementedError

    def write_png(self,path: Path) ->None:
        raise NotImplementedError