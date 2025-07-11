class NathanMcMahonModel:
    """
    Classe pour valider les arguments nécessaires à la méthode de récession Furey-Gupta.
    """
    def __init__(self, k):
        """
        Initialise et valide les données pour la méthode Furey-Gupta.

        :param gamma: Paramètre gamma (doit être un nombre positif).
        :param cs_over_c: Ratio cs_over_c (doit être un nombre positif).
        """
        self.k = float(k)
        self.validate()

    def validate(self):
        """
        Valide les paramètres gamma et cs_over_c.
        """
        if not isinstance(self.k, (int, float)) or not (0 <= self.k < 1):
            raise ValueError("Le paramètre 'k' doit être compris entre 0 et 1.")
        
    def to_dict(self):
        """
        Retourne les paramètres du modèle sous forme de dictionnaire.
        """
        return {
            'k': self.k

        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres du modèle Furey-Gupta.
        """
        return {
            "k": "k"
        }

    @staticmethod
    def get_default_values():
        return {
            "k": 0.9
        }

    @staticmethod
    def get_default_ranges():
        return {
            "k": [0.1,1]
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
            if key == "k" and (value < 0 or value > 1):
                raise ValueError("Le paramètre 'k' doit être un nombre compris entre 0 et 1.")
            return True
        except Exception as e:
            return str(e)
