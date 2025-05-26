import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.contracts.Bundle import DataBaseFlow
from backend.ptq.PTQ import PTQ

class IHACRES(BaseFlow):
    """
    Classe pour implémenter la méthode de récession exponentielle.
    
    def __init__(self,separationModel : SeparationModel):

        self.lambda_ = separationModel.lambda_
        self.lag_time = separationModel.lag_time
        self.k = separationModel.k
    """
    
    def compute(self, p_inf, alpha):
        qs = np.zeros_like(p_inf)
        for t in range(1, len(qs)):
            qs = -alpha*qs[t-1]+ (1-alpha)*p_inf
        return qs
        
    
 
    def reverse_compute(self,previous_qbase, Q_direct):
        Q_base_rev = np.zeros(len(Q_direct))
        Q_base_rev[0]  = previous_qbase

        factor1 = ((3 * self.alpha) - 1) / (3 - self.alpha)
        factor2 = (1 - self.alpha) / (3 - self.alpha)

        for k in range(1, len(Q_direct)):
            Q_base_rev[k] = (1/(1-factor2)) * ( Q_base_rev[k-1]*(factor1+factor2) + 
                                            factor2*(Q_direct[k] + Q_direct[k-1]))
        
        return Q_base_rev
    
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
