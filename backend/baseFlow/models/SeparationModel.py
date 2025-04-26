class SeparationModel:
    """
    Classe pour valider les arguments communs aux méthodes de récession.
    """
    def __init__(self, lambda_=0.3,k = 0.5, lag_time =  1):
        """
        Initialise et valide les arguments communs aux méthodes de récession.

        :param lambda_: Paramètre lambda (doit être un nombre positif).
        """
        self.lambda_ = float(lambda_)
        self.lag_time = float(lag_time)
        self.k = float(k)
        self.validate()

    def validate(self):
        """
        Valide le paramètre lambda.
        """
        try :
            self.k = float(self.k)
        except :
            raise ValueError("Le paramètre 'lambda' doit être un nombre positif.")
        if self.lambda_ <= 0:
            raise ValueError("Le paramètre 'lambda' doit être un nombre positif.")
        if self.lag_time <= 0:
            raise ValueError("Le paramètre 'lag_time' doit être un nombre positif.")

    def to_dict(self):
        """
        Retourne les paramètres du modèle sous forme de dictionnaire.
        """
        return {
            'lambda': self.lambda_,
            'k' : self.k,
            'lag_time': self.lag_time
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne le nom du paramètre 'lambda' pour le modèle Separation.
        """
        return {
            "lambda": "lambda",
            "k" : "k",
            "lag_time" : "lag time"
        }
    @staticmethod
    def get_default_values():
        return {
                "lambda": 0.8,
                "k" : 0.5,
                "lag_time" : 2
            }

    @staticmethod
    def get_default_ranges():
        return {
                "lambda": [0.1,1],
                "k" : [0.1,1],
                "lag_time" : [1,10]
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
            if key == "lambda" and value <= 0:
                raise ValueError("Le paramètre doit être un nombre strictement positif.")
            elif key == "lag_time" and value <= 0:
                raise ValueError("Le paramètre doit être un nombre strictement positif.")
            elif key == "k" and value <= 0:
                raise ValueError("Le paramètre doit être un nombre strictement positif.")
            return True
        except Exception as e:
            return str(e)
