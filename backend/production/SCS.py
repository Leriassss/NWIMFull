
import numpy as np
import pandas as pd
from backend.production.Production import Production
from backend.production.models.SCSModel import SCSModel


class SCS(Production):
    """
    Implémentation de la méthode SCS pour le calcul du ruissellement.
    """

    def __init__(self, initialLoss : pd.Series, data_model: SCSModel):
        """
        Initialise la méthode SCS avec un modèle de données validé.

        :param data_model: Instance de SCSDataModel contenant les données validées.
        """
        self._data_model = data_model
        self.initial_loss = initialLoss

    def compute(self):
        """
        Calcule le ruissellement net basé sur la méthode SCS.

        :return: Série pandas contenant le ruissellement net.
        """
        prec =self.initial_loss
        curve_number = self._data_model.curve_number

        # Calcul des paramètres SCS
        s = (25400 / curve_number) - 254  
        i_a = self._data_model.i_a * s  
        n = prec.count()
        rainfall_cumul = np.zeros(n)
        runoff_cumul = np.zeros(n)
        net_runoff = np.zeros(n)

        # Calcul du ruissellement cumulé et net
        for t in range(1, n):
            rainfall_cumul[t] = rainfall_cumul[t - 1] + prec.iloc[t]
            p = rainfall_cumul[t]
            if p > i_a:
                runoff_cumul[t] = ((p - i_a) ** 2) / (p - i_a + s)
            else:
                runoff_cumul[t] = 0
            net_runoff[t] = runoff_cumul[t] - runoff_cumul[t - 1]

        return pd.Series(net_runoff).reset_index(drop=True)
    

    def compute_hour(self):
        """
        Calcule le ruissellement net basé sur la méthode SCS.

        :return: Série pandas contenant le ruissellement net.
        """
        prec =self.initial_loss
        curve_number = self._data_model.curve_number

        # Calcul des paramètres SCS
        s = (25400 / curve_number) - 254  # Stockage potentiel maximal
        i_a = 0.2 * s  # Précipitation initiale
        n = prec.count()
        rainfall_cumul = np.zeros(n)
        runoff_cumul = np.zeros(n)
        net_runoff = np.zeros(n)

        # Calcul du ruissellement cumulé et net
        for t in range(1, n):
            rainfall_cumul[t] = rainfall_cumul[t - 1] + prec.iloc[t]
            p = rainfall_cumul[t]
            if p > i_a:
                runoff_cumul[t] = ((p - i_a) ** 2) / (p - i_a + s)
            else:
                runoff_cumul[t] = 0
            net_runoff[t] = runoff_cumul[t] - runoff_cumul[t - 1]

        return pd.Series(net_runoff, index=prec.index)

    @classmethod
    def help(cls):
        """
        Affiche une description de la méthode SCS et de ses paramètres.
        """
        description = """
        Méthode SCS (Soil Conservation Service) pour le calcul du ruissellement.

        Paramètres requis dans le modèle de données :
        - prec : Série pandas contenant les précipitations (en mm).
        - curve_number : Curve Number, doit être compris entre 0 et 100.

        La méthode calcule le ruissellement à partir des précipitations totales et
        des caractéristiques de l'utilisation des sols en utilisant la formule :
            S = (25400 / CN) - 254
            Ia = 0.2 * S
            Ruissellement cumulé = ((P - Ia)^2) / (P - Ia + S) si P > Ia, sinon 0.

        Le ruissellement net est ensuite calculé à chaque pas de temps.
        """
        print(description)
