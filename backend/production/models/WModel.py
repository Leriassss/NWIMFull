class WModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode WMin.
    """

    def __init__(self, runoff_coef = 0.25):
        """
        Initialise et valide les données pour la méthode WMin.

        :param runoff_coef: Coefficient de ruissellement, doit être compris entre 0 et 1.
        """
        self.runoff_coef = int(runoff_coef)
        self.validate()

    def validate(self):
        if (self.runoff_coef <= 0 or self.runoff_coef> 1):
            raise ValueError("Le coefficient de ruissellement doit être compris entre 0 et 1.")

    def to_dict(self):
        return {
            "w": self.runoff_coef,
        }

    @staticmethod
    def get_parameter_names():
        return {
            "w": "coef. ruissellement"
        }
    
    @staticmethod
    def get_default_ranges():
        return {
                "w": [0,1],
            }
    
    @staticmethod
    def get_default_values():
        return {
                "w": 0.25
            }

    @staticmethod
    def validate_parameter(key, value):
        try:
            value = float(value)  # S'assure que la valeur est un nombre
            if key == "w" and (value <= 0 or value > 1):
                raise ValueError("Le coefficient de ruissellement doit être compris entre 0 et 1.")
            return True
        except Exception as e:
            return str(e)
