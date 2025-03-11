class EToLossModel:
    """
    Modèle de données pour valider les paramètres de la méthode des pertes basées sur l'évapotranspiration potentielle (ETo).
    """

    def __init__(self, alpha: float):
        """
        Initialise et valide les données pour le modèle de pertes ETo.

        :param alpha: Coefficient d'évapotranspiration (doit être compris entre 0 et 1).
        """
        self.alpha = alpha
        self.validate()

    def validate(self):
        """
        Vérifie que les paramètres sont valides.
        """
        if self.alpha < 0 or self.alpha >= 1:
            raise ValueError("Le paramètre 'alpha' doit être compris entre 0 et 1.")

    def to_dict(self):
        """
        Retourne un dictionnaire des paramètres du modèle.
        """
        return {
            'alpha': self.alpha
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres du modèle.
        """
        return {
            "alpha": "evap. coeff"
        }

    @staticmethod
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique.

        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre à valider.
        :return: True si valide, sinon un message d'erreur est retourné.
        """
        try:
            value = float(value)  # Vérifie que la valeur est numérique
            if key == "alpha" and (value < 0 or value >= 1):
                raise ValueError("Le paramètre 'alpha' doit être compris entre 0 et 1.")
            return True
        except ValueError as e:
            return str(e)
