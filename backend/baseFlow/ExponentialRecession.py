import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.models.SeparationModel import SeparationModel
from backend.ptq.PTQ import PTQ

class ExponentialRecessionCurve(BaseFlow):
    """
    Classe pour implémenter la méthode de récession exponentielle.
    """
    def __init__(self,ptq : PTQ, separationModel : SeparationModel):
        self.dates = ptq.dates
        self.Q_sim = ptq.q
        self.lambda_ = separationModel.lambda_

    def compute(self):
        """
        Applique la fonction de récession exponentielle q = q0 * exp(-lambda * t) par année.
        
        Returns:
            pd.DataFrame: DataFrame avec la courbe de récession appliquée par année.
        """
        df = pd.DataFrame({"dates": self.dates, "Q_sim": self.Q_sim})
        df["dates"] = pd.to_datetime(df["dates"])    
        resultats = []
        
        # Traiter chaque année séparément
        for annee, groupe in df.groupby(df["dates"].dt.year):
            serie_debits = pd.Series(groupe['Q_sim'].values)
            indice_max = serie_debits.idxmax()
            q0 = serie_debits[indice_max]
            
            result = np.zeros(len(groupe))
            for t in range(indice_max , len(groupe)):
                result[t] = q0 * np.exp(-self.lambda_ * (t - indice_max))
                
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
