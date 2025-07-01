
import numpy as np
import pandas as pd
from backend.contracts.Bundle import DataSimulation, RoutingContract

from backend.routing.Routing import Routing
from backend.routing.models.HUNModel import HUNModel

class HUN(Routing):
    def __init__(self,kwargs: RoutingContract):
        self.kwargs = kwargs
        self.hunModel = HUNModel(*self.kwargs)
        
    def calage(self,datas : DataSimulation): 
        return self.compute_hun(datas)
            
    def validation(self,datas : DataSimulation):
        return self.compute_hun(datas) 
    
    def compute_hun(self,datas : DataSimulation):
        transformed_production = pd.Series(np.where(np.round(datas["pn"], 0) == 0, 1, datas["pn"]))
        initial_production = datas["pn"]
        time_base = self.hunModel.time_base
        q_direct = datas["qdirect_means"]
        seq_hun = np.arange(0,len(q_direct),time_base)
        hun_time_base = []
        interm_hun = []
        xtra_flow = np.zeros(time_base-1)
        for k in seq_hun:
            initial_production_seq = initial_production[k:k+time_base]
            len_ips = len(initial_production_seq)
            transformed_production_seq = transformed_production[k:k+time_base]
            q_direct_seq = q_direct[k:k+time_base]
            hun_k = q_direct_seq/(transformed_production_seq.sum())
            interm_hun.append(pd.Series(hun_k))
            total_sim = np.convolve(initial_production_seq,hun_k)
            sim_flow = total_sim[:len_ips]    
            sim_flow[:len(xtra_flow)] += xtra_flow[:len(sim_flow)]
            xtra_flow = total_sim[len_ips:]
            hun_time_base.append(pd.Series(sim_flow))
        q_sim_direct =  pd.concat(hun_time_base).reset_index(drop=True)[:len(initial_production)]
        return q_sim_direct


    @staticmethod
    def help():
        """
        Fournit une description des méthodes disponibles dans la classe Recession.
        """
        description = """
        Implémente l'Hydrogramme unitaire
        """
        print(description)
