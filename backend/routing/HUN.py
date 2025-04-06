
import numpy as np
import pandas as pd
from backend.contracts.Bundle import DataSimulation, RoutingContract

from backend.routing.Routing import Routing
from backend.routing.models.HUNModel import HUNModel

from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from permetrics.regression import RegressionMetric

class HUN(Routing):
    def __init__(self,kwargs: RoutingContract):
        self.kwargs = kwargs
        self.hunModel = HUNModel(*self.kwargs)
        self.hun = []
        self.datas_calage = []
        self.qbase_ratio = []
        
    def calage(self,datas : DataSimulation): 
        self.datas_calage  = datas
        interm_hun = []
        production = datas["pn"]
        time_base = self.hunModel.time_base
        dt = self.hunModel.dt
        q_direct = np.maximum(0,datas["qobs"] - datas["qbase"])

        seq_hun = np.arange(0,q_direct.count(),time_base)
        hun_time_base = []
        for k in seq_hun:
            production_seq = production[k:k+time_base]
            q_direct_seq = q_direct[k:k+time_base]
            if production_seq.sum()>0:
                hun_k = np.array(q_direct_seq/(production_seq.sum()))
            else:
                hun_k = np.zeros_like(q_direct_seq)
            interm_hun.append(pd.Series(hun_k.copy()))
            hun_time_base.append(pd.Series(np.convolve(production_seq,hun_k))[:len(production_seq)]*dt)
        self.hun = pd.concat(interm_hun).reset_index(drop=True)
        q_sim_direct =  pd.concat(hun_time_base).reset_index(drop=True)[:len(production)]
        return q_sim_direct
        
        #self.qbase_ratio = self.qbase_routine(datas["dates"], q_sim_direct, datas["qbase"])
        
        #return np.maximum(0,q_sim_direct + self.qbase_ratio["Q_base_corr"] )
        #self.regBaseFlow(datas["qbase"], datas["qobs"])
            
    def validation(self,datas : DataSimulation):
        self.calage(self.datas_calage)
        hun_ = self.hun.copy()
        production = datas["pn"]
        time_base = self.hunModel.time_base
        dt = int(self.hunModel.dt)
        seq_hun = np.arange(0,len(production),time_base)
        hun_time_base = []        
        for k in seq_hun:
            production_seq = production[k:k+time_base]
            hun_seq = hun_[k:k+time_base]
            hun_time_base.append(pd.Series(np.convolve(production_seq,hun_seq))[:time_base]*dt)
        q_sim_direct =  pd.concat(hun_time_base).reset_index(drop=True)[:len(production)]
        return np.maximum(0, q_sim_direct + datas["qbase"])
    

    @staticmethod
    def help():
        """
        Fournit une description des méthodes disponibles dans la classe Recession.
        """
        description = """
        Implémente l'Hydrogramme unitaire
        """
        print(description)
