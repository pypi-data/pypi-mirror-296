from typing import List, Union
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
from talp_pages.io.run_folders import RunFolder
from talp_pages.talp_common import TALP_JSON_TIMESTAMP_KEY,TALP_JSON_METADATA_KEY,ExecutionMode

import logging
from enum import Enum

TALP_VERSION_KEY="dlbVersion"
TALP_PAGES_DEFAULT_REGION_NAME = "Application"





def detect_execution_mode(df) -> ExecutionMode:
    # First check if for all its 1
    total_threads = df['totalNumCpus'] - df['totalNumMpiRanks']
    if df['totalNumCpus'].sum() == len(df['totalNumCpus']):
        # Only 1 totalNumCpu per entry -> all entries are serial
        return ExecutionMode.SERIAL
    elif df['totalNumMpiRanks'].sum() == 0:
        # Not all runs are serial, but no MPI Ranks: 
        return ExecutionMode.OPENMP
    elif total_threads.sum() == 0:
        # We have MPI Ranks, but no additional CPUs #TODO Think of LeWI
        return ExecutionMode.MPI
    else: 
        return ExecutionMode.HYBRID



def __load_talp_json_3_5(json_input,json_path):
    TALP_JSON_POP_METRICS_KEY = "popMetrics"
    TALP_RESOURCES_KEY = "resources"
    
    
    # we do this a bit ugly for now and reorganize the json a bit: 
    for region in json_input[TALP_JSON_POP_METRICS_KEY].keys():
        json_input[TALP_JSON_POP_METRICS_KEY][region]['regionName'] = region   

    df = pd.DataFrame(json_input[TALP_JSON_POP_METRICS_KEY].values())
    try:
        df['timestamp'] = pd.to_datetime(json_input[TALP_JSON_TIMESTAMP_KEY])
    except KeyError:
        df['timestamp']=pd.to_datetime(datetime.now())
        logging.critical(f"Could not read {TALP_JSON_TIMESTAMP_KEY} key in {json_path}. Using current time instead")
    try:
        #TODO metadata expansion here
        df['metadata'] = json.dumps(json_input[TALP_JSON_METADATA_KEY])
    except KeyError:
        df['metadata'] = json.dumps({})
    try:
        resources = json_input[TALP_RESOURCES_KEY]
        num_cpus = resources['numCpus']
        num_mpi_ranks = resources['numMpiRanks']
        df['totalNumCpus']=num_cpus
        df['totalNumMpiRanks']=num_mpi_ranks
    except:
        df['totalNumCpus']=0
        df['totalNumMpiRanks']=0
    
    df['dlbVersion'] = "3.5"
    df['jsonFile'] = str(json_path)
    df['DEFAULT_REGION_NAME'] = TALP_PAGES_DEFAULT_REGION_NAME

    # Compute some additional data
    
    invalid_cycles=df['cycles'] < 0
    invalid_instructions=df['instructions'] < 0
    # CLAMP cycles and instructions
    df.loc[invalid_cycles,'cycles'] = 0
    df.loc[invalid_instructions,'instructions'] = 0
    df['IPC'] = df['instructions'] / df['cycles']
    df.loc[invalid_cycles | invalid_instructions,'IPC'] = 0
    df['frequency'] =  (df['cycles'] / df['usefulTime'])
    # Normalize to seconds
    df["elapsedTime"] = df["elapsedTime"] * 1e-9

    execution_mode = detect_execution_mode(df)
    if execution_mode == ExecutionMode.HYBRID: 
        # Then we do the X
        df['totalThreads'] = (df.loc[:,'totalNumCpus'] / df.loc[:,'totalNumMpiRanks']).astype(int)
        df['ressourceLabel'] = df.loc[:,'totalNumMpiRanks'].astype(str) + "xMPI " + df.loc[:,'totalThreads'].astype(str) +"xOpenMP"
    elif execution_mode == ExecutionMode.SERIAL:
        df['ressourceLabel'] = ExecutionMode.SERIAL.value
    else:
        df['ressourceLabel'] = df.loc[:,'totalNumCpus'].astype(str) + f"x{execution_mode.value}"
    
    df['executionMode'] = execution_mode.value
    # finally sort
    df = df.sort_values(by=["elapsedTime"], ascending=False)
    return df



def load_talp_json_df(json_path: Path) -> pd.DataFrame:
    with open(json_path) as file:
        run_json = json.load(file)
        df = None
        # First check version
        if run_json[TALP_VERSION_KEY] in ["3.5","3.5a"]:
            df = __load_talp_json_3_5(run_json,json_path)
        else:
            raise Exception(f"Unable to find parser for {run_json[TALP_VERSION_KEY]}. Please update your talp-pages instance.")

        
        return df

def get_dfs(run_folders: List[RunFolder], as_list=True) -> Union[List[pd.DataFrame],pd.DataFrame] :
    dfs_outer =[]
    for run_folder in run_folders:
        dfs_inner = []
        for json_entry in run_folder.jsons:
            df = load_talp_json_df(json_entry)
            df['runFolder'] = str(run_folder.relative_path)
            dfs_inner.append(df)
            
        # Now combine the inner semantically clustered jsons and add to list 
        df_of_run_folder = pd.concat(dfs_inner)
        dfs_outer.append(df_of_run_folder)

    if as_list:
        return dfs_outer
    else:
        return pd.concat(dfs_outer)

