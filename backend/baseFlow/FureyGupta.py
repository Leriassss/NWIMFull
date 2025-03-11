from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.models.FureyGuptaModel import FureyGuptaModel
from backend.ptq.PTQ import PTQ
import numpy as np

class FureyGupta(BaseFlow):
    """
    Classe pour implémenter la méthode de récession Furey-Gupta.
    """
    def __init__(self,ptq : PTQ, fureyGuptaModel : FureyGuptaModel):
        self.flow_series = ptq.q
        self.gamma = fureyGuptaModel.gamma
        self.cs_over_c = fureyGuptaModel.cs_over_c

    def compute(self):
        """
        Implémente le filtre basé sur les paramètres physiques selon la méthode de Furey-Gupta.
        
        Args:
            flow_series : Série temporelle des débits [mm/jour]
            gamma  : Coefficient lié au retard des eaux souterraines
            cs_over_c (float) : Ratio des coefficients (par défaut 1.1)
            
        Returns:
            np.array : Série des débits de base (Qk).
        """
        Q_base = self.flow_series.copy()
        for k in range(3, len(self.flow_series)):
            Q_base[k] =np.maximum(0, 
                                  (1 - self.gamma) * Q_base[k - 1] + self.gamma * (self.cs_over_c) * (self.flow_series[k - 3] - Q_base[k - 3])
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
