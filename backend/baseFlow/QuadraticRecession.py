
import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.models.SeparationModel import SeparationModel
from backend.ptq.PTQ import PTQ

class QuadraticRecessionCurve(BaseFlow):
    """
    Classe pour implémenter la méthode de récession quadratique.
    """
    def __init__(self,ptq : PTQ, separationModel : SeparationModel):
        self.dates = ptq.dates
        self.Q_sim = ptq.q
        self.lambda_ = separationModel.lambda_

    def compute(self):
        """
        Applique la fonction de récession quadratique q = q0 / (1 + lambda * t)^2 par année.
        
        Returns:
            pd.DataFrame: DataFrame avec les dates et les débits ajustés.
        """
        df = pd.DataFrame({"dates": self.dates, "Q_sim": self.Q_sim})
        df["dates"] = pd.to_datetime(df["dates"])  # S'assurer que les dates sont au bon format
        
        resultats = []
        
        for annee, groupe in df.groupby(df["dates"].dt.year):
            serie_debits = pd.Series(groupe['Q_sim'].values)
            indice_max = serie_debits.idxmax()  # Trouver l'indice du maximum
            q0 = serie_debits[indice_max]  # Débit initial
            
            result = np.zeros(len(groupe))
            for t in range(indice_max, len(groupe)):
                result[t] = q0 / (1 + self.lambda_ * (t - indice_max))**2
        
            resultats.append(pd.Series(result))
        
        return pd.concat(resultats).reset_index(drop=True)

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
