from typing import Dict, TypedDict, List

import pandas as pd
from backend.ptq.PTQ import PTQ

class RoutingData(TypedDict):
    pn: Dict[str, List[float]]
    qb: Dict[str, List[float]]
    sim: Dict[str, List[float]]
    loss: Dict[str, List[float]]

class SimulationMethodsData(TypedDict):
    production : str
    recession : str
    routing : str
    initial_loss : str

class DataSimulation(TypedDict):
    pn : pd.Series
    qbase : pd.Series
    qobs : pd.Series 
    dates : pd.Series

class DataBaseFlow(TypedDict):
    qsim : pd.Series
    qbase : pd.Series
    ptq : PTQ
    qmean : pd.Series

class DataInitialLoss(TypedDict):
    net_rainfall : pd.Series
    etp : pd.Series

class RoutingContract(TypedDict):
    sim: Dict[str, List[float]]