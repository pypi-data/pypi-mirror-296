"""
File declaring some global scoped variables and functions
"""
from dataclasses import dataclass
from typing import List
from datetime import datetime
from enum import Enum


TALP_PAGES_VERSION = "3.5.0alpha"
TALP_METRIC_TO_NAME_MAP = {
    "globalEfficiency": "Global Effiency",
    "globalEfficiencyBySpeedup": "Global Effiency from Speedup",
    "parallelEfficiency": "Parallel efficiency",
    "computationScalability": "Computation Scalability",
    "averageIPC": "Average IPC",
    "cycles": "Cycles",
    "instructions": "Useful Instructions", 
    "IPC": "Useful IPC",
    "frequency": "Frequency [GHz]",
    "mpiParallelEfficiency": "MPI Parallel efficiency",
    "mpiCommunicationEfficiency": "MPI Communication efficiency",
    "mpiLoadBalance": "MPI Load balance",
    "mpiLoadBalanceIn": "MPI In-node load balance",
    "mpiLoadBalanceOut": "MPI Inter-node load balance",
    "ompParallelEfficiency": "OpenMP Parallel efficiency",
    "ompLoadBalance": "OpenMP Load balance",
    "ompSchedulingEfficiency": "OpenMP Scheduling efficiency",
    "ompSerializationEfficiency": "OpenMP Serialization efficiency",
    "instructionScaling": "Instructions scaling",
    "ipcScaling": "IPC scaling",
    "frequencyScaling": "Frequency scaling",
    "elapsedTime": "Elapsed time [s]",
    "speedup": "Speedup"

}


class ExecutionMode(Enum):
    SERIAL = "Serial"
    OPENMP = "OpenMP"
    MPI = "MPI"
    HYBRID = "Hybrid MPI+OpenMP"


TALP_PAGES_INDEX_PAGE = "index.html"
TALP_PAGES_REPORT_PAGE = "report.html"
TALP_JSON_TIMESTAMP_KEY = "timestamp"
TALP_JSON_METADATA_KEY = "metadata"

TALP_IMPLICIT_REGION_NAME = "Application"

@dataclass
class HighlightedRegions:
    selected_regions: List[str]

@dataclass
class TalpPageMetadata:
    timestamp: datetime
    timestamp_string: str
    version: str

