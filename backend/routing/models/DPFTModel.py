class DPFTModel:
    """
    Modèle de données pour la méthode DPFT.
    """

    def __init__(self, time_base=5):
        self.time_base = time_base
        self.validate()

    def validate(self):
        """
        Valide le paramètre 'time_base'.

        Raises
        ------
        ValueError : Si 'time_base' n'est pas un entier strictement positif.
        """
        if not isinstance(self.time_base, int) or self.time_base <= 0:
            raise ValueError("Le paramètre 'time_base' doit être un entier strictement positif.")

    def to_dict(self):
        """
        Convertit l'objet en un dictionnaire.

        :return: Dictionnaire des paramètres du modèle DPFT.
        """
        return {
            'time_base': self.time_base
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres pour la méthode DPFT.

        :return: Dictionnaire des noms des paramètres.
        """
        return {
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
            value = int(value)  # S'assure que la valeur est un entier
            if key == "time_base":
                if value <= 0:
                    raise ValueError("Le paramètre 'time_base' doit être un entier strictement positif.")
            else:
                raise ValueError(f"Paramètre inconnu: {key}")
            return True
        except ValueError as e:
            return str(e)
