import numpy as np
import pandas as pd
from backend.production.Production import Production
from backend.production.models.HoltanModel import HoltanModel


class Holtan(Production):
    """
    Implémentation de la méthode Holtan pour l'infiltration.
    """

    def __init__(self,initialLoss : pd.Series,  data_model: HoltanModel):
        """
        Initialise la méthode Holtan avec un modèle de données validé.

        :param data_model: Instance de HoltanDataModel contenant les données validées.
        """
        self._data_model = data_model
        self.initial_loss = initialLoss

    def compute(self):
        """
        Calcule l'infiltration basée sur la méthode Holtan.

        :return: Série pandas des infiltrations calculées.
        """
        prec = self.initial_loss
        f_0 = self._data_model.f_0
        f_t = self._data_model.f_t
        k = self._data_model.k
        storage_capacity = self._data_model.storage_capacity

        lame_cumulee_ruisselee = np.zeros(len(prec))
        infiltration = np.zeros(len(prec))

        for i in range(1, len(prec)):
            # Calcul du rapport entre la lame cumulée et la capacité de stockage
            rapport = lame_cumulee_ruisselee[i - 1] / storage_capacity

            # Calcul de l'infiltration pour chaque pas de temps
            infiltration[i - 1] = 0 if rapport < 1 else f_t + f_0 * np.power((1 - rapport), k)

            # Mise à jour de la lame cumulée
            lame_cumulee_ruisselee[i] = infiltration[i - 1] + lame_cumulee_ruisselee[i - 1]

        # Calcul final de l'infiltration
        infiltration_finale = np.maximum(0, prec - infiltration)

        return pd.Series(infiltration_finale).reset_index(drop=True)

    @classmethod
    def help(cls):
        """
        Affiche une description de la méthode Holtan et de ses paramètres.
        """
        description = """
        Méthode Holtan pour modéliser l'infiltration.

        Paramètres requis dans le modèle de données :
        - prec : Série pandas contenant les précipitations (en mm).
        - f_0 : Taux d'infiltration initial (en mm/h).
        - f_t : Taux d'infiltration final (en mm/h).
        - k : Exposant empirique du modèle.
        - storage_capacity : Capacité de stockage du sol (en mm).

        La méthode calcule l'infiltration en tenant compte de la capacité de stockage du sol et de l'évolution temporelle
        du taux d'infiltration.
        """
        print(description)
