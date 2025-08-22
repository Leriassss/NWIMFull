from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from backend.contracts.Bundle import DataBaseFlow
from backend.baseFlow.models.EckhardtModel import EckhardtModel

import numpy as np

class Eckhardt(BaseFlowRoutine, BaseFlow):
    """
    Classe pour implémenter la méthode de récession Chapman.
    """
    def __init__(self, eckhardtModel: EckhardtModel):
        self.alpha = eckhardtModel.alpha
        self.bfi_max = eckhardtModel.bfi_max 

        self.a,self.b,self.correc_factor = 0, 0, 0

    def compute(self,flow_series, previous_qbase):
        Q_base = np.zeros_like(flow_series)
        Q_base[0] = previous_qbase
        for k in range(1, len(flow_series)):
            Q_base[k] = np.fmax(0,((1-self.bfi_max) * self.alpha* Q_base[k-1] + 
                    (1-self.alpha)*self.bfi_max*flow_series[k])/(1-(self.alpha*self.bfi_max)))

        return np.maximum(0,Q_base)


    def reverse_compute(self,previous_qbase, Q_direct):
        
        Q_base_rev = np.zeros(len(Q_direct))
        Q_base_rev[0]  = previous_qbase
        alpha_bfi = (1-self.alpha)/(1-self.bfi_max)
        for k in range(1, len(Q_direct)):
            Q_base_rev[k] = self.alpha*Q_base_rev[k-1] + alpha_bfi*self.bfi_max*Q_direct[k]
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
        return qbase_rev
    

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
