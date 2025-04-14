from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine

from backend.baseFlow.models.EckhardtModel import EckhardtModel
from backend.contracts.Bundle import DataBaseFlow

import numpy as np
import pandas as pd

from backend.ptq.PTQ import PTQ

class Eckhardt(BaseFlow):
    """
    Classe pour implémenter la méthode de récession Chapman.
    """
    def __init__(self, eckhardtModel: EckhardtModel):
        self.alpha = eckhardtModel.alpha
        self.bfi_max = eckhardtModel.bfi_max 

        self.a,self.b,self.correc_factor = 0, 0, 0

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
        for k in range(1, len(flow_series)):
            Q_base[k] = ((1-self.bfi_max) * self.alpha* Q_base[k-1] + 
                    (1-self.alpha)*self.bfi_max*flow_series[k])/(1-(self.alpha*self.bfi_max))

        return np.maximum(0,Q_base)

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
    
    def calibration_routine(self,data : DataBaseFlow):
        dates = data['ptq'].dates
        qobs = data['ptq'].q

        baseFlowRoutine = BaseFlowRoutine()
        prev_day = baseFlowRoutine.get_qobs_mean(dates[0])

        #FITTING DES COEFFICIENTS POUR LA RELATION QBASE-QOBS
        self.a,self.b  = baseFlowRoutine.regBaseFlow(data['qbase'] , qobs)
        #DETERMINATION DU DEBIT MOYEN JOURNALIER CORRESPONDANT
        q_obs_mean = data["qmean"][prev_day-1]
        #DETERMINATION DU DEBIT DE BASE PRECEDENT
        q_base_previous = baseFlowRoutine.modele_baseflow(q_obs_mean, self.a, self.b)

        #CALCUL DU DEBIT DE BASE PAR LA METHODE REVERSE
        qbase_rev = self.reverse_compute(q_base_previous, data['qsim'])
        # CALCUL DU FACTEUR DE CORRECTION
        self.correc_factor = baseFlowRoutine.correction_factor(qbase_rev, data['qbase'])

        qbase_rev_corr =  self.correc_factor * qbase_rev
        return qbase_rev_corr
        
    def validation_routine(self, data : DataBaseFlow):

        dates = data['ptq'].dates

        baseFlowRoutine = BaseFlowRoutine()
        prev_day = baseFlowRoutine.get_qobs_mean(dates[0])
        
        #DETERMINATION DU DEBIT MOYEN JOURNALIER CORRESPONDANT
        q_obs_mean = data["qmean"][prev_day-1]
        #DETERMINATION DU DEBIT DE BASE PRECEDENT
        q_base_previous = baseFlowRoutine.modele_baseflow(q_obs_mean, self.a, self.b)
        #CALCUL DU DEBIT DE BASE PAR LA METHODE REVERSE
        qbase_rev = self.reverse_compute(q_base_previous, data['qsim'])
        print(self.correc_factor)
        qbase_rev_corr =  self.correc_factor * qbase_rev
        return qbase_rev_corr

    def reverse_compute(self,previous_qbase, Q_direct):
        
        Q_base_rev = np.zeros(len(Q_direct))
        Q_base_rev[0]  = previous_qbase
        alpha_bfi = (1-self.alpha)/(1-self.bfi_max)
        for k in range(1, len(Q_direct)):
            Q_base_rev[k] = self.alpha*Q_base_rev[k-1] + alpha_bfi*self.bfi_max*Q_direct[k]
        
        return Q_base_rev

