
class RidgeRegressionModel:
    """
    Classe pour valider les arguments nécessaires à la méthode de Regression Ridge.
    """

    def __init__(self, alpha):
        """
        Initialise et valide les données pour la méthode Chapman.

        """
        self.alpha = float(alpha)
        self.validate()

    def validate(self):
        """
        Valide le paramètre alpha.
        """
        if not isinstance(self.alpha, (int, float)) :
            raise ValueError("Valeur invalide.")

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
    def get_default_values():
        return {
                'alpha': 10
        }

    @staticmethod
    def get_default_ranges():
        return {
                'alpha': [0,100]
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
            if key == "alpha" and not isinstance(value, (int, float)):
                raise ValueError("Paramètre invalide")
            return True
        except Exception as e:
            return str(e)
