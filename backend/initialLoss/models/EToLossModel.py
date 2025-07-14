class EToLossModel:
    """
    Modèle de données pour valider les paramètres de la méthode des pertes basées sur l'évapotranspiration potentielle (ETo).
    """

    def __init__(self, alpha: float):
        """
        Initialise et valide les données pour le modèle de pertes ETo.

        :param alpha: Coefficient d'évapotranspiration (doit être compris entre 0 et 1).
        """
        self.alpha = float(alpha)
        self.validate()

    def validate(self):
        """
        Vérifie que les paramètres sont valides.
        """
        self.alpha = float(self.alpha)
         

    def to_dict(self):
        """
        Retourne un dictionnaire des paramètres du modèle.
        """
        return {
            'alpha': self.alpha
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne les noms des paramètres du modèle.
        """
        return {
            "alpha": "evap. coeff"
        }

    @staticmethod
    def get_default_values():
        return {
            "alpha" : 1
        }

    @staticmethod
    def get_default_ranges():
        return {
            "alpha": [0,1]
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
            value = float(value) 
            if key != "alpha" :
                raise ValueError("Parametre inconnu !!!")
            return True
        except Exception as e:
            return str(e)
