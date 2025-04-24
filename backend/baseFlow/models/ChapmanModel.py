
class ChapmanModel:
    """
    Classe pour valider les arguments nécessaires à la méthode de récession Chapman.
    """

    def __init__(self, alpha=0.925):
        """
        Initialise et valide les données pour la méthode Chapman.

        :param alpha: Coefficient alpha pour la récession Chapman (entre 0 et 1).
        """
        self.alpha = float(alpha)
        self.validate()

    def validate(self):
        """
        Valide le paramètre alpha.
        """
        if not isinstance(self.alpha, (int, float)) or not (0 < self.alpha <= 1):
            raise ValueError("Le coefficient alpha doit être un nombre entre 0 et 1.")

    def to_dict(self):
        """
        Retourne les paramètres du modèle sous forme de dictionnaire.
        """
        return {
            'alpha': self.alpha
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres du modèle Chapman.
        """
        return {
            "alpha": "alpha"
        }

    @staticmethod
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique pour Chapman.

        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre à valider.
        :return: True si valide, sinon un message d'erreur est retourné.
        """
        try:
            value = float(value)  # S'assure que la valeur est un nombre
            if key == "alpha" and not (0 < value <= 1):
                raise ValueError("Le paramètre 'alpha' doit être un nombre entre 0 et 1.")
            return True
        except Exception as e:
            return str(e)
