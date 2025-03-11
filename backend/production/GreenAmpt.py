

import numpy as np
import pandas as pd
from backend.production.Production import Production
from backend.production.models.GreenAmptModel import GreenAmptModel

class GreenAmpt(Production):
    """
    Implémentation de la méthode Green-Ampt pour l'infiltration.
    """
    def __init__(self, initialLoss : pd.Series,data_model: GreenAmptModel):
        self._data_model = data_model
        self.initial_loss = initialLoss

    def compute(self):
        """
        Calcule l'infiltration basée sur la méthode Green-Ampt.

        :param data_model: Une instance de GreenAmptDataModel contenant les données validées.
        :return: Série pandas des infiltrations calculées.
        """
        prec = self.initial_loss
        succion = self._data_model.succion
        d_theta = self._data_model.d_theta
        ks = self._data_model.ks
        h0 = self._data_model.H0

        lame_cumulee_ruisselee = np.zeros(len(prec))
        infiltration = np.zeros(len(prec))

        for i in range(1, len(prec)):
            # Calcul de l'infiltration pour chaque pas de temps
            infiltration[i - 1] = ks * (1 + (succion * d_theta / max(lame_cumulee_ruisselee[i - 1], 0)))
            lame_cumulee_ruisselee[i] = infiltration[i - 1] + lame_cumulee_ruisselee[i - 1]

        # Calcul final de l'infiltration selon Green-Ampt
        infiltration_ga = np.maximum(0, h0 - infiltration)
        infiltration_finale = np.maximum(0, prec - infiltration_ga)

        return pd.Series(infiltration_finale, index=prec.index)

    def compute_hour(self):
        """
        Calcule l'infiltration basée sur la méthode Green-Ampt.

        :param data_model: Une instance de GreenAmptDataModel contenant les données validées.
        :return: Série pandas des infiltrations calculées.
        """
        prec = self._data_model.prec
        succion = self._data_model.succion
        d_theta = self._data_model.d_theta
        ks = self._data_model.ks
        h0 = self._data_model.H0

        lame_cumulee_ruisselee = np.zeros(len(prec))
        infiltration = np.zeros(len(prec))

        for i in range(1, len(prec)):
            # Calcul de l'infiltration pour chaque pas de temps
            infiltration[i - 1] = ks * (1 + succion * d_theta / max(lame_cumulee_ruisselee[i - 1], 1e-6))
            lame_cumulee_ruisselee[i] = infiltration[i - 1] + lame_cumulee_ruisselee[i - 1]

        # Calcul final de l'infiltration selon Green-Ampt
        infiltration_ga = np.maximum(0, h0 - infiltration)
        infiltration_finale = np.maximum(0, prec - infiltration_ga)

        return pd.Series(infiltration_finale, index=prec.index)
    @classmethod
    def help(cls):
        """
        Affiche une description de la méthode Green-Ampt et de ses paramètres.
        """
        description = """
        Méthode Green-Ampt pour modéliser l'infiltration.

        Paramètres requis dans le modèle de données :
        - prec : Série pandas contenant les précipitations (en mm).
        - succion : Succion du sol (en mm).
        - d_theta : Variation de teneur en eau (en fraction).
        - ks : Conductivité hydraulique saturée du sol (en mm/h).
        - H0 : Hauteur initiale d'eau sur le sol (en mm).
        """
        print(description)
