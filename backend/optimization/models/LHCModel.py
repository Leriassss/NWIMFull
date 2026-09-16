class LHCModel:
    def __init__(self, n_samples=10):
        self.n_samples = int(n_samples)

        self.validate()

    def validate(self):
        """ Vérifie tous les paramètres à l'initialisation. """
        for key, value in self.to_dict().items():
            validation = self.validate_parameter(key, value)
            if validation is not True:
                raise ValueError(validation)

    def to_dict(self):
        """ Retourne les paramètres sous forme de dictionnaire. """
        return {
            'n_samples': self.n_samples
        }

    @staticmethod
    def get_parameter_names():
        """ Retourne les noms des paramètres avec leurs descriptions. """
        return {
            'n_samples': "Nombre d'échantillons "
        }

    @staticmethod
    def get_default_values():
        return {
                "n_samples": 10
        }

    @staticmethod
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique.

        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre à valider.
        :return: True si valide, sinon un message d'erreur.
        """
        try:
            value = int(value)
            if key == "n_samples":
                if value <= 0:
                    raise ValueError("n_samples doit être un entier positif.")
            return True
        except Exception as e:
            return str(e)
