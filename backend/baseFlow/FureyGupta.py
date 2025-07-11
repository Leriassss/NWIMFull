from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from backend.contracts.Bundle import DataBaseFlow
from backend.baseFlow.models.FureyGuptaModel import FureyGuptaModel
import numpy as np

class FureyGupta(BaseFlowRoutine, BaseFlow):
    """
    Classe pour implémenter la méthode de récession Furey-Gupta.
    """
    def __init__(self, fureyGuptaModel : FureyGuptaModel):
        self.gamma = fureyGuptaModel.gamma
        self.cs_over_c = fureyGuptaModel.cs_over_c

    def compute(self, flow_series):
        """
        Implémente le filtre basé sur les paramètres physiques selon la méthode de Furey-Gupta.
        
        Args:
            flow_series : Série temporelle des débits [mm/jour]
            gamma  : Coefficient lié au retard des eaux souterraines
            cs_over_c (float) : Ratio des coefficients (par défaut 1.1)
            
        Returns:
            np.array : Série des débits de base (Qk).
        """
        
        Q_base = flow_series.copy()
        for k in range(1, len(flow_series)):
            Q_base[k] =np.maximum(0, 
                                  (1 - self.gamma) * Q_base[k - 1] + self.gamma * (self.cs_over_c) * (flow_series[k - 1] - Q_base[k - 1])
                                  ) 
        return Q_base
    

    def reverse_compute(self,previous_qbase, Q_direct):
        
        Q_base_rev = np.zeros(len(Q_direct))
        Q_base_rev[0]  = previous_qbase
        
        for k in range(1, len(Q_direct)):
            Q_base_rev[k] = (1-self.gamma)*Q_base_rev[k-1] + self.gamma*self.cs_over_c*Q_direct[k-1]
        return Q_base_rev
    
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

    
        
