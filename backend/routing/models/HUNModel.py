class HUNModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode HUN.
    """

    def __init__(self, time_base):
        """
        Initialise et valide les données pour la méthode HUN.
        :param time_base: Temps de base observé pour le transfert (en jours).
        """
        self.time_base = int(time_base)
        self.validate()

    def validate(self):
        if  self.time_base <= 0:
            raise ValueError("Le paramètre 'time_base' doit être un entier strictement positif.")

    def to_dict(self):
        return {
            'time_base': self.time_base
        }

    @staticmethod
    def get_parameter_names():
        return {
            "time_base": "time base"
        }

    @staticmethod
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique pour la méthode HUN.

        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre à valider.
        :return: True si valide, sinon un message d'erreur est retourné.
        """
        try:
            value = float(value)  # S'assure que la valeur est un nombre
            if key == "time_base" and value <= 0:
                raise ValueError("Le paramètre 'time_base' doit être un entier strictement positif.")
            return True
        except Exception as e:
            return str(e)
