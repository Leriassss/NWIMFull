
import pandas as pd
from backend.production.Production import Production
from backend.production.models.WModel import WModel

class W(Production):
    """
    Implémentation du modèle WMin pour le calcul du ruissellement.
    """

    def __init__(self, initialLoss : pd.Series, data_model: WModel):
        """
        Initialise le modèle WMin avec un modèle de données validé.

        :param data_model: Instance de WMinDataModel contenant les données validées.
        """

        self._data_model = data_model
        self.initial_loss = initialLoss

    def compute(self):
        return self.initial_loss * float(self._data_model.runoff_coef)

    @classmethod
    def help(cls):
        """
        Affiche une description de la méthode WMin et de ses paramètres.
        """
        description = """
        Méthode WMin pour le calcul du ruissellement.

        Paramètres requis dans le modèle de données :
        - prec : Série pandas contenant les précipitations (en mm).
        - runoff_coef : Coefficient de ruissellement, doit être compris entre 0 et 1.

        La méthode calcule le ruissellement en multipliant les précipitations
        par le coefficient de ruissellement spécifié.
        """
        print(description)
