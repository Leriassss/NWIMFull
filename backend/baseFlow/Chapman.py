from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from backend.baseFlow.models.ChapmanModel import ChapmanModel
from backend.contracts.Bundle import DataBaseFlow

import numpy as np
import pandas as pd

from backend.ptq.PTQ import PTQ
class Chapman(BaseFlow):
    """
    Classe pour implémenter la méthode de récession Chapman.
    """
    def __init__(self, chapmanModel : ChapmanModel):
        self.alpha = chapmanModel.alpha
        self.a,self.b = 0, 0
        self.correc_factor = None

    def compute(self, ptq : PTQ):
        """
        Implémente la méthode de séparation des écoulements selon la méthode de Chapman.
        
        Args:
            flow_series : Série temporelle des débits de rivières (Yk).
            alpha (float) : Coefficient alpha (par défaut 0.925).
            
        Returns:
            np.array : Série des débits de base (Qk).
        """
        flow_series = ptq.q
        Q_base = flow_series.copy()
        factor1 = (3 * self.alpha - 1) / (3 - self.alpha)
        factor2 = (1 - self.alpha) / (3 - self.alpha)
        
        for k in range(1, len(flow_series)):
            Q_base[k] = (
                factor1 * Q_base[k - 1]
                + factor2 * (flow_series[k] + flow_series[k - 1])
            )

        return Q_base

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
    

    def reverse_compute(self,previous_qbase, Q_direct):
        Q_base_rev = np.zeros(len(Q_direct))
        Q_base_rev[0]  = previous_qbase

        factor1 = ((3 * self.alpha) - 1) / (3 - self.alpha)
        factor2 = (1 - self.alpha) / (3 - self.alpha)

        for k in range(1, len(Q_direct)):
            Q_base_rev[k] = (1/(1-factor2)) * ( Q_base_rev[k-1]*(factor1+factor2) + 
                                            factor2*(Q_direct[k] + Q_direct[k-1]))
        
        return Q_base_rev

