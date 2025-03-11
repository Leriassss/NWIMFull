class FureyGuptaModel:
    """
    Classe pour valider les arguments nécessaires à la méthode de récession Furey-Gupta.
    """
    def __init__(self, gamma, cs_over_c):
        """
        Initialise et valide les données pour la méthode Furey-Gupta.

        :param gamma: Paramètre gamma (doit être un nombre positif).
        :param cs_over_c: Ratio cs_over_c (doit être un nombre positif).
        """
        self.gamma = gamma
        self.cs_over_c = cs_over_c
        self.validate()

    def validate(self):
        """
        Valide les paramètres gamma et cs_over_c.
        """
        if not isinstance(self.gamma, (int, float)) or self.gamma <= 0:
            raise ValueError("Le paramètre 'gamma' doit être un nombre positif.")
        if not isinstance(self.cs_over_c, (int, float)) or self.cs_over_c <= 0:
            raise ValueError("Le ratio 'cs_over_c' doit être un nombre positif.")

    def to_dict(self):
        """
        Retourne les paramètres du modèle sous forme de dictionnaire.
        """
        return {
            'gamma': self.gamma,
            'cs_over_c': self.cs_over_c
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres du modèle Furey-Gupta.
        """
        return {
            "gamma": "gamma",
            "cs_over_c": "cs_over_c"
        }

    @staticmethod
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique pour Furey-Gupta.

        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre à valider.
        :return: True si valide, sinon un message d'erreur est retourné.
        """
        try:
            value = float(value)  # S'assure que la valeur est un nombre
            if key == "gamma" and value <= 0:
                raise ValueError("Le paramètre 'gamma' doit être un nombre positif.")
            elif key == "cs_over_c" and value <= 0:
                raise ValueError("Le paramètre 'cs_over_c' doit être un nombre positif.")
            return True
        except ValueError as e:
            return str(e)
