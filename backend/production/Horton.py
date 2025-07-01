
import numpy as np
import pandas as pd
from backend.production.Production import Production
from backend.production.models.HortonModel import HortonModel


class Horton(Production):
    """
    Implémentation de la méthode Horton pour l'infiltration.
    """

    def __init__(self, initialLoss : pd.Series, data_model: HortonModel):
        """
        Initialise la méthode Horton avec un modèle de données validé.

        :param data_model: Instance de HortonDataModel contenant les données validées.
        """
        self._data_model = data_model
        self.initial_loss = initialLoss

    def compute_hour(self):
        """
        Calcule le ruissellement basé sur la méthode Horton.

        :return: Série pandas des ruissellements calculés.
        """
        prec =self.initial_loss
        f_0 = self._data_model.f_0
        f_t = self._data_model.f_t
        k = self._data_model.k

        # Utilisation de l'index temporel pour les calculs
        t = np.arange(len(prec))
        taux_infiltration = pd.Series(f_t + (f_0 - f_t) * np.exp(-k * t), index=prec.index)

        # Calcul du ruissellement
        ruissellement = np.maximum(0, prec - taux_infiltration)

        return pd.Series(ruissellement)

    def compute(self):
        """
        Calcule le ruissellement basé sur la méthode Horton.

        :return: Série pandas des ruissellements calculés.
        """
        prec =self.initial_loss
        f_0 = self._data_model.f_0
        f_t = self._data_model.f_t
        k = self._data_model.k

        # Utilisation de l'index temporel pour les calculs
        t = 1
        taux_infiltration = pd.Series(f_t + (f_0 - f_t) * np.exp(-k * t), index=prec.index)

        # Calcul du ruissellement
        ruissellement = np.maximum(0, prec - taux_infiltration)

        return pd.Series(ruissellement).reset_index(drop=True)
    
    @classmethod
    def help(cls):
        """
        Affiche une description de la méthode Horton et de ses paramètres.
        """
        description = """
        Méthode Horton pour modéliser l'infiltration.

        Paramètres requis dans le modèle de données :
        - prec : Série pandas contenant les précipitations (en mm).
        - f_0 : Taux d'infiltration initial (en mm/h).
        - f_t : Taux d'infiltration final (en mm/h).
        - k : Constante de décroissance exponentielle (en 1/h).

        La méthode calcule le ruissellement en fonction de la différence entre les précipitations et le taux
        d'infiltration à chaque pas de temps.
        """
        print(description)
