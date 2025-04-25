class PhiModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode Phi.
    """


    def __init__(self, c_r: float):
        """
        Initialise et valide les données pour la méthode Phi.

        :param prec: Série pandas contenant les précipitations (en mm).
        :param c_r: Coefficient de ruissellement (entre 0 et 1).
        """
        self.c_r = c_r
        self.validate()

    @staticmethod
    def get_default_values():
        return {
                "c_r": 0.25
            }

    def validate(self):
        """
        Valide les paramètres du modèle.
        """
        if self.c_r <= 0 or self.c_r > 1:
            raise ValueError("Le coefficient de ruissellement 'c_r' doit être compris entre 0 et 1.")

    def to_dict(self):
        return {
                    'c_r': self.c_r
                }


    @staticmethod
    def get_parameter_names():
        return {
                    'c_r': "coef. ruissellement",
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

            if key == "c_r" and (value <= 0 or value > 1):
                raise ValueError("Le coefficient de ruissellement 'c_r' doit être compris entre 0 et 1.")

            return True  # Si aucune erreur, le paramètre est valide

        except Exception as e:
            return str(e)  # Retourne le message d'erreur
