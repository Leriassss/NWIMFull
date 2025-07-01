class WMinModel:
    """
    Modèle de données pour valider les paramètres de la méthode des pertes initiales (Ia).
    """

    def __init__(self, S: float, alpha: float):
        """
        Initialise et valide les données pour le modèle de pertes initiales Ia.

        :param S: Capacité de stockage du sol (doit être ≥ 0).
        :param alpha: Coefficient de pertes initiales (doit être compris entre 0 et 1).
        :param loss_days: Nombre de jours de pertes (doit être ≥ 0).
        """
        self.S = float(S)
        self.alpha = float(alpha)
        self.validate()

    def validate(self):
        """
        Vérifie que les paramètres sont valides.
        """
        if self.S < 0:
                raise ValueError("Le paramètre 'S' doit être positif.")
        if (self.alpha < 0 or self.alpha > 1):
                raise ValueError("Le paramètre 'alpha' doit être compris entre 0 et 1.")

    def to_dict(self):
        """
        Retourne un dictionnaire des paramètres du modèle.
        """
        return {
            'S': self.S,
            'alpha': self.alpha
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres du modèle.
        """
        return {
            "S": "S",
            "alpha": "alpha"
        }

    @staticmethod
    def get_default_ranges():
        return {
                'S': [0,20],
                'alpha': [0,1]
            }
    
    @staticmethod
    def get_default_values():
        return {
                'S': 0,
                'alpha': 0.25
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
            return True
        except Exception as e:
            return str(e)
