class WMinModel:
    """
    Modèle de données pour valider les paramètres de la méthode des pertes initiales (Ia).
    """

    def __init__(self, S: float, alpha: float, loss_days: int):
        """
        Initialise et valide les données pour le modèle de pertes initiales Ia.

        :param S: Capacité de stockage du sol (doit être ≥ 0).
        :param alpha: Coefficient de pertes initiales (doit être compris entre 0 et 1).
        :param loss_days: Nombre de jours de pertes (doit être ≥ 0).
        """
        self.S = S
        self.alpha = alpha
        self.loss_days = loss_days
        self.validate()

    def validate(self):
        """
        Vérifie que les paramètres sont valides.
        """
        try:
            value = float(value)  # Vérifie que la valeur est numérique
            if key == "S" and value < 0:
                raise ValueError("Le paramètre 'S' doit être positif.")
            elif key == "alpha" and (value < 0 or value > 1):
                raise ValueError("Le paramètre 'alpha' doit être compris entre 0 et 1.")
            elif key == "loss_days":
                value = int(value)  # Convertit en entier
                if value < 0:
                    raise ValueError("Le paramètre 'loss_days' doit être positif.")
            return True
        except Exception as e:
            return str(e)

    def to_dict(self):
        """
        Retourne un dictionnaire des paramètres du modèle.
        """
        return {
            'S': self.S,
            'alpha': self.alpha,
            'loss_days': self.loss_days
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres du modèle.
        """
        return {
            "S": "S",
            "alpha": "alpha",
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
            elif key == "alpha" and (value < 0 or value > 1):
                raise ValueError("Le paramètre 'alpha' doit être compris entre 0 et 1.")
            elif key == "loss_days":
                value = int(value)  # Convertit en entier
                if value < 0:
                    raise ValueError("Le paramètre 'loss_days' doit être positif.")
            return True
        except Exception as e:
            return str(e)
