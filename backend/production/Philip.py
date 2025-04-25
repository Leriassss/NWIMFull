
import numpy as np
import pandas as pd
from backend.production.Production import Production
from backend.production.models.PhilipModel import PhilipModel

class Philip(Production):
    """
    Implémentation de la méthode Philip pour l'infiltration.
    """

    def __init__(self, initialLoss : pd.Series, data_model: PhilipModel):
        """
        Initialise la méthode Philip avec un modèle de données validé.

        :param data_model: Instance de PhilipDataModel contenant les données validées.
        """
        self._data_model = data_model
        self.initial_loss = initialLoss

    def compute(self):
        """
        Calcule l'infiltration et le ruissellement basé sur la méthode Philip.

        :return: Série pandas du ruissellement.
        """
        prec = self.initial_loss
        S = float(self._data_model.S)
        K = float(self._data_model.K)

        # Calcul de l'infiltration selon le modèle de Philip
        infiltration_philip =  S + K

        # Calcul du ruissellement
        ruissellement = np.maximum(0, prec - infiltration_philip)
        return ruissellement

    def compute_hour(self):
        """
        Calcule l'infiltration et le ruissellement basé sur la méthode Philip.

        :return: Série pandas du ruissellement.
        """
        prec = self.initial_loss
        S = self._data_model.S
        K = self._data_model.K

        # Calcul de l'infiltration selon le modèle de Philip
        infiltration_philip = np.power(prec.index + 1, -1 / 2) * S + K

        # Calcul du ruissellement
        ruissellement = np.maximum(0, prec - infiltration_philip)
        return ruissellement
    @classmethod
    def help(cls):
        """
        Affiche une description de la méthode Philip et de ses paramètres.
        """
        description = """
        Méthode Philip pour modéliser l'infiltration et le ruissellement.

        Paramètres requis dans le modèle de données :
        - prec : Série pandas contenant les précipitations (en mm).
        - S : Paramètre d'absorption (positif).
        - K : Conductivité hydraulique (positif).

        La méthode calcule l'infiltration en fonction du temps à l'aide de la formule de Philip :
            infiltration(t) = S / sqrt(t) + K

        Le ruissellement est ensuite obtenu par la différence entre les précipitations et l'infiltration.
        """
        print(description)
