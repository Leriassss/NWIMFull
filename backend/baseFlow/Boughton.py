
from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.models.BoughtonModel import BoughtonModel
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from backend.contracts.Bundle import DataBaseFlow
import numpy as np
import pandas as pd

class Boughton(BaseFlowRoutine, BaseFlow):
    """
    Classe pour implémenter la méthode de récession Furey-Gupta.
    """
    def __init__(self, boughtonModel : BoughtonModel):
        self.k = boughtonModel.k
        self.c = boughtonModel.c

    def compute(self, flow_series, previous_qbase):
        Q_base = np.zeros_like(flow_series)
        Q_base[0] = previous_qbase
        for k in range(1, len(flow_series)):
            Q_base[k] =  np.fmax(0,(self.k*Q_base[k-1]/ (1+self.c)) + self.c * flow_series[k]/(1+self.c))
        return np.maximum(0, Q_base)
    

    def reverse_compute(self,previous_qbase, Q_direct):
        
        Q_base_rev = np.zeros(len(Q_direct))
        Q_base_rev[0]  = previous_qbase
        
        for k in range(1, len(Q_direct)):
            Q_base_rev[k] = (self.k)*Q_base_rev[k-1] + self.c*Q_direct[k]
        return Q_base_rev
    
    def calibration_routine(self,data : DataBaseFlow):
        qbase = self.compute(data["qObs"], data['prevObs'])
        qbase_previous = self.get_qbase_previous(data,qbase)
        qbase_rev = self.reverse_compute(qbase_previous, data['qsim'])
        qbase_rev_corr = self.get_qbase_rev_corr(qbase_rev,qbase)
        return qbase_rev_corr
    
    def validation_routine(self, data : DataBaseFlow):
        #DETERMINATION DU DEBIT DE BASE PRECEDENT
        q_base_previous = self.modele_baseflow(data["prevObs"], self.a, self.b)
        #CALCUL DU DEBIT DE BASE PAR LA METHODE REVERSE
        qbase_rev = self.reverse_compute(q_base_previous, data['qsim'])
        qbase_rev_corr = self.get_qbase_rev_corr_validation(qbase_rev)
        return qbase_rev_corr
    
    @staticmethod
    def help():
        """
        Fournit une description des méthodes disponibles dans la classe Recession.
        """
        description = """
        Implémente le filtre de récession de Furey-Gupta.


        Arguments pour `furey_gupta`:
        - flow_series : Série temporelle des débits [mm/jour] (pd.Series ou np.ndarray).
        - k : Coefficient de récession (par défaut 0.03).
        - c : Ratio des coefficients (par défaut 1.1).
        """
        print(description)

    
        
