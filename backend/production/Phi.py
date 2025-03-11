import numpy as np
import pandas as pd
from backend.production.Production import Production
from backend.production.models.PhiModel import PhiModel


class Phi(Production):
    """
    Implémentation de la méthode Phi pour l'infiltration.
    """

    def __init__(self,initialLoss : pd.Series, data_model: PhiModel):
        """
        Initialise la méthode Phi avec un modèle de données validé.

        :param data_model: Instance de PhiDataModel contenant les données validées.
        """
        self._data_model = data_model
        self.initial_loss = initialLoss
        self.phi_index = 0
        

    def compute(self):
        """
        Calcule le ruissellement basé sur la méthode Phi.

        :return: Liste contenant des dictionnaires avec les valeurs de 'phi' et le ruissellement associé.
                 Si aucun phi satisfaisant n'est trouvé, retourne un résultat par défaut.
        """
        prec = self.initial_loss
        c_r = self._data_model.c_r

        # Calculs initiaux
        prec_sorted = prec.sort_values(ascending=False).round(3)
        lame_ruisselee = (c_r * prec.sum()).round(3)

        # Initialisation des résultats
        pluie_nette = []

        for i in prec_sorted.index:
            prec_iter_sum = prec_sorted[: (i + 1)].sum()
            phi_index = (prec_iter_sum - lame_ruisselee) / (i + 1)
            if phi_index > 0:
                ruissellement = np.maximum(0, prec - phi_index)
                ruissellement = pd.Series(ruissellement)
                
                # Condition modifiée : différence <= 5 mm
                if abs(ruissellement.sum().round(3) - lame_ruisselee) <= 5:
                    self.phi_index = phi_index
                    pluie_nette = prec - ruissellement

        # Si aucun phi satisfaisant n'est trouvé, retourner un résultat par défaut
        if len(pluie_nette) == 0:
            raise ValueError("Pas de valeurs de phi satisfaisantes")

        return pluie_nette

    @classmethod
    def help(cls):
        """
        Affiche une description de la méthode Phi et de ses paramètres.
        """
        description = """
        Méthode Phi pour modéliser le ruissellement et l'infiltration.

        Paramètres requis dans le modèle de données :
        - prec : Série pandas contenant les précipitations (en mm).
        - c_r : Coefficient de ruissellement (entre 0 et 1).

        La méthode calcule les indices 'phi' pour estimer le ruissellement associé à un événement
        pluvieux. Les résultats incluent une liste de valeurs de 'phi', les séries de ruissellement correspondantes,
        et les valeurs de pluie nette. Si aucun phi satisfaisant n'est trouvé, un résultat par défaut est retourné.
        """
        print(description)
