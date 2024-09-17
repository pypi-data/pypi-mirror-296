import pandas as pd
from pathlib import Path
from talp_pages.talp_common import HighlightedRegions,TALP_METRIC_TO_NAME_MAP,TALP_METRIC_TO_NESTING_MAP
from talp_pages.talp_common import ExecutionMode
from enum import Enum
from typing import List,Tuple
import logging
import plotly.express as px

pd.options.mode.chained_assignment = None

import numpy as np


import plotly.graph_objects as go
from plotly.colors import n_colors
from plotly.colors import sample_colorscale
class ScalingMode(Enum):
    WEAK = "Weak Scaling"
    STRONG = "Strong Scaling"



# Assume ordered list
def detect_scaling_mode(dfs:List[pd.DataFrame]) -> ScalingMode:
    # Assume a ordered list where the ressource with the lowest is the first
    # Use instructions to estimate the weak or strong scaling
    # Assumption: IFF Weak scaling the number of instructions/totalNumCpus should be roughly the same within a bound of +- 50%
    # Default mode. Strong
    if not dfs:
        return ScalingMode.STRONG

    base_case = dfs[0]

    if base_case['instructions'].values[0] <= 0: 
        logging.warning(f"Unable to detect ScalingMode, as no instructions are available. Run with PAPI. Assuming {ScalingMode.STRONG}")
        return ScalingMode.STRONG

    # Assume Weak scaling -> if condition violated to strong scaling
    for df in dfs:
        instruction_growth =df['instructions'].to_numpy() / base_case['instructions'].to_numpy()
        cpu_growth = df['numCpus'].to_numpy() / base_case['numCpus'].to_numpy()

        if (instruction_growth / cpu_growth) < 0.75:
            logging.debug(f"ScalingMode found to be Strong as {instruction_growth / cpu_growth} < 0.75")
            return ScalingMode.STRONG

    return ScalingMode.WEAK
            
      
    

def compute_scaling_metrics(df: pd.DataFrame,region) -> Tuple[pd.DataFrame, pd.DataFrame,List[pd.DataFrame]]:
    # Computes the scaling metrics and returns a tuple with the first beeing just the basic_anylsis like table 
    # and the second one being a ordered list of the dataframes making up the BA table. 
    df_copy = df.copy(deep=True)
   
    clean_df = df_copy.loc[df_copy['regionName'] == region]
    if clean_df.empty:
        raise ValueError("Region not available")

    
    ressource_combinations = clean_df.sort_values(by='totalNumCpus')['ressourceLabel'].drop_duplicates().to_numpy()
    df_datapoints = []
    for combination in  ressource_combinations:
        datapoint = clean_df.loc[clean_df['ressourceLabel'] == combination].sort_values(by=["timestamp"], ascending=False).head(1)
        df_datapoints.append(datapoint)
    if not df_datapoints:
        logging.error(f"Not able to compute the scaling metrics for dataframe: {clean_df}")
        #return (pd.DataFrame(),[])
    
    scaling_mode = detect_scaling_mode(df_datapoints)

    clean_df.loc[:,"scalingMode"] = scaling_mode.value

    reference_case = df_datapoints[0]
    if scaling_mode==ScalingMode.STRONG:
        #Assume instructions stay constant 
        clean_df['instructionScaling'] = (reference_case['instructions'] / clean_df.loc[:,'instructions'])
    if scaling_mode == ScalingMode.WEAK:
        # optimal behavior: iWnstructions 
        clean_df['instructionScaling'] = (reference_case['instructions']/reference_case['numCpus']) * (1/(clean_df['instructions']/clean_df['numCpus']))
    clean_df.loc[:,'ipcScaling']= clean_df.loc[:,'IPC'] / reference_case['IPC']

    clean_df.loc[:,'frequencyScaling'] =clean_df.loc[:,'frequency'] / reference_case['frequency']
    clean_df.loc[:,'computationScalability']= clean_df['instructionScaling'] * clean_df['ipcScaling'] *  clean_df['frequencyScaling']
    clean_df.loc[:,'globalEfficiency'] = clean_df.loc[:,'parallelEfficiency'] * clean_df.loc[:,'computationScalability']
    clean_df.loc[:,'speedup'] = reference_case['elapsedTime'] / clean_df['elapsedTime']
    clean_df.loc[:,'globalEfficiencyBySpeedup'] = clean_df.loc[:,'speedup'] / (clean_df.loc[:,'numCpus'] / reference_case['numCpus'])
            
    df_datapoints = []
    for combination in  ressource_combinations:
        datapoint = clean_df[clean_df['ressourceLabel'] ==combination].sort_values(by=["timestamp"], ascending=False).head(1)
        df_datapoints.append(datapoint)
    return (clean_df,pd.DataFrame(),df_datapoints)
        

