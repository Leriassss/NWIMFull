import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.contracts.Bundle import DataBaseFlow
from backend.ptq.PTQ import PTQ
class HUNBaseFlow(BaseFlow):
    """
    Classe pour implémenter la méthode de récession exponentielle.
    
    def __init__(self,separationModel : SeparationModel):

        self.lambda_ = separationModel.lambda_
        self.lag_time = separationModel.lag_time
        self.k = separationModel.k
    """
    def __init__(self):
        super().__init__()
        self.hun = []
    
    def compute(self):
        pass


    def chapman_computing(self, flow_series):
        alpha = 0.925
        Q_base = flow_series.copy()
        factor1 = (3 * alpha - 1) / (3 - alpha)
        factor2 = (1 - alpha) / (3 - alpha)
        
        for k in range(1, len(flow_series)):
            Q_base[k] = (
                factor1 * Q_base[k - 1]
                + factor2 * (flow_series[k] + flow_series[k - 1])
            )

        return Q_base
        
    def calage(self,time_base,initial_production, flow_series):        
        transformed_production = pd.Series(np.where(np.round(initial_production, 1) == 0, 1, initial_production))
        q_direct = self.chapman_computing(flow_series)

        seq_hun = np.arange(0,len(q_direct),time_base)
        hun_time_base = []
        interm_hun = []
        for k in seq_hun:
            initial_production_seq = initial_production[k:k+time_base]
            transformed_production_seq = transformed_production[k:k+time_base]
            q_direct_seq = q_direct[k:k+time_base]
            hun_k = pd.Series(q_direct_seq/(transformed_production_seq.sum()))
            interm_hun.append(hun_k)
            hun_time_base.append(pd.Series(np.convolve(initial_production_seq,hun_k))[:len(initial_production_seq)])
        self.hun = pd.concat(interm_hun).reset_index(drop=True)
        q_sim_direct =  pd.concat(hun_time_base).reset_index(drop=True)[:len(initial_production)]

        q_sim_direct = q_sim_direct.rolling(window=5, center=True, min_periods=time_base).mean()
        return q_sim_direct 
            
    def validation(self,time_base,production):
        hun_ = self.hun
        seq_hun = np.arange(0,len(production),time_base)
        hun_time_base = []        
        for k in seq_hun:
            production_seq = production[k:k+time_base]
            hun_seq = hun_[k:k+time_base]
            hun_time_base.append(pd.Series(np.convolve(production_seq,hun_seq))[:time_base])
        q_sim_direct =  pd.concat(hun_time_base).reset_index(drop=True)[:len(production)]
        
        q_sim_direct = q_sim_direct.rolling(window=5, center=True, min_periods=1).mean()
        return np.maximum(0, q_sim_direct)
      
 
    def reverse_compute(self):
        pass
    
        
    @staticmethod
    def help():
        """
        Fournit une description des méthodes disponibles dans la classe Recession.
        """
        description = """
        Implémente le filtre de récession de Furey-Gupta.


        Arguments pour `furey_gupta`:
        - flow_series : Série temporelle des débits [mm/jour] (pd.Series ou np.ndarray).
        - gamma : Coefficient de récession (par défaut 0.03).
        - cs_over_c : Ratio des coefficients (par défaut 1.1).
        """
        print(description)
