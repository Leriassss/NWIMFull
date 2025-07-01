import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.contracts.Bundle import DataBaseFlow
from backend.ptq.PTQ import PTQ
class RatioBaseFlow(BaseFlow):
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

    def calage(self,Qr : pd.Series, Qb: pd.Series):
        Qr = Qr.fillna(0)
        Qb = Qb.fillna(0)
        def ratio_row(qr, qb):
            if qr == 0 and qb > 0:
                return qb
            elif qb == 0:
                return 0
            else:
                return qr / qb
        self.hun = pd.Series([ratio_row(qr, qb) for qr, qb in zip(Qr, Qb)], index=Qr.index)
        
        return  (Qr/self.hun).rolling(window=5, center=True, min_periods=1).mean()


            
    def validation(self,Qr : pd.Series):
        print("VALIDATION //// ------ ")
        print(Qr)
        return  (Qr/self.hun[:len(Qr)]).rolling(window=5, center=True, min_periods=1).mean()

      
 
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