class ScalingView:
    def __init__(self,dataframe : pd.DataFrame):
        self.df = dataframe


    def _get_table(self,clean_df,df_datapoints):

        ressource_combinations = clean_df.sort_values(by='totalNumCpus')['ressourceLabel'].drop_duplicates().to_numpy()

        
        if ExecutionMode.HYBRID.value in clean_df['executionMode'].to_numpy():
            eff_metrics=['globalEfficiency','parallelEfficiency',
                     'mpiParallelEfficiency','mpiCommunicationEfficiency','mpiLoadBalance','mpiLoadBalanceIn','mpiLoadBalanceOut',
                     'ompParallelEfficiency','ompSchedulingEfficiency','ompLoadBalance','ompSerializationEfficiency',
                    'computationScalability',
                     'instructionScaling','ipcScaling','frequencyScaling']
            abs_metrics=['IPC','frequency','elapsedTime']


        if ExecutionMode.MPI.value in clean_df['executionMode'].to_numpy():
            eff_metrics=['globalEfficiency','parallelEfficiency',
                     'mpiParallelEfficiency','mpiCommunicationEfficiency','mpiLoadBalance','mpiLoadBalanceIn','mpiLoadBalanceOut',
                     'computationScalability',
                     'instructionScaling','ipcScaling','frequencyScaling']
            abs_metrics=['IPC','frequency','elapsedTime']
        
        if ExecutionMode.OPENMP.value in clean_df['executionMode'].to_numpy():
            eff_metrics=['globalEfficiency','parallelEfficiency',
                     'ompParallelEfficiency','ompSchedulingEfficiency','ompLoadBalance','ompSerializationEfficiency',
                     'computationScalability',
                     'instructionScaling','ipcScaling','frequencyScaling']
            abs_metrics=['IPC','frequency','elapsedTime']
        
        if ExecutionMode.SERIAL.value in clean_df['executionMode'].to_numpy():
            eff_metrics=['globalEfficiency',
                     'computationScalability',
                     'instructionScaling','ipcScaling','frequencyScaling']
            abs_metrics=['IPC','frequency','elapsedTime']

        
        metrics = eff_metrics+abs_metrics

        header = ["Metrics"]
        header.extend([f"<b>{combination}</b>" for combination in ressource_combinations])
        aligns= ["left"]
        aligns.extend(["center" for metric in metrics ])
        values = [[f"{'-'*TALP_METRIC_TO_NESTING_MAP[metric]} {TALP_METRIC_TO_NAME_MAP[metric]}" for metric in metrics]]
        numeric_values = [datapoint[metrics].to_numpy().squeeze().round(2) for datapoint in df_datapoints]
        values.extend(numeric_values)
        
        colors = [np.full_like(metrics,'rgb(250, 250, 250)').squeeze()]
       
        colors.extend([sample_colorscale('rdylgn',np.clip(numeric_value,0,1),low=0.0,high=1.0) for numeric_value in numeric_values])
        # reset color for absolute metrics
        for col in colors[1:]:
            col[len(eff_metrics):len(metrics)]=['rgb(250, 250, 250)' for metric in abs_metrics]
        
        fig = go.Figure(data=[go.Table(
        header=dict(
            values=header,
            #line_color='white', fill_color='white',
            align=aligns,
            font=dict(color='black', size=20)
        ),
        cells=dict(
            values=values,
            line_color=colors,
            fill_color=colors,
            height=30,
            align=aligns,
            font=dict(color='black', size=16)
            ))
        ])
        return fig



    def _get_figure(self, region):
        logging.debug(f"get_figure {region}")
        # First build up the ressource list
        clean_df,df_return,df_datapoints= compute_scaling_metrics(self.df,region)
        
      
        ressource_combinations = clean_df.sort_values(by='totalNumCpus')['ressourceLabel'].drop_duplicates().to_numpy()

        
        
        if ExecutionMode.HYBRID.value in clean_df['executionMode'].to_numpy():
            metrics=['globalEfficiency','globalEfficiencyBySpeedup', 'parallelEfficiency', 'computationScalability',
                     'mpiParallelEfficiency','mpiCommunicationEfficiency','mpiLoadBalance','mpiLoadBalanceIn','mpiLoadBalanceOut',
                     'ompParallelEfficiency','ompSchedulingEfficiency','ompLoadBalance','ompSerializationEfficiency',
                     'instructionScaling','ipcScaling','frequencyScaling', 'elapsedTime','speedup']

        if ExecutionMode.SERIAL.value in clean_df['executionMode'].to_numpy():
            metrics=['globalEfficiency','computationScalability']
        

        metrics_labels = [TALP_METRIC_TO_NAME_MAP[metric] for metric in metrics]

        data = np.zeros((len(metrics),len(ressource_combinations)))
        
        


        for i,datapoint in enumerate(df_datapoints):
            data[:,i]= datapoint[metrics].to_numpy()


        data_text = data.round(2).astype('str')
   

        fig = px.imshow(data, x=ressource_combinations, y=metrics_labels, color_continuous_scale='RdYlGn', aspect="auto",zmin=0,zmax=1)
        fig.update_traces(text=data_text, texttemplate="%{text}")
        fig.update_xaxes(side="top")

        figure_substring=""
        # construct data string
        for datapoint in df_datapoints:
            figure_substring += f"{datapoint['ressourceLabel'].values[0]}: {datapoint['json_file'].values[0]}<br>"
        fig.update_layout(
            title=f"Performance Scaling of Region:{region} assuming {scaling_mode.value}<br> <sup>{figure_substring}</sup>"
        )
        return fig
    
    def get_dfs(self,region):
        return compute_scaling_metrics(self.df,region)
    def get_html(self,region:str)->str:
        clean_df,df_return,df_datapoints= compute_scaling_metrics(self.df,region)

        fig = self._get_table(clean_df,df_datapoints)
        fig.update_layout(
            autosize=True,
            height=650,
            margin=dict(l=50, r=50, b=0, t=0, pad=4),
            font=dict(
                family="Roboto Condensed, monospace",
                # size=18,
            ),
        )
        return fig.to_html(full_html=False)
    
    def write_svg(self,path: Path,region:str) ->None:
        fig = self._get_figure(region)
        fig.update_layout(
            autosize=True,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
            font=dict(
                family="Roboto Condensed, monospace",
                # size=18,
            ),
        )
        fig.write_image(path, engine="kaleido")
    
    def write_png(self,path: Path,region:str) ->None:
        fig = self._get_figure(region)
        fig.update_layout(
            legend_title="Regions",
            autosize=True,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
            font=dict(
                family="Roboto Condensed, monospace",
            ),
        )
        fig.write_image(path, engine="kaleido")