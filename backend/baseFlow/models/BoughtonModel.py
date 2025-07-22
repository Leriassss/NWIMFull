class BoughtonModel:
    """
    Classe pour valider les arguments nécessaires à la méthode de récession Furey-Gupta.
    """
    def __init__(self, k, c):
        """
        Initialise et valide les données pour la méthode Furey-Gupta.

        :param k: Paramètre k (doit être un nombre positif).
        :param c: Ratio c (doit être un nombre positif).
        """
        self.k = float(k)
        self.c = float(c)
        self.validate()

    def validate(self):
        """
        Valide les paramètres k et c.
        """
        if not isinstance(self.k, (int, float)) or self.k < 0:
            raise ValueError("Le paramètre 'k' doit être un nombre positif.")
        if not isinstance(self.c, (int, float)) or self.c <= 0:
            raise ValueError("Le ratio 'c' doit être un nombre positif.")

    def to_dict(self):
        """
        Retourne les paramètres du modèle sous forme de dictionnaire.
        """
        return {
            'k': self.k,
            'c': self.c
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres du modèle Furey-Gupta.
        """
        return {
            "k": "k",
            "c": "c"
        }

    @staticmethod
    def get_default_values():
        return {
            "k": 0.1,
            "c": 0.5
        }

    @staticmethod
    def get_default_ranges():
        return {
            "k": [0.1,1],
            "c": [0.5,1.1]
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
            if key == "k" and value <= 0:
                raise ValueError("Le paramètre 'k' doit être un nombre strictement positif.")
            elif key == "c" and value <= 0:
                raise ValueError("Le paramètre 'c' doit être un nombre strictement positif.")
            return True
        except Exception as e:
            return str(e)
