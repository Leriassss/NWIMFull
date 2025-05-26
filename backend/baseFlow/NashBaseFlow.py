import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.contracts.Bundle import DataBaseFlow
from backend.ptq.PTQ import PTQ
from scipy.special import gamma
class NashBaseFlow(BaseFlow):
    """
    Classe pour implémenter la méthode de récession exponentielle.
    
    def __init__(self,separationModel : SeparationModel):

        self.lambda_ = separationModel.lambda_
        self.lag_time = separationModel.lag_time
        self.k = separationModel.k
    """
    
    def compute(self, nash_k, nash_n, time_base, production ):
        n = len(production)

        # Séquencement basé sur le temps
        seq_nash = np.arange(0, n, time_base)
        nash_time_base = []

        for k in seq_nash:
            # Extraction des précipitations nettes pour une séquence donnée
            production_seq = production[k : k + time_base]
            if production_seq.sum() > 0:
                t = np.arange(0, len(production_seq))
                # Fonction gamma de Nash
                q = pd.Series(
                    (1 / (nash_k * gamma(nash_n)))
                    * np.power(t / nash_k, nash_n - 1)
                    * np.exp(-t / nash_k)
                )
                # Convolution entre la séquence de production et la fonction gamma
                nash_k_result = pd.Series(np.convolve(production_seq, q))[: len(production_seq)]
            else:
                # Si aucune production dans la séquence, retourne des zéros
                nash_k_result = pd.Series(np.zeros_like(production_seq))
            nash_time_base.append(nash_k_result)

        # Assemblage des résultats et découpage à la taille initiale
        q_base =  pd.concat(nash_time_base).reset_index(drop=True)[:n]
        return q_base

        
    
 
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
