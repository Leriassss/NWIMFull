class SeparationModel:
    """
    Classe pour valider les arguments communs aux méthodes de récession.
    """
    def __init__(self, k =  0.1, window = 10):
        """
        Initialise et valide les arguments communs aux méthodes de récession.

        :param lambda_: Paramètre lambda (doit être un nombre positif).
        """
        self.k = float(k)
        self.window = int(float(window))
        self.validate()

    def validate(self):
        """
        Valide le paramètre lambda.
        """
        if  self.k  <= 0:
            raise ValueError("alpha doit être un nombre entre 0 et 1.")
        if  self.window <= 0:
            raise ValueError("window doit être un nombre entre 0 et 1.")

    def to_dict(self):
        """
        Retourne les paramètres du modèle sous forme de dictionnaire.
        """
        return {
            'k': self.k,
            'window' : self.window
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne le nom du paramètre 'lambda' pour le modèle Separation.
        """
        return {
            "k" : "k",
            "window" : "window"
        }
    @staticmethod
    def get_default_values():
        return {
                "k" : 0.1,
                "window" : 10
            }

    @staticmethod
    def get_default_ranges():
        return {
                "k" : [0.1,1],
                "window" : [1, 50]
        }
    
    @staticmethod
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique pour Separation.

        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre à valider.
        :return: True si valide, sinon un message d'erreur est retourné.
        """
        try:
            value = float(value)  # S'assure que la valeur est un nombre
            if key == "k" and value <= 0:
                raise ValueError("Le paramètre doit être un nombre strictement positif.")
            if key == "window" and int(value) <= 0:
                raise ValueError("Le paramètre doit être un nombre strictement positif.")
            return True
        except Exception as e:
            return str(e)
