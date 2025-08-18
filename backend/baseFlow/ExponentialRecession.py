import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.models.SeparationModel import SeparationModel
from backend.contracts.Bundle import DataBaseFlow
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
class ExponentialRecessionCurve(BaseFlow):
    """
    Classe pour implémenter la méthode de récession exponentielle.
    """
    def __init__(self,separationModel : SeparationModel):
        self.k = separationModel.k
        self.window = separationModel.window
        self.ratio = separationModel.ratio
        self.a, self.b = 0, 0
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
    """
    def compute(self, flow_series):
        return self.ratio*flow_series
 
    def compute2(self, data : DataBaseFlow):
        """
        Estimation du débit de base par décroissance exponentielle.
        
        Paramètres :
        - a, b : coefficients pour la transformation a * Q^b
        - k : taux de décroissance
        - pluie : série de précipitations
        - debit : série de débits observés
        - Q0 : valeur initiale du débit de base
        
        Retourne :
        - Serie de débit de base estimé
        """

        # Étape 1 : considérer les périodes sans pluie
        debit_modifie = data['qsim'].where(data["p"] != 0)
        
        debit_sim = debit_modifie.dropna()
        qb = (self.ratio * data['qObs']).where(data["p"] != 0).dropna()
        self.a, self.b = BaseFlowRoutine.regBaseFlow(qb,debit_sim)
        
        # Étape 2 : appliquer la loi a * Q^b quand c’est défini
        debit_modifie = debit_modifie.apply(lambda q: self.a * q**self.b if pd.notna(q) else np.nan)
        
        # Étape 3 : appliquer la décroissance exponentielle aux périodes manquantes
        debit_base = debit_modifie.copy()
        debit_base.iloc[0] = data['prevObs']  # initialisation
        
        i = 1
        while i < len(debit_base):
            if pd.isna(debit_base.iloc[i]):
                q0 = debit_base.iloc[i - 1] if i == 1 else debit_base.iloc[i - 1] + data['qsim'].iloc[i-1]
                t = 1
                j = i
                while j < len(debit_base) and pd.isna(debit_base.iloc[j]):
                    debit_base.iloc[j] = q0 * np.exp(-self.k * t)

                    t += 1
                    j += 1
                i = j
            else:
                i += 1
        debit_base = debit_base.rolling(window=self.window, center=True, min_periods=1).mean()
        return debit_base

    
    def calibration_routine(self,data : DataBaseFlow):
        return self.compute2(data)
    
    def validation_routine(self,data : DataBaseFlow):
        # Étape 1 : considérer les périodes sans pluie
        debit_modifie = data['qsim'].where(data["p"] != 0)

        # Étape 2 : appliquer la loi a * Q^b quand c’est défini
        debit_modifie = debit_modifie.apply(lambda q: self.a * q**self.b if pd.notna(q) else np.nan)
        
        # Étape 3 : appliquer la décroissance exponentielle aux périodes manquantes
        debit_base = debit_modifie.copy()
        debit_base.iloc[0] = data['prevObs']  # initialisation
        
        i = 1
        while i < len(debit_base):
            if pd.isna(debit_base.iloc[i]):
                q0 = debit_base.iloc[i - 1] if i == 1 else debit_base.iloc[i - 1] + data['qsim'].iloc[i-1]
                t = 1
                j = i
                while j < len(debit_base) and pd.isna(debit_base.iloc[j]):
                    debit_base.iloc[j] = q0 * np.exp(-self.k * t)

                    t += 1
                    j += 1
                i = j
            else:
                i += 1
        debit_base = debit_base.rolling(window=self.window, center=True, min_periods=1).mean()
        return debit_base
        
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
