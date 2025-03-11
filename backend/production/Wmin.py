
import pandas as pd
from backend.production.Production import Production
from backend.production.models.WminModel import WMinModel

class WMin(Production):
    """
    Implémentation du modèle WMin pour le calcul du ruissellement.
    """

    def __init__(self, initialLoss : pd.Series, data_model: WMinModel):
        """
        Initialise le modèle WMin avec un modèle de données validé.

        :param data_model: Instance de WMinDataModel contenant les données validées.
        """

        self._data_model = data_model
        self.initial_loss = initialLoss

    def compute(self):
        """
        Calcule le ruissellement en utilisant le coefficient de ruissellement.

        :return: Série pandas contenant le ruissellement calculé.
        """
        prec =self.initial_loss
        runoff_coef = self._data_model.runoff_coef
        
        return prec * runoff_coef

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
