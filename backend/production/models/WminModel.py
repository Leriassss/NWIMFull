
class WMinModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode WMin.
    """

    def __init__(self, runoff_coef: float):
        """
        Initialise et valide les données pour la méthode WMin.

        :param prec: Série pandas contenant les précipitations (en mm).
        :param runoff_coef: Coefficient de ruissellement, doit être compris entre 0 et 1.
        """
        self.runoff_coef = runoff_coef
        self.validate()

    def validate(self):
        """
        Valide les paramètres du modèle.
        """
        """
                if not isinstance(self.prec, pd.Series):
            raise TypeError("La variable 'prec' doit être une série pandas.")
        if self.prec.isnull().any():
            raise ValueError("La série 'prec' ne doit pas contenir de valeurs manquantes.")
        """

        if self.runoff_coef <= 0 or self.runoff_coef > 1:
            raise ValueError("Le coefficient de ruissellement doit être compris entre 0 et 1.")

    def to_dict(self):
        return {
                'w': self.runoff_coef,
            }

    @staticmethod
    def get_parameter_names():
        return {
            "w" : "coef. ruissellement"
        }

