class AmountLossModel:
    """
    Modèle de données pour valider les paramètres de la méthode des pertes en quantité.
    """

    def __init__(self, S, loss_days):
        """
        Initialise et valide les données pour le modèle des pertes en quantité.

        :param S: Capacité de stockage du sol (en mm).
        :param loss_days: Nombre de jours associés aux pertes (doit être positif).
        """
        self.S = S
        self.loss_days = loss_days
        self.validate()

    def validate(self):
        """
        Vérifie que les paramètres sont valides.
        """
        if self.S < 0:
            raise ValueError("Le paramètre 'S' doit être positif.")
        if self.loss_days < 0:
            raise ValueError("Le paramètre 'loss_days' doit être positif.")

    def to_dict(self):
        """
        Retourne un dictionnaire des paramètres du modèle.
        """
        return {
            'S': self.S,
            'loss_days': self.loss_days
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres du modèle.
        """
        return {
            "S": "S",
            "loss_days": "loss days"
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
            if key == "S" and value < 0:
                raise ValueError("Le paramètre 'S' doit être positif.")
            elif key == "loss_days" and value < 0:
                raise ValueError("Le paramètre 'loss_days' doit être positif.")
            return True
        except ValueError as e:
            return str(e)
