class PLAModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode PLA.
    """

    def __init__(self, mu, landa):
        """
        Initialise et valide les données pour la méthode PLA.

        :param mu: Paramètre mu, doit être strictement positif.
        :param landa: Paramètre landa, doit être strictement positif.
        :param t_x: Paramètre t_x, doit être strictement positif.
        :param s_f: Paramètre s_f, doit être strictement positif.
        """
        self.mu = float(mu)
        self.landa = float(landa)
        self.validate()

    def validate(self):
        """
        Valide les paramètres mu, landa, t_x et s_f.

        Raises
        ------
        ValueError : Si un des paramètres est inférieur ou égal à 0.
        """
        if self.mu <= 0:
            raise ValueError("Le paramètre 'mu' doit être strictement positif.")
        if self.landa <= 0:
            raise ValueError("Le paramètre 'landa' doit être strictement positif.")

    def to_dict(self):
        """
        Convertit l'objet en un dictionnaire.

        :return: Dictionnaire des paramètres du modèle PLA.
        """
        return {
            'mu': self.mu,
            'landa': self.landa
        }

    @staticmethod
    def get_default_values():
        return {
            'mu': 1.03,
            'landa': 9
        }

    @staticmethod
    def get_default_ranges():
        return {
            'mu': [1,10],
            'landa': [1,10]
            }
    
    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres pour la méthode PLA.

        :return: Dictionnaire des noms des paramètres.
        """
        return {
            "mu": "mu",
            "landa": "landa"
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
            if key == "mu":
                if value <= 0:
                    raise ValueError("Le paramètre 'mu' doit être strictement positif.")
            elif key == "landa":
                if value <= 0:
                    raise ValueError("Le paramètre 'landa' doit être strictement positif.")
            else:
                raise ValueError(f"Paramètre inconnu: {key}")
            return True
        except Exception as e:
            return str(e)
