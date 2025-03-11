class PLossModel:
    """
    Modèle de données pour valider les paramètres de la méthode des pertes proportionnelles (P).
    """

    def __init__(self, p: float):
        """
        Initialise et valide les données pour le modèle de pertes proportionnelles.

        :param p: Coefficient de perte proportionnelle (doit être compris entre 0 et 1).
        """
        self.p = p
        self.validate()

    def validate(self):
        """
        Vérifie que le paramètre est valide.
        """
        if self.p < 0 or self.p >= 1:
            raise ValueError("Le paramètre 'p' doit être compris entre 0 et 1.")

    def to_dict(self):
        """
        Retourne un dictionnaire des paramètres du modèle.
        """
        return {
            'p': self.p
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres du modèle.
        """
        return {
            "p": "loss % "
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
            value = float(value)  # Vérifie que la valeur est numérique
            if key == "p" and (value < 0 or value >= 1):
                raise ValueError("Le paramètre 'p' doit être compris entre 0 et 1.")
            return True
        except ValueError as e:
            return str(e)
