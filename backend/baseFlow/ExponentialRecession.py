import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.models.SeparationModel import SeparationModel
from backend.contracts.Bundle import DataBaseFlow
from backend.ptq.PTQ import PTQ

class ExponentialRecessionCurve(BaseFlow):
    """
    Classe pour implémenter la méthode de récession exponentielle.
    """
    def __init__(self,separationModel : SeparationModel):

        self.lambda_ = separationModel.lambda_
        self.lag_time = separationModel.lag_time
        self.k = separationModel.k
    
    def compute(self, ptq : PTQ):
        precip = np.asarray(ptq.p)
        q_obs = np.asarray(ptq.daily_qobs_mean())
        q_rec = np.zeros_like(precip)
        dates = ptq.dates

        is_dry = (np.round(precip,3) == 0).astype(int)
        diff = np.diff(np.concatenate(([0], is_dry, [0])))
        starts = np.where(diff == 1)[0]
        ends = np.where(diff == -1)[0]
        alpha = 1-self.lambda_
        for start, end in zip(starts, ends):
            length = end - start
            if length >= self.lag_time:
                t = np.arange(length) + 1
                q_rec[start:end] = (-alpha*self.k*t)**(1/alpha)
        return q_rec
    
    def calibration_routine(self,data : DataBaseFlow):
        return self.compute(data['ptq'])
    
    def validation_routine(self,data : DataBaseFlow):
        return self.compute(data['ptq'])
        
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
