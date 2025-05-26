import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.models.SeparationModel import SeparationModel
from backend.contracts.Bundle import DataBaseFlow
from backend.ptq.PTQ import PTQ

class ExponentialRecessionCurve(BaseFlow):
    """
    Classe pour implémenter la méthode de récession exponentielle.
    
    def __init__(self,separationModel : SeparationModel):

        self.lambda_ = separationModel.lambda_
        self.lag_time = separationModel.lag_time
        self.k = separationModel.k
    """
    
    def compute(self, ptq : PTQ):
        precip = np.asarray(ptq.p)
        q_obs = np.asarray(ptq.daily_qobs_mean())
        q_rec = np.zeros_like(precip)

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
    
    def expo(self, a, b, k, pluie,debit):

        # Étape 1 : Mise à NaN là où la pluie est nulle
        debit_modifie = debit.where(pluie != 0)

        # Étape 2 : Transformation des valeurs non-NaN par a * Q^b
        debit_modifie = debit_modifie.apply(lambda q: a * q**b if pd.notna(q) else np.nan)

        # Étape 3 : Remplissage des NaN par décroissance exponentielle
        debit_modifie_filled = debit_modifie.copy()
        i = 0
        while i < len(debit_modifie_filled):
            if pd.isna(debit_modifie_filled[i]):
                # Trouver q0 (valeur précédente non NaN)
                if i == 0:
                    i += 1
                    continue  # On ignore les NaN en tout début de série
                q0 = debit_modifie_filled[i - 1]
                t = 1
                j = i
                # Remplacer tous les NaN consécutifs
                while j < len(debit_modifie_filled) and pd.isna(debit_modifie_filled[j]):
                    debit_modifie_filled[j] = q0 * np.exp(-k * t)
                    t += 1
                    j += 1
                i = j  # Continuer après la séquence
            else:
                i += 1
        return debit_modifie_filled

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
