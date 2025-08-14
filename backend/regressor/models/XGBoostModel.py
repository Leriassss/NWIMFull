class XGBoostModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode XGBoost.
    """

    def __init__(self, max_depth, learning_rate, n_estimators, gamma, lambda_):
        """
        Initialise et valide les données pour la méthode XGBoost.
        :param max_depth: Profondeur maximale des arbres (int > 0)
        :param learning_rate: Taux d'apprentissage (float > 0)
        :param n_estimators: Nombre d'arbres (int > 0)
        :param gamma: Régularisation gamma (float >= 0)
        :param lambda_: Régularisation lambda (float >= 0)
        """
        self.max_depth = int(float(max_depth))
        self.learning_rate = float(learning_rate)
        self.n_estimators = int(float(n_estimators))
        self.gamma = float(gamma)
        self.lambda_ = float(lambda_)
        self.validate()

    def validate(self):
        """Valide les paramètres."""
        if self.max_depth <= 0:
            raise ValueError("Le paramètre 'max_depth' doit être un entier strictement positif.")
        if self.learning_rate <= 0:
            raise ValueError("Le paramètre 'learning_rate' doit être un nombre strictement positif.")
        if self.n_estimators <= 0:
            raise ValueError("Le paramètre 'n_estimators' doit être un entier strictement positif.")
        if self.gamma < 0:
            raise ValueError("Le paramètre 'gamma' doit être >= 0.")
        if self.lambda_ < 0:
            raise ValueError("Le paramètre 'lambda' doit être >= 0.")

    def to_dict(self):
        """Retourne les paramètres sous forme de dictionnaire."""
        return {
            'max_depth': self.max_depth,
            'learning_rate': self.learning_rate,
            'n_estimators': self.n_estimators,
            'gamma': self.gamma,
            'lambda': self.lambda_
        }

    @staticmethod
    def get_parameter_names():
        """Retourne un mapping clé → nom lisible."""
        return {
            "max_depth": "Profondeur maximale",
            "learning_rate": "Taux d'apprentissage",
            "n_estimators": "Nombre d'arbres",
            "gamma": "Régularisation gamma",
            "lambda": "Régularisation lambda"
        }

    @staticmethod
    def get_default_ranges():
        """Retourne les plages de valeurs par défaut."""
        return {
            "max_depth": [1, 15],
            "learning_rate": [0.01, 0.3],
            "n_estimators": [50, 1000],
            "gamma": [0, 5],
            "lambda": [0, 10]
        }

    @staticmethod
    def get_default_values():
        """Retourne les valeurs par défaut."""
        return {
            "max_depth": 6,
            "learning_rate": 0.1,
            "n_estimators": 100,
            "gamma": 0,
            "lambda": 1
        }

    @staticmethod
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique.
        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre.
        :return: True si valide, sinon message d'erreur.
        """
        try:
            if key in ("learning_rate", "gamma", "lambda"):
                value = float(value)
            else:
                value = int(float(value))

            if key == "max_depth" and value <= 0:
                raise ValueError("Le paramètre 'max_depth' doit être > 0.")
            elif key == "learning_rate" and value <= 0:
                raise ValueError("Le paramètre 'learning_rate' doit être > 0.")
            elif key == "n_estimators" and value <= 0:
                raise ValueError("Le paramètre 'n_estimators' doit être > 0.")
            elif key == "gamma" and value < 0:
                raise ValueError("Le paramètre 'gamma' doit être >= 0.")
            elif key == "lambda" and value < 0:
                raise ValueError("Le paramètre 'lambda' doit être >= 0.")
            return True
        except Exception as e:
            return str(e)
