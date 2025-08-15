
import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.models.SeparationModel import SeparationModel
from backend.contracts.Bundle import DataBaseFlow

class QuadraticRecessionCurve(BaseFlow):
    """
    Classe pour implémenter la méthode de récession quadratique.
    """
    def __init__(self,separationModel : SeparationModel):
        self.k = separationModel.k
        self.window = separationModel.window

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
    def compute(self, data : DataBaseFlow):
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
        a = data['factors'][0]
        b = data['factors'][1]
        # Étape 1 : considérer les périodes sans pluie
        debit_modifie = data['qsim'].where(data["p"] != 0)
        
        # Étape 2 : appliquer la loi a * Q^b quand c’est défini
        debit_modifie = debit_modifie.apply(lambda q: a * q**b if pd.notna(q) else np.nan)
        
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
                    debit_base.iloc[j] = q0 /((1+self.k*t)**2)

                    t += 1
                    j += 1
                i = j
            else:
                i += 1
        debit_base = debit_base.rolling(window=self.window, center=True, min_periods=1).mean()
        return debit_base

    
    def calibration_routine(self,data : DataBaseFlow):
        return self.compute(data)
    
    def validation_routine(self,data : DataBaseFlow):
        return self.compute(data)
        

