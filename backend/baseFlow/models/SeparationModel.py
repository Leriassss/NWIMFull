class SeparationModel:
    """
    Classe pour valider les arguments communs aux méthodes de récession.
    """
    def __init__(self, lambda_=0.3):
        """
        Initialise et valide les arguments communs aux méthodes de récession.

        :param lambda_: Paramètre lambda (doit être un nombre positif).
        """
        self.lambda_ = lambda_
        self.validate()

    def validate(self):
        """
        Valide le paramètre lambda.
        """
        if self.lambda_ <= 0:
            raise ValueError("Le paramètre 'lambda' doit être un nombre positif.")

    def to_dict(self):
        """
        Retourne les paramètres du modèle sous forme de dictionnaire.
        """
        return {
            'lambda': self.lambda_
        }

    @staticmethod
    def get_parameter_names():
        """
        Retourne le nom du paramètre 'lambda' pour le modèle Separation.
        """
        return {
            "lambda": "lambda"
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
                raise ValueError("Le paramètre 'lambda' doit être un nombre positif.")
            return True
        except Exception as e:
            return str(e)
