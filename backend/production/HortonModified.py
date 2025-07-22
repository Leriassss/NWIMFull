
import numpy as np
import pandas as pd
from backend.production.Production import Production
from backend.production.models.HortonModifiedModel import HortonModifiedModel


class HortonModified(Production):
    """
    Implémentation de la méthode Horton pour l'infiltration.
    """

    def __init__(self, initialLoss : pd.Series, data_model: HortonModifiedModel):
        """
        Initialise la méthode Horton avec un modèle de données validé.

        :param data_model: Instance de HortonDataModel contenant les données validées.
        """
        self._data_model = data_model
        self.initial_loss = initialLoss

    def compute(self):
        """
        Calcule le ruissellement basé sur la méthode Horton.

        :return: Série pandas des ruissellements calculés.
        """
        prec =self.initial_loss
        init_storage = self._data_model.init_storage
        smax = self._data_model.smax
        k = self._data_model.k

        a = init_storage*smax
        inf_capacity = np.zeros_like(prec)
        inf_capacity[0] = smax-a
        for i in range(1,len(inf_capacity)):
            a = min(smax, a + prec[i-1])
            a = a*(1-k)
            inf_capacity[i] = smax - a
        return pd.Series(prec-inf_capacity)
        



    
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
