class NashModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode Nash.
    """

    def __init__(self, nash_k, nash_n, time_base=5):
        """
        Initialise et valide les données pour la méthode Nash.

        :param nash_k: Paramètre de la méthode Nash (doit être strictement positif).
        :param nash_n: Paramètre de la méthode Nash (doit être strictement positif).
        :param time_base: Temps de base pour le transfert (jour), valeur par défaut est 5.
        """
        self.nash_k = float(nash_k)
        self.nash_n = float(nash_n)
        self.time_base = int(time_base)
        self.validate()

    def validate(self):
        """
        Valide les paramètres nash_k, nash_n et time_base.

        Raises
        ------
        ValueError : Si nash_k, nash_n ou time_base ne sont pas valides.
        """
        if self.nash_k <= 0 or self.nash_n <= 0 or self.time_base <= 0:
            raise ValueError("Les paramètres 'nash_k', 'nash_n' et 'time_base' doivent être strictement positifs.")

    def to_dict(self):
        """
        Convertit l'objet en un dictionnaire.

        :return: Dictionnaire des paramètres du modèle Nash.
        """
        return {
            'nash_k': self.nash_k,
            'nash_n': self.nash_n,
            'time_base': self.time_base
        }

    @staticmethod
    def get_default_values():
        return {
            'nash_k': 25,
            'nash_n': 3,
            'time_base': 8
        }

    @staticmethod
    def get_default_ranges():
        return {
            'nash_k': [1,100],
            'nash_n': [1,5],
            'time_base': [1,30]
            }
    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres pour la méthode Nash.

        :return: Dictionnaire des noms des paramètres.
        """
        return {
            "nash_k": "nash_k",
            "nash_n": "nash_n",
            "time_base": "time_base"
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
            if key == "nash_k" and value <= 0:
                raise ValueError("Le paramètre 'nash_k' doit être strictement positif.")
            elif key == "nash_n" and value <= 0:
                raise ValueError("Le paramètre 'nash_n' doit être strictement positif.")
            elif key == "time_base" and value <= 0:
                raise ValueError("Le paramètre 'time_base' doit être strictement positif.")
            return True
        except Exception as e:
            return str(e)
