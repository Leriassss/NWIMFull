from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from backend.contracts.Bundle import DataBaseFlow
from backend.baseFlow.models.LyneHollickModel import LyneHollickModel

import numpy as np


class LyneHollick(BaseFlowRoutine, BaseFlow):
    """
    Classe pour implémenter la méthode de récession Chapman.
    """
    def __init__(self, lyneHollickModel: LyneHollickModel):
        self.k = lyneHollickModel.k

        self.a,self.b,self.correc_factor = 0, 0, 0

    def compute(self,flow_series):
        """
        Implémente la méthode de séparation des écoulements selon la méthode de Chapman.
        
        Args:
            flow_series : Série temporelle des débits de rivières (Yk).
            alpha (float) : Coefficient alpha (par défaut 0.925).
            
        Returns:
            np.array : Série des débits de base (Qk).
        """
        Q_base = np.zeros_like(flow_series)
        for k in range(1, len(flow_series)):
            Q_base[k] = self.k*Q_base[k-1] +  (1+self.k)*(flow_series[k]-flow_series[k-1])/2

        return np.maximum(0,Q_base)


    def reverse_compute(self,previous_qbase, Q_direct):
        
        Q_base_rev = np.zeros(len(Q_direct))
        Q_base_rev[0]  = previous_qbase
        for k in range(1, len(Q_direct)):
            Q_base_rev[k] = Q_base_rev[k-1] + (1+self.k)*(Q_direct[k]-Q_direct[k-1])/(1-self.k)
        return np.maximum(0,Q_base_rev)

    def calibration_routine(self,data : DataBaseFlow):
        qbase = self.compute(data["qObs"])
        qbase_previous = self.get_qbase_previous(data,qbase)
        qbase_rev = self.reverse_compute(qbase_previous, data['qsim'])
        
        qbase_rev_corr = self.get_qbase_rev_corr(qbase_rev,qbase)
        return qbase_rev_corr
    
    def validation_routine(self, data : DataBaseFlow):
        #DETERMINATION DU DEBIT DE BASE PRECEDENT
        q_base_previous = self.modele_baseflow(data["prevObs"], self.a, self.b)
        #CALCUL DU DEBIT DE BASE PAR LA METHODE REVERSE
        qbase_rev = self.reverse_compute(q_base_previous, data['qsim'])
        return qbase_rev
    

    @staticmethod
    def help():
        pass