class MuskingumModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode Muskingum.
    """

    def __init__(self, K, x):
        """
        Initialise et valide les données pour la méthode Muskingum.

        :param K: Temps de transfert de pointe observé (en jours).
        :param x: Pondération (comprise entre 0 et 0.5).
        :param dt: Intervalle de temps utilisé (en jours).
        """
        self.K = float(K)
        self.x = float(x)
        self.validate()

    def validate(self):
        """
        Valide les paramètres K, x et dt.

        Raises
        ------
        ValueError : Si K, x ou dt ne sont pas valides.
        """
        if not (0 <= self.x <= 0.5):
            raise ValueError("Le paramètre 'x' doit être compris entre 0 et 0.5.")
        if self.K <= 0:
            raise ValueError("Le paramètre 'K' doit être strictement positif.")

    def to_dict(self):
        """
        Convertit l'objet en un dictionnaire.

        :return: Dictionnaire des paramètres du modèle Muskingum.
        """
        return {
            'K': self.K,
            'x': self.x
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres pour la méthode Muskingum.

        :return: Dictionnaire des noms des paramètres.
        """
        return {
            "K": "K",
            "x": "x"
        }

    @staticmethod
    def get_default_values():
        return {
            "K": 5,
            "x": 0.27
    }

    @staticmethod
    def get_default_ranges():
        return {
            "K": [5,10],
            "x": [0.1,0.5]
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
            value = float(value)  # S'assure que la valeur est un nombre
            if key == "x" and not (0 <= value <= 0.5):
                raise ValueError("Le paramètre 'x' doit être compris entre 0 et 0.5.")
            elif key == "K" and value <= 0:
                raise ValueError("Le paramètre 'K' doit être strictement positif.")
            return True
        except Exception as e:
            return str(e)
